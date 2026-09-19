#!/usr/bin/env python3
"""
Module for reading log files for the State QSO Party contest. It uses the 
Cabrillo parser to read and parse the log files. Most of the validation of the log file
has been done by Bruce Horn's log uploaders, but the Cabrillo parser will catch some errors and
do additional validation of the log file.

The Cabrillo object created for each log file, along with some other information
is added to the results data structure for further processing.

Do the paarsing and validation as we read them into the results data structure. 
This is a single-pass process that reads the log file, parses the QSOs, and validates the data as it is read.
It reads in a log file, parses the header info, checks it for errors, and then stores it into the results data structure. 
Next it parses each QSO line, checks it for errors, and stores it into the results data structure.
No scoring can be done at this point because we have not done cross-checking of the QSOs yet.
Called only by batch.py


Some of the processing of log files must wait until all the files are in hand, like cross-checking, scoring, and reporting. But other tasks are done as the individual files are read in, indluding:
- parse the header and QSO lines into a cabrillo object
- validate both the header and QSO lines
- extract the QSO information into a more convenient data structure for later use
- create an qso_index_dict index file of QSOs key'ed by received call (dx_call in the cabrillo object), 
        which is used in cross-checking for quick lookup
- create a set of all callsigns that submitted logs for UNIQUE detection
"""

from pprint import pprint
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest import result
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from utilities import generate_index_key, get_dxcc

# Import your existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    CONTEST_YEAR, BATCH_INPUT_DIR, HQ_FIELDS
)
SCRIPT_DIR = Path(__file__).resolve().parent

def read_prepare(s):
    """
    Main loop to read, parse, and validate log files in the incoming directory.
    This function is called by batch.py and processes all logs for the specified contest year.

    For each log file:
    - parse file
    - save cab Cabrillo object both as object and dict of vars
    """
    dir_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR).resolve()
    filenames = [p.name for p in dir_path.iterdir() if p.is_file()]
    for file in filenames:
        # print(f"READING {file}")
        s.stats["total_logs"] += 1
        try:
            file_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR / file).resolve()
            cab = parse_log_file(file_path, ignore_unknown_key=True, check_categories=False, ignore_order=True, check_mode=False)
            # print(f"CAB {cab.callsign} # qsos {len(cab.qso)}")
        except Exception as e:
            if file:
                s.stats["rejected_logs"] += 1
                s.stats["rejected_logs_filenames"].append(file)
                print(f"ERROR: log file {file} was rejected by the parser - REJECTED")
                s.out_files['error_file'].write(f"ERROR: log file {file} was rejected by the parser - REJECTED\n")
                continue
        # Process Bruce Horn's HQ keys and adding and replacing values in the cab object
        if not process_hq_keys(s, cab):
            s.stats["rejected_logs"] += 1
            s.stats["rejected_logs_filenames"].append(file)
            print(f"ERROR: log file {file} had no HQ- keys - REJECTED")
            s.out_files['error_file'].write(f"ERROR: log file {file} had no HQ- keys - REJECTED\n")
            continue
        
        s.stats["valid_logs"] += 1
        # print(vars(cab))
        
        result = s._init_result()

        # update result if a DX station
        result['dxcc_code'], result['dxcc_entity'] = get_dxcc(s, cab.location, cab.callsign)

        # Add the callsign to the set of all callsigns for UNIQUE detection
        s.all_callsigns.add(cab.callsign)

        # Add MOBILE stations to that set
        if cab.category_station.upper() == 'MOB':
            s.mobile_callsigns.add(cab.callsign)

        result['cab'] = cab
        result['callsign'] = cab.callsign.upper().split('/')[0]
        update_qso_index_dict(s, result, cab.qso, result['dxcc_entity'])
        # result['header_attribs'] = vars(cab)
        s.results.append(result)
        # print('BREAK')
   
def update_qso_index_dict(s, result, qsos, dxcc):
    """
    Update the qso_index_dict for quick lookup of QSOs by 
    received call (dx_call in the cabrillo object) plus mode plus band
    This function is called after reading and preparing each log file.
    """
    qso_count = 0
    # print(f"BEGIN index_dict: qso_count: {qso_count} total: {result['total_qsos']} valid: {result['valid_qsos']} call: {result['callsign']}")
    for qso in qsos:
        qso_count += 1
        s.stats['total_qsos'] += 1
        result['total_qsos'] += 1
        # remove non-TX to non-TX
        if qso.de_exch[1] not in s.counties and  qso.dx_exch[1] not in s.counties:
            s.out_files['error_file'].write(f"QSO Invalid NTX or TX to NTX or TX from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H:%M")}Z\n")
            qso.valid = False
            # print(f"NOT VALID TX EXCH: valid qsos: total: {result['total_qsos']} valid: {result['valid_qsos']} de: {qso.de_exch[1]} dx: {qso.dx_exch[1]}")
            continue
        if not qso.valid:
            s.stats['qso_parser_not_valid'] += 1
            s.stats['calls_w_not_valid_qsos'].add(result['callsign'])
            # print(f"NOT VALID PARSER total: {result['total_qsos']} valid: {result['valid_qsos']} from parser for {result['callsign']}")
            continue
        # This is now a VALID  qso
        s.stats['valid_qsos'] += 1
        result['valid_qsos'] += 1
        # print(f"index_dict VALID total: qso_count: {qso_count} {result['total_qsos']} valid: {result['valid_qsos']}  for {result['callsign']}")
        # fix DC --> MD
        if qso.de_exch[1] == 'DC': qso.de_exch[1] = 'MD'
        if qso.dx_exch[1] == 'DC': qso.dx_exch[1] = 'MD'
        k = generate_index_key(s, qso, dxcc, False) # FALSE = key from de POV
        # print(f"END index_dict: qso_count: {qso_count} total:{result['total_qsos']} valid:{result['valid_qsos']} dx:{qso.dx_call}")
        s.qso_index_dict[k].append(qso)

def process_hq_keys(s, cab):
    try:
        if len(cab.hq_anything):
            cab.category = cab.hq_anything['HQ-CATEGORY'].upper()
            cab.cat = cab.hq_anything['HQ-CAT'].upper()
            if "HQ_CLUB" in list(cab.hq_anything.keys()):
                cab.club = cab.hq_anything['HQ-CLUB']
                # if the operator specified a club NOT in the dropdown
                if cab.club not in list(s.contest_clubs.keys()):
                    s.contest_clubs.setdefault(cab.club, 0)
            else:
                cab.club = "None"
            temp = {
                key.strip(): value.strip()
                for item in cab.hq_anything['HQ-QUESTIONS'].split(",")
                for key, value in [item.split(":", 1)]
            }
            if type(temp) == dict:
                for key in temp:
                    setattr(cab, HQ_FIELDS[key], temp[key])
                return True
    except Exception as e:
        print(f"ERROR: Exception {e} getting hq_keys")
    return False

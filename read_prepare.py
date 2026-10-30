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
import copy
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest import result
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from utilities import generate_index_key, get_dxcc, writefile
from global_stats import categorize_log, fix_exchange, record_recipient_location

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
    result_index = 0
    for file in filenames:
        s.stats["total_logs"] += 1
        try:
            file_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR / file).resolve()
            cab = parse_log_file(file_path, ignore_unknown_key=True, check_categories=False, ignore_order=True, check_mode=False)
            cab.callsign = cab.callsign.split('/')[0]
        except Exception as e:
            s.stats['exceptions'].append(f"parse: {file_path}: {e}")
            if file:
                s.stats["rejected_logs"] += 1
                s.stats["rejected_logs_filenames"].append(file)
                print(f"ERROR - REJECTED: log file {file} was rejected by the parser")
                s.out_files['errors'].write(f"REJECTED log file {file} was rejected by the parser\n")
                continue
        # adds category, cat, category, club, and other Bruce Horn HQ-anything fields to cab
        if not process_hq_keys(s, cab):
            s.stats["rejected_logs"] += 1
            s.stats["rejected_logs_filenames"].append(file)
            print(f"ERROR: log file {file} had no HQ- keys - REJECTED")
            s.out_files['errors'].write(f"log file {file} had no HQ- keys - REJECTED\n")
            continue
        
        result = s._init_result()

        # Add the callsign to the set of all callsigns for UNIQUE detection
        if cab.callsign in list(s.all_callsigns.keys()):
            # multiple logs with the same callsign
            s.out_files['dups'].write(f"DUPLICATE CALLSIGN: logfile {file} has same callsign as a previous log had\n")
            print(f"ERROR: DUPLICATE CALLSIGN: logfile {file} has same callsign as a previous log had")
        else:
            # we are storing the indix into the results list for each callsign so we have quick access
            # to the results for any callsign. Could have done the results object as a dict, but dit not
            # maybe when refactoring....
            s.all_callsigns[cab.callsign] = result_index
            result_index += 1
        
        # update result if a DX station
        result['dxcc_code'], result['dxcc_entity'] = get_dxcc(s, cab.location, cab.callsign)
        s.code_to_dxcc[result['dxcc_code']] = result['dxcc_entity']
        result['cab'] = cab
        result['callsign'] = cab.callsign.upper().split('/')[0]
        update_qso_index_dict(s, result, cab)
        # result['header_attribs'] = vars(cab)
        s.results.append(result)
   
def update_qso_index_dict(s, result, cab):
    """
    Update the qso_index_dict for quick lookup of QSOs by 
    received call (dx_call in the cabrillo object) plus mode plus band
    This function is called after reading and preparing each log file.
    """
    # 14037 CW 2026-09-19 1929 AA0AW 599 MN AD4EB 599 MARI
    uncategorized = True

    # print(f"BEGIN index_dict: qso_count: {qso_count} total: {result['total_qsos']} valid: {result['valid_qsos']} call: {result['callsign']}")
    for num_qso, qso in enumerate(cab.qso):
        if uncategorized and num_qso < 5:
            # we will decrement this counter IFF we cannot categorize the log
            if not categorize_log(s, result, qso):
                s.stats['uncategorized_logs'] += 1
            else:
                uncategorized = False
        s.stats['total_qsos'] += 1
        result['total_qsos'] += 1
        # just take the first part of each call sign
        qso.de_call = qso.de_call.split('/')[0].upper()
        qso.dx_call = qso.dx_call.split('/')[0].upper()
        if qso.de_exch[1] == 'DC': qso.de_exch[1] = 'MD'
        if qso.dx_exch[1] == 'DC': qso.dx_exch[1] = 'MD'
        
        # multiple counties in sender exchange
        if '/' in qso.de_exch[1]:
            s.stats['bad_exchanges'].add(qso.de_exch[1])
            s.stats['multi_county_exchanges'] += 1
            counties = qso.de_exch[1].split('/')
            qso.de_exch[1] = counties[0]
            for c in counties[1:]:
                new_qso = copy.deepcopy(qso)
                new_qso.de_exch[1] = c
                result['cab'].qso.append(new_qso)
        # multiple counties in receiver exchange
        if '/' in qso.dx_exch[1]:
            s.stats['bad_exchanges'].add(qso.dx_exch[1])
            s.stats['multi_county_exchanges'] += 1
            counties = qso.dx_exch[1].split('/')
            qso.dx_exch[1] = counties[0]
            for c in counties[1:]:
                new_qso = copy.deepcopy(qso)
                new_qso.dx_exch[1] = c
                result['cab'].qso.append(new_qso)

        # remove non-TX to non-TX and make sure at least one exchange is a county
        if qso.de_exch[1].isalpha() and qso.de_exch[1] not in s.counties and qso.dx_exch[1].isalpha() and qso.dx_exch[1] not in s.counties:
            # neither exchange is a TX county, so this is an invalid QSO
            qso.valid = False  # so it will not be used in scoring
            result['other_invalid_qsos'] += 1

            s.stats['other_invalid_qsos'] += 1
            s.stats['invalidated_qsos'] += 1
            writefile(s, result, 'Neither exchange is a TX county:', ['errors', 'other_invalid_qsos'])
            continue
        if qso.de_exch[1] == 'TX' or  qso.dx_exch[1] == 'TX':
            # one or both exchanges is "TX", which is invalid, so this is an invalid QSO
            result['other_invalid_qsos'] += 1
            s.stats['other_invalid_qsos'] += 1
            s.stats['invalidated_qsos'] += 1
            writefile(s, result, 'One or both exchanges is "TX":', ['errors'])
            continue

        got_location = record_recipient_location(s, qso, result)
        if not got_location:
            # this is an invalid QSO, so we will not score it
            continue
        
        # This is now a VALID QSO
        result['valid_qsos'] += 1
        # capture the stats about the receiver of this contact
        record_recipient_location(s, qso, result)
        k = generate_index_key(s, qso, result['callsign'], False) # FALSE = key from de POV
        s.qso_index_dict[k].append(qso)

def process_hq_keys(s, cab):
    try:
        if 'hq_anything' in list(cab.__dict__.keys()):
            cab.category = cab.hq_anything['HQ-CATEGORY'].upper()
            temp = cab.hq_anything['HQ-CAT'].upper().split()
            try:
                x = len(cab.cat)
            except Exception as e:
                # s.stats['exceptions'].append(f"cab.cat: {cab.callsign}: {e}")
                cab.cat = ''
                for t in temp:
                    if t == "TXM":
                        cab.cat += 'TM'
                    else:
                        cab.cat += t[:1]
            if "HQ-CLUB" in list(cab.hq_anything.keys()) and cab.hq_anything['HQ-CLUB'] != 'None' and cab.hq_anything['HQ-CLUB'] in s.contest_clubs: 
                cab.club = cab.hq_anything['HQ-CLUB']
                if not cab.club.isupper():
                    cab.club.lower().title()
                if cab.club in list(s.contest_clubs.keys()):
                    s.contest_clubs[cab.club] += 1
                else:
                    s.contest_clubs[cab.club] = 1
            else:
                cab.club = None


            # process the HQ_FIELDS
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
        
        s.stats['exceptions'].append(f"process_hq_keys: {cab.callsign}: {e}")
        print(f"ERROR: Exception {e} getting hq_keys")
    return False

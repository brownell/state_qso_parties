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
"""

"""
This module reads each of the log files in the incoming directory. It uses the 
Cabrillo parser to read and parse the log files. Most of the validation of the log file
has been done by Bruce Horn's log uploaders, but the Cabrillo parser will catch some errors and
do additional validation of the log file.

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
from cabrillo.qso import frequency_to_band

# Import your existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, 
    STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS,
    US_PREFIXES, CANADIAN_PREFIXES, QRZ_CALLSIGN, QRZ_PASSWORD,
    PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE,
    CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, CONTEST_YEAR, 
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES, BATCH_INPUT_DIR, HQ_FIELDS
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
    TEST_LOGS = ['AA0AW.log', 'K5OT.log', 'KA5D.log', 'KK5TY.log', 'N5NA.log', 'W5LO.log']
    dir_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR).resolve()
    filenames = [p.name for p in dir_path.iterdir() if p.is_file()]
    for file in filenames:
        # for testing purposes
        if file not in TEST_LOGS:
            continue
        s.stats["total_logs"] += 1
        try:
            file_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR / file).resolve()
            cab = parse_log_file(file_path, ignore_unknown_key=True, check_categories=False,
                   ignore_order=True, check_mode=False)
        except Exception as e:
            if file:
                s.stats["rejected_logs"] += 1
                s.stats["rejected_logs_filenames"].append(file)
            print(f"ERROR: log file {file} was rejected by the parser - REJECTED")
            continue
        # print out test logs cab object
        # Process Bruce Horn's HQ keys and adding and replacing values in the cab object
        if not process_hq_keys(cab):
            s.stats["rejected_logs"] += 1
            s.stats["rejected_logs_filenames"].append(file)
            print(f"ERROR: log file {file} had no HQ- keys - REJECTED")
            continue
        
        s.stats["valid_logs"] += 1
        # print(vars(cab))
        new_result = s._init_result()

        new_result['cab'] = cab
        new_result['callsign'] = cab.callsign.upper()

        # Add the callsign to the set of all callsigns for UNIQUE detection
        s.all_callsigns.add(new_result['callsign'])

        # Add MOBILE stations to that set
        if cab.category_station.upper() == 'MOBILE':
            s.mobile_callsigns.add(new_result['callsign'])

        update_qso_index_dict(s, new_result, cab.qso)
        extract_qso_info(new_result)
        
        if file in TEST_LOGS:
            print(f"vars(cab)")
        s.results.append(new_result)
        new_result['header_attribs'] = vars(cab)
        print('BREAK')
   
def update_qso_index_dict(s, new_result, qsos):
    """
    Update the qso_index_dict for quick lookup of QSOs by 
    received call (dx_call in the cabrillo object) plus mode plus band
    This function is called after reading and preparing each log file.
    """
    for qso in qsos:
        s.stats['total_qsos'] += 1
        if not qso.valid:
            s.stats['qso_parser_not_valid'] += 1
            s.stats['calls_w_not_valid_qsos'].add(new_result['callsign'])
            continue
        s.stats['qso_valids'] += 1
        k = s._generate_index_key(qso, False) # FALSE = key for myself
        s.qso_index_dict[k].append(qso)
        
def extract_qso_info(new_result):
    qso_list = new_result['cab'].qso
    for qso in qso_list:
        new_result['qso_data'].append(vars(qso))

def check_callsign_is_DX(s, new_result):
        ## check if this log is from a DX station. If so, replace his de_exch with his DXCC entity 
        try:
            dx_callsign  = s.my_callinfo.get_all(new_result['callsign'])
        except Exception as e:
            return
        try:            
            if dx_callsign and ((dx_callsign['country'] not in ['United States', 'Canada'])): # log of DX station
                dxcc_entity = s.dxcc_entities[int(dx_rcvd_qth['adif'])]
                new_result['dxcc_entity'] = dxcc_entity
        except Exception as e:
            rcvd_qth = qso['rcvd_qth']
            dx_rcvd_qth = None
            result['warnings'].append(f"ERROR QSO: cannot determine if rcvd_qth is DX for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")
            print(f"Exception {e} sender {result['callsign']} cannot determine if rcvd_qth is DX for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")
     
def process_hq_keys(cab):
    if cab.hq_anything and cab.hq_anything.get('HQ-CATEGORY', False) and cab.hq_anything.get('HQ-QUESTIONS', False) and cab.hq_anything.get('HQ-CLUB', 'None') and cab.hq_anything.get('HQ-CAT', False):
        cab.category = cab.hq_anything['HQ-CATEGORY'].upper()
        cab.cat = cab.hq_anything['HQ-CAT'].upper()
        cab.club = cab.hq_anything.get('HQ-CLUB', False)
        temp = {
            key.strip(): value.strip()
            for item in cab.hq_anything['HQ-QUESTIONS'].upper().split(",")
            for key, value in [item.split(":", 1)]
        }
        if type(temp) == dict:
            for key in temp:
                setattr(cab, HQ_FIELDS['HQ-QUESTIONS'][key], temp[key])
        else:
            return False
    else:
        cab.category = "_".join([cab.category_station.upper(), cab.category_mode.upper(), cab.category_power.upper()])
        return False


    
### UTILITY FUNCTIONS ###


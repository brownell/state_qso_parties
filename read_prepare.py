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
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES, BATCH_INPUT_DIR
)


def read_prepare(s):
    """
    Main loop to read, parse, and validate log files in the incoming directory.
    This function is called by batch.py and processes all logs for the specified contest year.

    For each log file:
    - parse file
    - save cab Cabrillo object both as object and dict of vars
    """

    input_dir = BATCH_INPUT_DIR + '/'  + CONTEST_YEAR + '/'
    filenames = [p.name for p in Path(input_dir).iterdir() if p.is_file()]
    for file in filenames:
        try:
            cab = parse_log_file(input_dir + file, ignore_unknown_key=True, check_categories=False,
                   ignore_order=False, check_mode=False)
            print(f"parsing {cab.callsign}")
        except Exception as e:
            print(f"Error parsing log file {file}: {e}")
            continue

        new_result = s._init_result()
        new_result['cab'] = cab
        new_result['header_attribs'] = vars(cab)

        # Add the callsign to the set of all callsigns for UNIQUE detection
        s.all_callsigns.add(new_result['header_attribs']['callsign'])

        update_qso_index_dict(s, cab.qso)
        extract_qso_info(new_result)
        s.results.append(new_result)
   
def update_qso_index_dict(s, qsos):
    """
    Update the qso_index_dict for quick lookup of QSOs by 
    received call (dx_call in the cabrillo object) plus mode plus band
    This function is called after reading and preparing each log file.
    """
    for qso in qsos:
        s.qso_index_dict[s._generate_index_key(qso, True)].append(qso)
        
def extract_qso_info(new_result):
    qso_list = new_result['cab'].qso
    for qso in qso_list:
        new_result['qso_data'].append(vars(qso))
     

    
### UTILITY FUNCTIONS ###


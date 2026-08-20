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

from pprint import pprint
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest import result
import csv
from batch import shared as s
from cabrillo.parser import parse_log_file

# Import your existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, 
    STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS,
    US_PREFIXES, CANADIAN_PREFIXES, QRZ_CALLSIGN, QRZ_PASSWORD,
    PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE,
    CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS,
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES, BATCH_INPUT_DIR
)

def read_prepare():
    """
    Main loop to read, parse, and validate log files in the incoming directory.
    This function is called by batch.py and processes all logs for the specified contest year.
    """
    results_index = -1
    if BATCH_INPUT_DIR:
            with open(BATCH_INPUT_DIR, 'r', encoding='utf-8', errors='replace') as f:
                try:
                  cab = parse_log_file(f, ignore_unknown_key=True)
                except Exception as e:
                    print(f"Error parsing log file {BATCH_INPUT_DIR}: {e}")
                    return

                new_result = s.init_result()
                new_result['cab'] = cab
                new_result['attribs'] = vars(cab)
                s.results.append(new_result)
                s.all_callsigns.add(new_result['attribs']['callsign'])
                update_qso_index(new_result['attribs'])
                extract_qso_info(cab.qso, results_index)
                results_index += 1
    
def update_qso_index(a):
    """
    Update the QSO index for quick lookup of QSOs by band, mode, and received call.
    This function is called after reading and preparing the log files.
    """
    for qso in a['qso']:
        s.qso_index_dict[qso.call].append(qso)
        
def extract_qso_info(qso_list, results_index):
    s.results[results_index]['qsos'] = []
    
    for qso in qso_list:
        qso_info = {
            'date': qso.date,
            'de_call': qso.de_call,
            'de_exch': qso.de_exch, 
            'dx_call': qso.de_call, 
            'dx_exch': qso.dx_exch, 
            'freq': qso.freq,
            'mo': qso.mo,
            't': qso.t,
            'valid': qso.valid
        }
        s.results[results_index]['qsos'].append(qso_info)
     

    
### UTILITY FUNCTIONS ###

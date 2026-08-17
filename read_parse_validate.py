#!/usr/bin/env python3
"""
Module for reading, parsing, and validating log files for the State QSO Party contest.
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

def main_loop():
    """
    Main loop to read, parse, and validate log files in the incoming directory.
    This function is called by batch.py and processes all logs for the specified contest year.
    """


    if BATCH_INPUT_DIR:
        with open(BATCH_INPUT_DIR, 'r', encoding='utf-8', errors='replace') as f:
            log_line_by_line(f)



## END of _log_line_by_line

### UTILITY FUNCTIONS ###

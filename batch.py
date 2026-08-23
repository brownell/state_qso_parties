#!/usr/bin/env python3
"""
State QSO Party main program to process all logs in the incoming 
directory for a given contest year.
python batch.py will process all logs in the incoming directory for the 
contest year specified in .env or config.py
Batch Control program to process ALL the logs in the incoming directory
"""

from typing import Dict, List, Set, Optional
import csv
from pyhamtools import LookupLib, Callinfo
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from collections import defaultdict

from config.config import (
    BONUS_CALLSIGN, COUNTIES_FILE, BATCH_INPUT_DIR, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, 
    STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS,
    US_PREFIXES, CANADIAN_PREFIXES, QRZ_CALLSIGN, QRZ_PASSWORD,
    PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE,
    CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, CONTEST_YEAR,
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES
    )
from database import save_result
from generate_rankings import generate_rankings
from generate_final_report import generate_final_report_html
from read_prepare import read_prepare
from cross_check import cross_check
from share import SHARED

def main(contest_year):
    '''
        Read in all the log files, save the Cabrillo object and the data, 
        save values that will be needed later
    '''
    read_prepare(context)

    '''
    Do the cross-checking, marking qsos that fail the match test.
    Warning messages are generated when qso fails match
    Failed qsos marked invalid so not counted in score
    '''
    cross_check(context)

print(f"after cross-check results - len(context._results)")

    #  Save results to database (valid and invalid)
    # valid_count = 0
    # invalid_count = 0
    # saved_count = 0
    
    # for result in shared.results:
        
    #     if result['is_valid']:
    #         valid_count += 1
    #     else:
    #         invalid_count += 1
    #         print(f"✗ {result['callsign']}: Invalid log")
    #         for error in result.get('errors', [])[:10]:  # Show first 10 errors
    #             print(f"    ERROR: {error}")
        
    #     # # Save to database (both valid and invalid for record-keeping)
    #     try:
    #         if save_result(result, contest_year):
    #             saved_count += 1
    #             status = "✓" if result['is_valid'] else "✗"
    #             # print(f"{status} {result['callsign']}: Saved to database")
    #         else:
    #             print(f"✗ {result['callsign']}: Database save failed")
    #     except Exception as e:
    #         print(f"✗ {result['callsign']}: Database error - {e}")

    # # generate rankings from the database results
    # generate_rankings(contest_year)

    # # generate_final_report_html(contest_year)
    # generate_final_report_html(contest_year)
    
    # print()
    # print("=" * 60)
    # print("Summary")
    # print("=" * 60)
    # print(f"Total processed: {len(results)}")
    # print(f"Valid logs: {valid_count}")
    # print(f"Invalid logs: {invalid_count}")
    # print(f"Saved to database: {saved_count}")
    # print()
    
if __name__ == "__main__":
    import os, sys
    from datetime import datetime
    from config.config import CONTEST_YEAR
    
    # Get year from environment or command line
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = CONTEST_YEAR
    print(f"{'*' * 10} Processing logs for year: {year}")
    context = SHARED()
    main(year)

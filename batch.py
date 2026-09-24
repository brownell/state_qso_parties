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
    CONTEST_YEAR
    )
from database import save_result
from generate_rankings import generate_rankings
from generate_final_report import generate_final_report_html
from read_prepare import read_prepare
from cross_check import cross_check
from utilities import debug_print
from share import SHARED

def main(contest_year):
    '''
        Read in all the log files, save the Cabrillo object and the data, 
        save values that will be needed later
    '''
    read_prepare(context)
    print(f"after read_prepare")


    '''
    Do the cross-checking, marking qsos that fail the match test.
    Warning messages are generated when qso fails match
    Failed qsos marked invalid so not counted in score
    '''
    cross_check(context)

    # for debugging, print out all the scores
    # for r in context.results:
    #     debug_print(context, r, "", False)
        # print(f" {r['callsign']} CW {r['cw_qsos']} PH {r['ph_qsos']} points {r['qso_points']} mults {r['total_multipliers']} score {r['score_wo_bonus']} valid {r['valid_qsos']}\n{r['errors']}\n")

    # REMEMBER to close all the out_files
    for f in list(context.out_files.keys()):
        context.out_files[f].close()

        
    print(f"after cross-check results")


    #  Save results to database (valid and invalid)
    # valid_count = 0
    # invalid_count = 0
    # saved_count = 0
    
    for result in context.results:
        
        # # Save to database (both valid and invalid for record-keeping)
        try:
            if save_result(result, contest_year):
                saved_count += 1
                status = "✓" if result['is_valid'] else "✗"
                # print(f"{status} {result['callsign']}: Saved to database")
            else:
                print(f"✗ {result['callsign']}: Database save failed")
        except Exception as e:
            print(f"✗ {result['callsign']}: Database error - {e}")

        print('BREAK')
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

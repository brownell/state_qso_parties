#!/usr/bin/env python3
"""
State QSO Party main program to process all logs in the incoming 
directory for a given contest year.
python batch.py will process all logs in the incoming directory for the 
contest year specified in .env or config.py
Batch Control program to process ALL the logs in the incoming directory
"""

from typing import Dict, List, Set, Optional
import sqlite3
import pickle
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from collections import defaultdict

from config.config import CONTEST_YEAR
from pathlib import Path
from pprint import pprint
from pdf_final_report import generate_final_report_pdf
from read_prepare import read_prepare
from cross_check import cross_check
from utilities import fix_stats
from score_qsos import score_all_qsos
from database import save_stats, store_rankings
from share import SHARED
from config.config import DATABASE_FILE, REPORTS_ONLY, DEBUG

def main(context, contest_year):
    s = context
    db_path = Path(DATABASE_FILE)
     # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.commit()
    '''
        Read in all the log files, save the Cabrillo object and the data, 
        save values that will be needed later
    '''
    if not REPORTS_ONLY:
        print(f"Batch processing program starting for contest year {contest_year}")
        print(f"\nStarting Read and Prepare")
        read_prepare(context)
        print(f"Finished Read and Prepare: invalidated qsos: {s.stats['invalidated_qsos']}, duplicate qsos: {s.stats['duplicate_qsos']}, nils: {s.stats['nils']}, busteds: {s.stats['busteds']}")

    '''
    Do the cross-checking, marking qsos that fail the match test.
    Warning messages are generated when qso fails match
    Failed qsos marked invalid so not counted in score
    '''
    
    if not REPORTS_ONLY:
        print(f"\nStarting Cross-Check")
        cross_check(context)
        print(f"Finished Cross-Check: invalidated qsos: {s.stats['invalidated_qsos']}, duplicate qsos: {s.stats['duplicate_qsos']}, nils: {s.stats['nils']}, busteds: {s.stats['busteds']}")

    # for debugging, print out all the scores
    # if DEBUG:
    #     for r in context.results:
    #         debug_print(context, context.results[0], "", False)
    #         print(f" {r['callsign']} CW {r['cw_qsos']} PH {r['ph_qsos']} points {r['qso_points']} mults {r['total_multipliers']} score {r['score_wo_bonus']} valid {r['valid_qsos']}\n{r['errors']}\n")
    # for i in [0,10,300]:
    #     r = context.results[i]
    #     print(f"results[{i}]: {r['callsign']} {r['final_score']} {r['mtb_mobile_points']} {r['score_wo_bonus']} {r['total_multipliers']} {r['qso_points']} {r['ph_qsos']} {r['cw_qsos']}")

    if not REPORTS_ONLY:
        print(f"\nStarting Scoring of Results")
        score_all_qsos(context)
        print(f"Finished Scoring of Results: invalidated qsos: {s.stats['invalidated_qsos']}, duplicate qsos: {s.stats['duplicate_qsos']}, nils: {s.stats['nils']}, busteds: {s.stats['busteds']}")

        print(f"\nSaving Results in Database")
        store_rankings(CONTEST_YEAR)
        print(f"Saved Results in Database")

        print(f"\nAdding to Statistics")
        fix_stats(context)
        print(f"Added to Statictics")

        print(f"\nSaving Statistics in Database")
        save_stats(context, contest_year, s.stats)
        print(f"Saved Statistics in Database")

    
    # REMEMBER to close all the out_files
    if not REPORTS_ONLY:
        print(f"\nClosing all output files")
        for f in list(context.out_files.keys()):
            context.out_files[f].close()
        print(f"Closed all output files")
            
    generate_final_report_pdf(context, contest_year)
    print(f"Finished Generating Final Report PDF for contest year {contest_year}")
    
if __name__ == "__main__":
    import os, sys
    from datetime import datetime
    from config.config import CONTEST_YEAR
    # Get year from environment or command line
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = CONTEST_YEAR
    main(SHARED(), year)

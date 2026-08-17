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

from config.config import (
    BONUS_CALLSIGN, COUNTIES_FILE, BATCH_INPUT_DIR, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, 
    STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS,
    US_PREFIXES, CANADIAN_PREFIXES, QRZ_CALLSIGN, QRZ_PASSWORD,
    PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE,
    CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS,
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES
    )
from database import save_result
from cross_check import cross_check_all_logs
from generate_rankings import generate_rankings
from generate_final_report import generate_final_report_html

def main(contest_year: str):
    import sys
    from pathlib import Path
    # Add project to path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    input_dir = Path(f"{BATCH_INPUT_DIR}/{contest_year}")
    print(f"Processing logs from directory: {input_dir}")

    '''
    Much of the processing of log files is done with the log data in memory in a large
    data structure called results. Each log file is processed and the results are stored in this structure.
    The results structure is a list of dictionaries, one entry for each log file. 
    '''
    class SHARED:
        """
        Data and methods shared across the processing of all logs. 
        This includes reference data for counties, states, provinces, and DXCC entities, 
        as well as methods for initializing result dictionaries and tracking 
        the first QTH sent in a log.
        """
        
        def __init__(self):
            """Initialize with reference data files"""
            # Load counties, states, and provinces
            with open(COUNTIES_FILE, 'r') as f:
                self.counties = set(line.strip().upper() for line in f if line.strip())

            with open(STATES_FILE, 'r') as f:
                self.states = set(line.strip().upper() for line in f if line.strip())

            with open(PROVINCES_FILE, 'r') as f:
                self.provinces = set(line.strip().upper() for line in f if line.strip())
            
            # to get country name and ADIF number from callsign
            my_lookup_lib = LookupLib(lookuptype='countryfile', filename='./reference_data/cty.plist', username=QRZ_CALLSIGN, pwd=QRZ_PASSWORD)
            self.my_callinfo = Callinfo(my_lookup_lib)

            ## create DXCC code (same as ADIF number) to DXCC entity. Needed for DX mults
            self.dxcc_entities = [None] * 750
            with open(DXCC_ENTITIES_FILE, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.dxcc_entities[int(row[0])] = row[1].split('  ')[0]
            
            self.first_call_qth = None  # To track the sent QTH in a log for checking other QSOs against it

            self.results = []  # List to hold results for all logs processed
        
        def _init_result(self, contest_year: str) -> Dict:
            """Initialize result dictionary with standardized structure"""
            return {
                'attribs': {},  # Parsed attributes from Cabrillo header
                'year': contest_year,
                'exchange': '',     # from first QSO in this operator's log
                'category': 'NON-LA',  # 'DX', 'NON-LA', 'LA-FIXED', 'LA-ROVER'
                'dxcc_code': 0,
                'dxcc_entity': '',
                'final_score': 0,
                'qso_points': 0,
                'total_qsos': 0, # total number validated, whether dups or not
                'valid_qsos': 0, #number of qsos that are not dups and contribute to the score
                'total_multipliers': 0,
                'counties_worked': set(),
                'counties_worked_multiplier': 0,
                'states_worked': set(),
                'states_worked_multiplier': 0,
                'provinces_worked': set(),
                'provinces_worked_multiplier': 0,
                'dx_worked': set(),
                'dx_worked_multiplier': 0,
                'counties_activated': set(),
                'rover_bonus_points': 0,
                'worked_n5lcc': False,
                'num_n5lcc_contacts': 0,
                'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 0, '15': 0, '10': 0, '6': 0, '2': 0},
                'qsos_by_mode': {'Phone': 0, 'CW/Digital': 0},
                'qsos_by_hour': {i: 0 for i in range(1400,2600, 100)},  # Hour of day (1400 - 2500)
                'bands_worked': set(),
                'errors': [],
                'warnings': [],
                'is_valid': True
            }
    shared = SHARED(contest_year)
    if BATCH_INPUT_DIR:
            with open(BATCH_INPUT_DIR, 'r', encoding='utf-8', errors='replace') as f:
                cab = parse_log_file(f)
                new_result = shared.init_result(contest_year)
                new_result['attribs'] = vars(cab)
                shared.results.append(new_result)
    print(f"Processed {len(shared.results)} logs for year {contest_year}.")
    print("stop")

    # Process all logs
    # print(f"before process_batch_logs, input_dir: {input_dir}")
    # results = process_batch_logs(input_dir, contest_year)

    # results, stats = cross_check_all_logs(results, contest_year)


    #  Save results to database (valid and invalid)
    valid_count = 0
    invalid_count = 0
    saved_count = 0
    
    for result in shared.results:
        
        if result['is_valid']:
            valid_count += 1
        else:
            invalid_count += 1
            print(f"✗ {result['callsign']}: Invalid log")
            for error in result.get('errors', [])[:10]:  # Show first 10 errors
                print(f"    ERROR: {error}")
        
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

    # generate rankings from the database results
    generate_rankings(contest_year)

    # generate_final_report_html(contest_year)
    generate_final_report_html(contest_year)
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total processed: {len(results)}")
    print(f"Valid logs: {valid_count}")
    print(f"Invalid logs: {invalid_count}")
    print(f"Saved to database: {saved_count}")
    print()
    
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
    main(year)

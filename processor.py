#!/usr/bin/env python3
"""
Louisiana QSO Party - Unified Log Processor

Combines validation, preparation, and scoring into a single streamlined process.
Works in-memory without intermediate files.
Returns standardized result dictionary.

This module can be used by:
- Web upload app (single log processing)
- Batch processor (iterate through multiple logs)
"""

from pprint import pprint
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest import result
import csv

# Import your existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, 
    STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS,
    US_PREFIXES, CANADIAN_PREFIXES, QRZ_CALLSIGN, QRZ_PASSWORD,
    PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE,
    CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS,
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES
)


class UnifiedLogProcessor:
    """
    Unified processor that combines validation, preparation, and scoring.
    """
    
    def __init__(self, counties_file: Path, states_file: Path, provinces_file: Path, dxcc_entities_file: Path):
        """Initialize with reference data files"""
        # Load counties, states, and provinces
        with open(counties_file, 'r') as f:
            self.counties = set(line.strip().upper() for line in f if line.strip())

        with open(states_file, 'r') as f:
            self.states = set(line.strip().upper() for line in f if line.strip())

        with open(provinces_file, 'r') as f:
            self.provinces = set(line.strip().upper() for line in f if line.strip())
        
        # to get country name and ADIF number from callsign
        my_lookup_lib = LookupLib(lookuptype='countryfile', filename='./reference_data/cty.plist', username=QRZ_CALLSIGN, pwd=QRZ_PASSWORD)
        self.my_callinfo = Callinfo(my_lookup_lib)

        ## create DXCC code (same as ADIF number) to DXCC entity. Needed for DX mults
        self.dxcc_entities = [None] * 750
        with open(dxcc_entities_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.dxcc_entities[int(row[0])] = row[1].split('  ')[0]
        
        self.first_call_qth = None  # To track the sent QTH in a log for checking other QSOs against it
    
    def _init_result(self, contest_year: str) -> Dict:
        """Initialize result dictionary with standardized structure"""
        return {
            'year': contest_year,
            'callsign': '',
            'name': '',
            'club': '',
            'exchange': '',     # from first QSO in this operator's log
            'overlay': None,  # 'WIRES', 'TB-WIRES', 'POTA', or None
            'location_type': 'NON-LA',  # 'DX', 'NON-LA', 'LA-FIXED', 'LA-ROVER'
            'dxcc_code': 0,
            'dxcc_entity': '',
            'mode_category': 'MIXED',  # 'PHONE', 'CW/DIGITAL', 'MIXED'
            'power_level': 'LOW',  # 'QRP', 'LOW', 'HIGH'
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
            'claimed_score': 0,
            'errors': [],
            'warnings': [],
            'is_valid': True,
            'qsos': [],
            # for processing the Cabrillo header records
            '_header': {}
        }
    
    def process_log_details(self,
        contest_year: str,
        log_path: Path = None,
        form_data: Dict = None
        ) -> Dict:

        """
        Complete processing pipeline: validate → prepare → score
        
        Args:
            log_path: Path to Cabrillo log file
            form_*: Optional web form values to cross-check
        
        Returns:
            Complete result dictionary with all statistics
        """
        # Initialize result with your standardized structure
        result = self._init_result(contest_year)
        
        # Phase 1: Validate and parse
        try:
            self._validate_and_parse(log_path, result, form_data)
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Validation failed: {str(e)}")

            print(f"validate and parse failed {result['callsign']} {result['errors']}")
            return result
        
        # If validation failed, return early
        if not result['is_valid']:
            return result
        
        #############################################
        # Phase 2: Prepare QSOs (in memory)
        #############################################
        # print("BREAK")
        try:
            qso_lines = result['qsos']
            result['qsos'] = []
            self._prepare_qsos(qso_lines, result)
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f": {str(e)}")
            print(f"prepare_qsos failed {result['callsign']} {result['errors']}")
            return result        
        return result
    
    def _get_dx_info(self, callsign):
        callinfo = self.my_callinfo.get_all(callsign)
        if callinfo and callinfo['country'] in ['United States', 'Canada']:
            return None
        else:
            return [callinfo['adif'], callinfo['country']]
    
    def _validate_and_parse(self,
            log_path: Path,
            result: Dict,
            form_data: Dict) -> None:


        #############################################
        #Phase 1: Validate and parse header and QSO lines
        #############################################
        qso_modes = set()
        
        if log_path:
            with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
                self._log_line_by_line(f, result) 
        
        # Check required fields and cross-check with form data
            
        if form_data and result['is_valid']:
            if form_data['callsign'] and result['callsign']:
                if result['callsign'].upper() != form_data['callsign'].upper():
                    result['errors'].append(f"CALLSIGN mismatch: log has {result['callsign'].upper()}, form has {form_data['callsign'].upper()}")
                    result['is_valid'] = False
            else:
                result['errors'].append("Callsign is missing from log or form:")
                result['is_valid'] = False
            
            if form_data['power'] and result['power_level']:
                if result['power_level'].lower() != form_data['power'].lower():
                    result['errors'].append(f"POWER mismatch: log has {result['power_level'].upper()}, form has {form_data['power'].upper()}")
                    result['is_valid'] = False
            else:
                result['errors'].append("Power is missing from log or form:")
                result['is_valid'] = False
            
            if form_data['email'] and result['email']:
                if result['email'].lower() != form_data['email'].lower():
                    result['errors'].append(f"Email mismatch: log has {result['email'].lower()}, form has {form_data['email'].lower()}")
                    result['is_valid'] = False
            else:
                result['errors'].append("Email is missing from log or form:")
                result['is_valid'] = False

            if form_data['mode'] and result['_header']['category-mode']:
                if form_data['mode'] and result['_header']['category-mode'].lower() != form_data['mode'].lower():
                    result['errors'].append(f"Mode mismatch: log has {result['_header']['category-mode'].upper()}, form has {form_data['mode'].upper()}")
                    result['is_valid'] = False
            else:
                result['errors'].append("Mode is missing from log or form:")
                result['is_valid'] = False

            if form_data['station_type'] and result['location_type']:
                if form_data['station_type'] and result['location_type'].lower() != form_data['station_type'].lower():
                    result['errors'].append(f"Station mismatch: log has {result['location_type'].upper()}, form has {form_data['station_type'].upper()}")
                    result['is_valid'] = False
            else:
                result['errors'].append("Station is missing from log or form:")
                result['is_valid'] = False

            if form_data['overlay'] and result['overlay']:
                if form_data['station_type'] and result['overlay'].lower() != form_data['station_type'].lower():
                    result['errors'].append(f"Station mismatch: log has {result['overlay'].upper()}, form has {form_data['station_type'].upper()}")
                    result['is_valid'] = False

        # ## Done with Cabrillo Header, now do QSOs
        
        # if result['total_qsos'] == 0:
        #     result['errors'].append("No valid QSOs found in log")
        #     result['is_valid'] = False

        # if not result['is_valid']:
        #     return

    # END of _validate_and_parse

    def _log_line_by_line(self, log_path, result: Dict):
        
        has_start = False
        has_end = False
        
        for line_num, line in enumerate(log_path, 1):
            line = line.strip()
            if not line:
                continue
            
            # Check for START-OF-LOG and END-OF-LOG
            if line.startswith('START-OF-LOG:'):
                has_start = True
                continue
            if line.startswith('END-OF-LOG:'):
                has_end = True
                continue
            
            # Parse header fields (CALLSIGN, NAME, CLUB, EMAIL, CATEGORY-POWER, CATEGORY-MODE, CATEGORY-STATION, CATEGORY-OVERLAY, CLAIMED-SCORE)
            if ':' in line and not line.startswith('QSO:'):
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                result['_header'][key] = value
                
                if key == 'callsign':
                    result['callsign'] = value.upper()
                    callsign_info = self.my_callinfo.get_all(result['callsign'])
                    # if result['callsign'] == 'OM2VL':
                    #     print('halt')
                    if callsign_info and callsign_info['country'] not in ['United States', 'Canada']:  ## It's DX
                        result['dxcc_code'] = int(callsign_info['adif'])
                        result['dxcc_entity'] = self.dxcc_entities[result['dxcc_code']]
                elif key == 'name':
                    result['name'] = value
                elif key == 'club':
                    result['club'] = value
                elif key == 'category-mode':
                    result['mode_category'] = value.upper()
                elif key == 'email':
                    result['email'] = value
                elif key == 'category-power':
                    power_value = value.upper()
                    if power_value in POWER_VALUE_OPTIONS:
                        result['power_level'] = power_value
                    else:
                        result['errors'].append(f"Unrecognized power level: {value}")

                elif key == 'category-station':
                    station_value = value.upper()
                    if station_value in STATION_VALUE_OPTIONS:
                        result['location_type'] = station_value
                    else:
                        result['warnings'].append(f"Unrecognized station type: {value}")

                elif key == 'category-overlay':
                    overlay_value = value.upper()
                    if overlay_value in OVERLAY_VALUE_OPTIONS:
                        result['overlay'] = overlay_value
                    else:
                        result['warnings'].append(f"Unrecognized overlay: {value}")

                elif key == 'claimed-score':
                    try:
                        result['claimed_score'] = int(value)
                    except ValueError:
                        result['claimed_score'] = -1
                        result['warnings'].append(f"Invalid claimed score format: {value}")
                
                continue
            
            # Validate QSO lines and collect them for later processing
            if line.startswith('QSO:'):
                qso_ok = self._validate_qso_line(result, line, line_num)
                if qso_ok:
                    result['qsos'].append((line_num, line))
                    result['total_qsos'] += 1

        return
    ## END of _log_line_by_line
    
    def _validate_qso_line(self, result, line: str, line_num: int) -> Optional[bool]:

        parts = line.split()
        if len(parts) < 11:
            result['warnings'].append(f"ERROR QSO Line {line_num}: {line} Insufficient number of QSO fields")
            return False
        self.first_call_qth = parts[7]
        # Validate frequency
        try:
            freq = int(parts[1])
            band = freq_to_band(freq)
            if band == 0:
                result['warnings'].append(f"ERROR QSO Line {line_num}: {line} Invalid frequency {freq} kHz")
                return False
        except (ValueError, IndexError):
            result['warnings'].append(f"ERROR QSO Line {line_num}: {line} Invalid frequency format")
            return False
        
        # Validate mode
        mode = parts[2]
        if mode not in PHONE_MODES and mode not in CW_DIGITAL_MODES and mode != 'MIXED':
            result['warnings'].append(f"ERROR QSO at line {line_num}: {line} Unrecognized mode {mode}")
            return False
            
        if result['mode_category'] == 'SSB' and mode not in PHONE_MODES and mode != 'MIXED':
            result['warnings'].append(f"ERROR QSO at line {line_num}: {line} Mode {mode} does not match header CATEGORY-MODE {result['mode_category']}")
            return False
            
        if result['mode_category'] == 'CW/DIGITAL' and mode not in CW_DIGITAL_MODES and mode != 'MIXED':
            result['warnings'].append(f"ERROR QSO at line {line_num}: {line} Mode {mode} does not match header CATEGORY-MODE {result['mode_category']}")
            return False
   
        return True
    
    def _prepare_qsos(self, qso_lines, result: Dict) -> List[Dict]:
        """Phase 2: Prepare QSOs (convert freq, expand multi-county, etc.)"""
        
        for line_num, qso_line in qso_lines:
            parts = qso_line.split()
            if len(parts) < 11:
                print("break qso loop")
                continue
            
            # pprint(f"Processing QSO Line {line_num}: {parts}")
            # print("BREAKPOINT")
            # Parse QSO fields
            freq_khz = int(parts[1])
            mode = parts[2]
            date = parts[3]
            time = parts[4]
            sent_call = parts[5].split('/')[0]  # Remove mobile indicator
            sent_rst = parts[6]
            sent_qth = parts[7]
            rcvd_call = parts[8].split('/')[0]  # Remove mobile indicator
            rcvd_rst = parts[9]
            rcvd_qth = parts[10]
            
            # Convert frequency to band
            band = str(freq_to_band(freq_khz))
            
            # Normalize mode
            if mode in PHONE_MODES:
                mode_cat = 'Phone'
            else:
                mode_cat = 'CW/Digital'  
            new_qso = {
                'band': band,
                'mode': mode,
                'mode_category': mode_cat,
                'date': date,
                'time': time,
                'sent_call': sent_call,
                'sent_rst': sent_rst,
                'sent_qth': sent_qth,
                'rcvd_call': rcvd_call,
                'rcvd_rst': rcvd_rst,
                'rcvd_qth': rcvd_qth,
                'line_num': line_num,
                'xcheck': ''
            }    
            result['qsos'].append(new_qso)
        
        # Get info that is NOT specific to each QSO but is needed for scoring (e.g., location type)
        # Determine location type from prepared QSOs
        result['location_type'] = self._determine_location_type(result)
        
    
    ## END of prepare_qsos
    
    # get location type of a QSO's sender
    def _determine_location_type(self, result: Dict) -> str:
        """Determine location type from QSOs"""
        
        initial_qso = True

        for qso in result['qsos']:
            sent_qth = qso['sent_qth'].replace('DX', '')
            sent_call = qso['sent_call']

            if initial_qso:
                initial_qso = False
                result['exchange'] = sent_qth
            
            
            # Check if DX
            callinfo = self.my_callinfo.get_all(sent_call)
            if callinfo and callinfo['country'] not in ['United States', 'Canada']:
                return 'DX'
            
            # Check if non-LA
            if (sent_qth in self.states) or (sent_qth in self.provinces):
                return 'NON-LA'
        
        # Determine if fixed or rover
        station = result['location_type']  # Get station type
        
        if station in ('MOBILE', 'ROVER'):
            return 'LA-ROVER'
        elif station in ('FIXED', 'PORTABLE'):
            return 'LA-FIXED'
        else:
            return 'LA-FIXED'
    
    
## Utility functions


    def _is_dx_callsign(self, call: str) -> bool:
        """Check if callsign is DX (not US or VE)"""
        prefix = self._get_callsign_prefix(call)
        if not prefix:
            return False
        
        # US callsigns
        if prefix[0] in ('K', 'N', 'W'):
            return False
        if prefix in US_PREFIXES:
            return False
        
        # Canadian callsigns
        if prefix in CANADIAN_PREFIXES:
            return False
        
        return True
    
    def _get_callsign_prefix(self, call: str) -> str:
        """Extract prefix from callsign"""
        for i, char in enumerate(call):
            if char.isdigit():
                if i < 1:
                    return call[:1]
                else:
                    return call[:i]
        return call
    
## End of UnifiedLogProcessor class

# Convenience functions for single log processing in WEB app ONLY (not used for batch processing)
def process_single_log(
        contest_year: str,
        log_path: Path = None,
        form_data: Dict = None,
        log_content: str = None,
        counties_file: Path = Path(COUNTIES_FILE),
        states_file: Path = Path(STATES_FILE),
        provinces_file: Path = Path(PROVINCES_FILE),
        dxcc_entities_file: Path = Path(DXCC_ENTITIES_FILE)) -> Dict:
    """
    Process a single log file (for web uploads ONLY).
    
    Args:
        log_path: Path to log file
        counties_file: Path to county abbreviations (optional, uses default)
        state_province_file: Path to state/province abbreviations (optional, uses default)
        **form_data: Optional form fields (email, mode, power, station, overlay)
    
    Returns:
        Result dictionary
    """
    processor = UnifiedLogProcessor(counties_file, states_file, provinces_file, dxcc_entities_file)

    return processor.process_log_details(
        contest_year,
        log_path,
        form_data
        )

def print_result(result):
    """Utility function to print result in a readable format"""
    print(f"Callsign: {result['callsign']} Errors: {len(result['errors'])}  Warnings: {len(result['warnings'])}")
    print(sorted(result['states_worked']))
    print(sorted(result['provinces_worked']))
    print(sorted(result['counties_worked']))
    print(sorted(result['dx_worked']))
    print(f"Number states worked: {len(result['states_worked'])}")
    print(f"Location Type: {result['location_type']}")
    print(f"Mode Category: {result['mode_category']}")
    print(f"Power Level: {result['power_level']}")
    print(f"Overlay: {result['overlay']}")
    print(f"Final Score: {result['final_score']} (Claimed: {result['claimed_score']})")
    print(f"Total QSOs: {result['total_qsos']}  Valid QSOs: {result['valid_qsos']}  QSO Points: {result['qso_points']}")
    print(f"Total Multipliers: {result['total_multipliers']} (Counties: {result['counties_worked_multiplier']}, States: {result['states_worked_multiplier']}, Provinces: {result['provinces_worked_multiplier']}, DX: {result['dx_worked_multiplier']})")
    if result['location_type'] == 'LA_ROVER':
        print(f"Rover Bonus Points: {result['rover_bonus_points']} for activating counties: {', '.join(result['counties_activated'])}")
    if result['worked_n5lcc']:
        print(f"N5LCC Contacts: {result['num_n5lcc_contacts']} (Bonus points applied)")
    if result['warnings']:
        if len(result['warnings']) < 10:
            print("Warnings:")
            for w in result['warnings']:
                print(f"{w}")
        else:
            q = 0
            m = 0
            for w in result['warnings']:
                if w.startswith("Duplicate Q"):
                    q += 1
                else:
                    m += 1
            print(f"Warnings: {q} duplicate QSOs")

    if result['errors'] and result['callsign']:
        print("Errors:")
        for e in result['errors']:
            print(f"{e}")

def process_batch_logs(log_dir: Path, contest_year: str) -> Dict:
    """
    Process multiple log files (for batch processing).
    
    Args:
        log_dir: Directory containing log files
        counties_file: Path to county abbreviations (optional, uses default)
        state_province_file: Path to state/province abbreviations (optional, uses default)
    
    Returns:
        List of result dictionaries
    """
    
    processor = UnifiedLogProcessor(COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE)

    results = []
    # print(f"ready to process_log_details for logs in {log_dir}")
    for log_path in log_dir.glob('*.log'):
        result = processor.process_log_details(contest_year, log_path)
        # print(f"Finished processing {log_path.name}: Score {result['final_score']} Mult: {result['total_multipliers']} qso points: Errors: {len(result['errors'])} Warnings: {len(result['warnings'])}")
        # print_result(result)
        results.append(result)
    
    return results

def freq_to_band(freq_khz: int) -> int:
    """
    Convert frequency in kHz to band in meters.
    
    Args:
        freq_khz: Frequency in kHz
    
    Returns:
        Band in meters (e.g., 20, 40, 80) or None if not in a valid band
    """
    for band, (min_freq, max_freq) in BAND_RANGES.items():
        if min_freq <= freq_khz <= max_freq:
            return band
    return None


if __name__ == "__main__":
    print("LAQP Unified Log Processor")
    print("This module should be imported, not run directly.")
    print()
    print("For web upload: from processor import process_single_log")
    print("For batch: from processor import process_batch_logs")

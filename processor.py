#!/usr/bin/env python3
"""
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
from batch import shared as s

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
   
"""
Get some general information first

"""

    





def validate_and_parse() -> None:




        
    

    # ## Done with Cabrillo Header, now do QSOs
    
    # if result['total_qsos'] == 0:
    #     result['errors'].append("No valid QSOs found in log")
    #     result['is_valid'] = False

    # if not result['is_valid']:
    #     return

# END of _validate_and_parse


def validate_qso_line(result, line: str, line_num: int) -> Optional[bool]:

    parts = line.split()
    if len(parts) < 11:
        result['warnings'].append(f"ERROR QSO Line {line_num}: {line} Insufficient number of QSO fields")
        return False
    s.first_call_qth = parts[7]
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

def prepare_qsos(qso_lines, result: Dict) -> List[Dict]:
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
    result['location_type'] = s._determine_location_type(result)
    

## END of prepare_qsos







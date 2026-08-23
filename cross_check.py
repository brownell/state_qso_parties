#!/usr/bin/env python3
"""
Louisiana QSO Party - Log Cross-Checking Module

This module cross-checks all submitted logs to validate QSOs by finding
reciprocal contacts in other logs. Invalid QSOs are marked and warnings
are added. Final scores are recalculated using only valid QSOs.

Cross-check classifications:
- CONFIRMED: QSO found in both logs with matching details
- NIL: QSO not found in other station's log
- BUSTED: Callsign error detected via fuzzy matching
- EXCHANGE_ERROR: QSO exists but exchange information is wrong
- UNIQUE: Callsign not found in any submitted log (no penalty)
"""

import math
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from cabrillo import QSO
from config.config import CONTEST_YEAR, CW_DIGITAL_QSO_POINTS, EXTRA_BONUS_POINTS, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE, DATABASE_FILE, TIME_WINDOW_MINUTES, ENABLE_FUZZY_MATCHING, MAX_EDIT_DISTANCE, BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS, US_PREFIXES, CANADIAN_PREFIXES,QRZ_CALLSIGN, QRZ_PASSWORD, PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE, CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES


def cross_check(s):

    '''
        We use the cabrillo python package to check for duplicate QSOs and to cross-check the QSOs in each log against the other logs.  The Cabrillo package has a QSO.match() function that checks for matching QSOs in two logs.  It returns True if the QSOs match, False if they do not match, and None if the QSO is not found in the other log.
    '''

    
    if len(s.results) < 1:
        return False
    
    for result in s.results:
        print(f"cross-checking {result['callsign']}")
        for qso_i, qso in enumerate(result['cab'].qso):
            # Skip invalid QSOs
            if not qso.valid:
                result["errors"].append(f"qso with {qso.dx_call} was not valid")
                print(f"qso with {qso.dx_call} was not valid")
                continue  

            # receiving call did not submit a log - UNIQUE
            if qso.dx_call not in s.all_callsigns:
                print(f"for qso {vars(qso)} {qso.dx_call} did not submit a log")
                continue

            else:
                # from the qso_index_dict, get all POTENTIAL matches, based
                # on callsign, exchange, mode, and band
                potential_matches = s.qso_index_dict[s._generate_index_key(qso, False)]

                if len(potential_matches) == 0:
                    # this should not be possible.
                    print(f"***  IMPOSSIBLE: callsign {qso.dx_call} was in all_callsigns, but nothing from qso_index_dict")
                    continue

                for p in potential_matches:
                    match = QSO.match_against(qso, p)
                    if  match:  # qso cross-checked
                        break
                if not match:
                    qso.valid = False
                    result['qso_data'][qso_i]["valid"] = False
                    result["warnings"].append(f"qso found no match with {qso.dx_call} even though dx did submit a log")
                    print(f"qso {vars(qso)} found no match with {qso.dx_call} even though dx did submit a log")
       
    return True


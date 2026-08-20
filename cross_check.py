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
from batch import shared as s
from config.config import CONTEST_YEAR, CW_DIGITAL_QSO_POINTS, EXTRA_BONUS_POINTS, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE, DATABASE_FILE, TIME_WINDOW_MINUTES, ENABLE_FUZZY_MATCHING, MAX_EDIT_DISTANCE, BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS, US_PREFIXES, CANADIAN_PREFIXES,QRZ_CALLSIGN, QRZ_PASSWORD, PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE, CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES


def cross_check():

    '''
        We use the cabrillo python package to check for duplicate QSOs and to cross-check the QSOs in each log against the other logs.  The Cabrillo package has a QSO.match() function that checks for matching QSOs in two logs.  It returns True if the QSOs match, False if they do not match, and None if the QSO is not found in the other log.
    '''
    
    for results_index in range(len(s.results)):
        for qso_index in range(len(s.results[results_index]['cab'].qso)):
            qso = s.results[results_index]['cab'].qso[qso_index]
            if not qso.valid:
                continue  # Skip invalid QSOs
            # see if this dx_call is in the qso_index
            qso = s.qso_index.get(s.results[i].cab.callsign, [])
        if not qso:
            return False
    
        else:
            match = QSO.match(s.results[i].cab, qso)
            if match == True:  # qso cross-checked and scored
                score
                return False

        '''
        If the QSO is valid, then we score it, first checking whether it is a duplicate.
        
        There are two types of duplicates: a point dup and a mult dup.  A point dup is when all of band/mode/rcvd_call are the same, in which case it should not count for points or multipliers.  A mult dup is when a QSO is a duplicate for multiplier purposes (same band/mode/rcvd_qth) but not a point dup (different rcvd_call).  These get qso points (if otherwise valid) but not multipliers.
        '''
        
        return True

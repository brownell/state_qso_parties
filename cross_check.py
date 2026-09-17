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
from datetime import datetime
from cabrillo import QSO

from cabrillo.qso import frequency_to_band_m
from score_a_qso import score_a_qso
from config.config import CONTEST_YEAR, CW_DIGITAL_QSO_POINTS, EXTRA_BONUS_POINTS, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE, DATABASE_FILE, TIME_WINDOW_MINUTES, ENABLE_FUZZY_MATCHING, MAX_EDIT_DISTANCE, BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS, US_PREFIXES, CANADIAN_PREFIXES,QRZ_CALLSIGN, QRZ_PASSWORD, PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE, CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES


def cross_check(s):

    '''
        We use the cabrillo python package to check for duplicate QSOs and to cross-check the QSOs in each log against the other logs.  The Cabrillo package has a QSO.match() function that checks for matching QSOs in two logs.  It returns True if the QSOs match, False if they do not match, and None if the QSO is not found in the other log.
    '''
    if len(s.results) < 1:
        return False
    c = s.stats
    for result in s.results:
        dup = {
            'qsos': [],
            'mults': []
        }
        for qso_i, qso in enumerate(result['cab'].qso):
            print(f"result {result['cab'].callsign} qso {qso_i} de {qso.de_call} dx {qso.dx_call} ")
            # if result['callsign'].upper() == 'AA0AW' and qso.dx_call.upper() == 'N5OT':
            #     print('BREAK')
            result['total_qsos'] += 1
            # Skip invalid QSOs
            if qso.valid:
                result['valid_qsos'] += 1
            else:
                result["errors"].append(f"qso from {qso.de_call} to {qso.dx_call} was not valid")
                print(f"qso from {qso.de_call} to {qso.dx_call} was not valid")
                continue  
            # receiving call did not submit a log - UNIQUE
            if qso.dx_call.upper() not in s.all_callsigns:
                # this is a UNIQUE
                c['uniques'] += 1
                s.out_files['uniques_file'].write(f"call from {qso.de_call} to {qso.dx_call}: latter did not submit a log")
                print(f"call from {qso.de_call} to {qso.dx_call}: latter did not submit a log")
                continue
            else:
                if check_it(s, result, qso):
                    score_a_qso(s, result, qso, dup)
                else:
                    result['valid_qsos'] -= 1
                    continue
                
def check_it(s, result, qso):
    # from the qso_index_dict, get all POTENTIAL matches, based
    # on callsign, exchange, mode, and band
    c = s.stats
    k = s._generate_index_key(qso, qso.dx_call, True) # from the dx POV
    # print(f"k: {k}, his call {qso.dx_call}  my call {qso.de_call}")
    potential_matches = s.qso_index_dict[k]
    if len(potential_matches) == 0:
        s.stats['dx_log_de_missing'] += 1
        s.stats['nils'] += 1
        s.stats['nil_calls'].append([qso.de_call, qso.dx_call])
        qso.valid = False
        s.out_files['nils_file'].write(f"qso from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H")}Z")
        result['warnings'].append(f"qso from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H")}Z\n")
        print(f"qso from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H")}Z")
        return False
    else:    
        for p in potential_matches:
            match_made = False
            match = QSO.match_against(qso, p)
            if match:  # see if another matches
                # print("BREAK")
                match_made = True
                break
            else:
                continue
        if match_made:
            return True
        else:
            '''  NONE of the potential_matches matches, so this is a case where 
                 the dx_call in the qso DID submit a log (because in s.all_callsigns)
                 but no matching qso was found in the log of the dx_call'''
            # print('BREAK')
            c['busteds'] += 1
            c['busted_calls'].append([qso.de_call, qso.dx_call])
            qso.valid = False
            s.out_files['busteds_file'].write(f"qso from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H")}Z")
            result["warnings"].append(f"qso from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H")}Z\n")
            print(f"qso from/to {qso.de_call}/{qso.dx_call} exchs:{qso.de_exch[1]}/{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H")}Z")
            return False
    
                
    print(f"end of cross-check")
    print(f"stats:\n{s.stats}")
    print(f"STOP")
    return True


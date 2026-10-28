#!/usr/bin/env python3
"""
Texas QSO Party - Log Cross-Checking Module

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

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
import copy
from cabrillo import QSO
from cabrillo.qso import frequency_to_band_m
from utilities import generate_index_key, get_near_match, writefile, capture_mobile, get_dxcc, qso_nil, qso_busted
from config.config_txqp import CONTEST_TIMES

def cross_check(s):
    '''
        We use the cabrillo python package "match_against" to check for duplicate QSOs and to cross-check the QSOs in each log against the other logs.  The Cabrillo package has a QSO.match() function that checks for matching QSOs in two logs.  It returns True if the QSOs match, False if they do not match, and None if the QSO is not found in the other log.'''
    if len(s.results) < 1:
        return False
    print(f"START cross-check")
    c = s.stats
    for result in s.results:
        dup = {
            'qsos': [],
            'num_qso': 0,
        }
        for qso in result['cab'].qso:
            # this is to account for qsos that were already matched when they were the DX qso
            # and it was observed they were valid and should be scored
            qso_dup = make_dup(s, result, qso)

            if qso_dup in dup['qsos']:
                if qso.valid:
                    result['valid_qsos'] -= 1
                    s.stats['valid_qsos'] -= 1
                    s.stats['duplicate_qsos'] += 1
                    temp = f"Duplicate QSO: "
                    writefile(s, result, qso, temp, ['errors'])
                    qso.valid = False
                result['dup_qsos'] += 1
                dup['num_qso'] += 1
                continue
            else:
                dup['qsos'].append(qso_dup)

            
            if "Mobile" in result['cab'].category and "/" in qso.de_exch[1]:
                # op should have made this two qsos but we do it for them
                # mobile put multiple counties in the same QSO separated by "/"
                writefile(s, result, qso, 'Multi-county exchange', ['warnings'])
                s.stats['multi_county_exchanges'] += 1
                counties = qso.de_exch[1].split('/')
                qso.de_exch[1] = counties[0]
                for c in counties[1:]:
                    new_qso = copy.deepcopy(qso)
                    new_qso.de_call = c
                    result['cab'].qso.append(new_qso)
            if qso.dx_call not in list(s.all_callsigns.keys()):
                # this is a UNIQUE - he gets the points
                result['uniques'] += 1
                c['uniques'] += 1
                writefile(s, result, qso, 'No log from receiver', ['uniques'])
                continue


            # this is to account for qsos that were already matched when they were the DX qso
            # and it was observed they were valid and should be scored
            if getattr(qso, 'points', False):
                continue

            dx_result = s.results[s.all_callsigns[qso.dx_call]]
            if not check_it(s, result, dx_result, qso):
                if qso.valid:
                    qso.valid = False
                    result['valid_qsos'] -= 1


def check_it(s, result, dx_result, qso):
    # from the qso_index_dict, get all POTENTIAL matches, based
    # on callsign, exchange, mode, and band
    c = s.stats
    if not (qso.date >= CONTEST_TIMES[0]['start'] and 
       (qso.date <= CONTEST_TIMES[0]['end'] )) or (
        qso.date >= CONTEST_TIMES[1]['start'] and 
       (qso.date <= CONTEST_TIMES[1]['end'] )
       ):
        qso.valid = False
        s.stats['valid_qsos'] -= 1
        writefile(s, result, qso, 'BAD DATE/TIME: QSO time not within contest times:', ['errors'])
    k = generate_index_key(s, qso, qso.dx_call, True) # from the dx POV

    # see if there are any PERFECT matches (except time)
    potential_matches = s.qso_index_dict[k]
    if len(potential_matches) == 0:
        match = get_near_match(s, qso, result, dx_result)
        if match != None:
            ''' the near_match (if one) is a receiver qso that does not
                have all the correct information, so we give the points
                to the sender, but mark the receiver's qso invalid'''
            capture_mobile(s, result, dx_result, qso, match)
            return True
    else:
        for p in potential_matches:
            # using Cabrillo package function
            # NOT checking time match and not checking exchanges
            match = QSO.match_against(qso, p, -1, False) and qso.dx_exch[1] == p.de_exch[1]
            if match:
                capture_mobile(s, result, dx_result, qso, p)
                return True
            ''' Check whether it is "close enough"
            '''
        match = get_near_match(s, qso, result, dx_result)
        if match != None:
            capture_mobile(s, result, dx_result, qso, p)
            return True
        
    '''There was not a full or near match in the qsos of the
        receiver, so this is a NIL'''
    qso_nil(s, qso, result)
    return False

def make_dup(s, r, qso):
    temp = "_".join([qso.de_call, qso.dx_call, qso.de_exch[1].upper(), qso.dx_exch[1].upper(), frequency_to_band_m(qso.freq), qso.mo.upper()])
    return temp
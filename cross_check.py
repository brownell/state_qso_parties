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
from cabrillo import QSO
from cabrillo.qso import frequency_to_band_m
from score_qsos import score_a_qso, score_an_operator
from utilities import generate_index_key, debug_print, get_fuzzies, test

def cross_check(s):
    '''
        We use the cabrillo python package "match_against" to check for duplicate QSOs and to cross-check the QSOs in each log against the other logs.  The Cabrillo package has a QSO.match() function that checks for matching QSOs in two logs.  It returns True if the QSOs match, False if they do not match, and None if the QSO is not found in the other log.'''
    if len(s.results) < 1:
        return False
    print(f"START cross-check")
    c = s.stats
    for result in s.results:
        if result['callsign'] == 'F4EUG':
            print('AD4EB')
        dup = {
            'qsos': [],
            'num_qso': 0,
            'mults': [],
            'num_mult': 0
        }
        num_qsos = 0
        valid_qsos_processed = 0
        calls_to_score_a_q = 0
        bad_xchk = []
        for qso_i, qso in enumerate(result['cab'].qso):
            num_qsos += 1
            # print(f"result {result['cab'].callsign} qso {qso_i} de {qso.de_call} dx {qso.dx_call} ")
            # Skip invalid QSOs
            if not qso.valid:
                result['other_bad_qsos'] += 1
                result["errors"].append(f"INVALID QSO: from {qso.de_call} to {qso.dx_call} ")
                continue
            # receiving call did not submit a log - UNIQUE
            if qso.dx_call not in list(s.all_callsigns.keys()):
                # this is a UNIQUE - he gets the points
                score_a_qso(s, result, qso, dup)
                valid_qsos_processed += 1
                calls_to_score_a_q += 1
                c['uniques'] += 1
                s.out_files['uniques'].write(f"call from {qso.de_call} to {qso.dx_call}: latter did not submit a log\n")
                # print(f"UNIQUE CALL from {qso.de_call} to {qso.dx_call}: latter did not submit a log")
                continue
            else:
                if check_it(s, result, qso):
                    score_a_qso(s, result, qso, dup)
                    # print(f"AFTER SCORE dx {qso.dx_call} total_qsos: {result['total_qsos']} valid: {result['valid_qsos']} hours {sum(result['qsos_by_hour'])}")
                    calls_to_score_a_q += 1
                    valid_qsos_processed += 1
                    # print(f"AFTER SCORE dx {qso.dx_call}: total_qsos: {result['total_qsos']} valid: {result['valid_qsos']} hours {sum(result['qsos_by_hour'])}")

        status= score_an_operator(s, result)
        

        # debug_print(s, result, "", False)
    # print(f"*** END of cross-check for {result['callsign']}")
                
def check_it(s, result, qso):
    # from the qso_index_dict, get all POTENTIAL matches, based
    # on callsign, exchange, mode, and band
    c = s.stats
    #=======================
    #=======================
    # TODO check that the time is within the contest windows
    #=======================
    #=======================
    k = generate_index_key(s, qso, qso.dx_call, True) # from the dx POV
    # print(f"k: {k}, his call {qso.dx_call}  my call {qso.de_call}")

    # see if there are any PERFECT matches (except time)
    potential_matches = s.qso_index_dict[k]
    if qso.dx_call == 'K4AMC':
        pass
    if len(potential_matches) == 0:
        # see if there any potential_fuzzy_matches
        # find the qsos for the dx_call
        try:
            dx_cab = s.results[s.all_callsigns[qso.dx_call]]['cab']
        except Exception as e:
            print(f"not in all_callsigns: {qso.dx_call}")
            return False
        match= get_fuzzies(qso, dx_cab.qso)
        # We found a fuzzy match between de's de_call and dx's dx_call
        if len(match) > 0:
            # we have a fuzzy match
            match_made = True
        else:
            qso.valid = False
            result['nils'] += 1
            result["errors"].append(f'''NIL QSO from-to {qso.de_call}-{qso.dx_call} exchs:{qso.de_exch[1]}-{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H%M")}Z\n''')
            s.stats['dx_log_de_missing'] += 1
            s.stats['nils'] += 1
            s.stats['nil_calls'].append([qso.de_call, qso.dx_call])
            s.out_files['nils'].write(f'''NIL from-to {qso.de_call}-{qso.dx_call} exchs:{qso.de_exch[1]}-{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H%M")}Z\n''')
            return False
    else:
        for p in potential_matches:
            match_made = False
            match = QSO.match_against(qso, p)
            if match:  # see if another matches
                # print("BREAK")
                match_made = True
                break
        if match_made:
            return True
        else:
            '''Now see if there is a fuzzy match since there was no 
                direct match'''
            try:
                dx_cab = s.results[s.all_callsigns[qso.dx_call]]['cab']
            except Exception as e:
                print(f"not in all_callsigns: {qso.dx_call}")
                return False
            match = get_fuzzies(qso, dx_cab.qso)
                # We found a fuzzy match between de's de_call and dx's dx_call
            if len(match) > 0:
                return True
            '''  NONE of the potential_matches matches and there 
                 no fuzzy match, so this is a case where 
                 the dx_call in the qso DID submit a log (because 
                 has callsign key and index in s.all_callsigns)
                 but no matching qso was found in the log of the dx_call'''
            # print('BREAK')
            result['busteds'] += 1
            result['busted_calls'].append([qso.de_call, qso.dx_call])
            c['busteds'] += 1
            c['busted_calls'].append([qso.de_call, qso.dx_call])
            qso.valid = False
            s.out_files['busteds'].write(f'''BUSTED from-to {qso.de_call}-{qso.dx_call} exchs:{qso.de_exch[1]}-{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H%M")}Z\n''')
            result["errors"].append(f'''BUSTED QSO to {qso.dx_call} exchs:{qso.de_exch[1]}-{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H%M")}Z\n''')
            return False


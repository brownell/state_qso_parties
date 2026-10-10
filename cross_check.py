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
from utilities import generate_index_key, debug_print, get_fuzzy_match
from config.config_txqp import CONTEST_TIMES

def cross_check(s):
    '''
        We use the cabrillo python package "match_against" to check for duplicate QSOs and to cross-check the QSOs in each log against the other logs.  The Cabrillo package has a QSO.match() function that checks for matching QSOs in two logs.  It returns True if the QSOs match, False if they do not match, and None if the QSO is not found in the other log.'''
    if len(s.results) < 1:
        return False
    print(f"START cross-check")
    c = s.stats
    for result in s.results:
        for qso in result['cab'].qso:
            # receiving call did not submit a log - UNIQUE
            if qso.dx_call not in list(s.all_callsigns.keys()):
                # this is a UNIQUE - he gets the points
                result['uniques'] += 1
                c['uniques'] += 1
                s.out_files['uniques'].write(f"call from {qso.de_call} to {qso.dx_call}: latter did not submit a log\n")
                # print(f"UNIQUE CALL from {qso.de_call} to {qso.dx_call}: latter did not submit a log")
                continue
            else:
                if "Mobile" in result['cab'].category and "/" in qso.de_exch[1]:
                    counties = qso.de_exch[1].split('/')
                    qso.de_exch[1] = counties[0]
                    for c in counties[1:]:
                        new_qso = qso
                        new_qso.de_call = c
                        result['cab'].qso.append(new_qso)
                if not check_it(s, result, qso):
                    qso.valid = False

def check_it(s, result, qso):
    # from the qso_index_dict, get all POTENTIAL matches, based
    # on callsign, exchange, mode, and band
    c = s.stats
    if not (qso.date >= CONTEST_TIMES[0]['start'] and 
       (qso.date <= CONTEST_TIMES[0]['end'] )) or (
        qso.date >= CONTEST_TIMES[1]['start'] and 
       (qso.date <= CONTEST_TIMES[1]['end'] )
       ):
        qso.valid = False

    k = generate_index_key(s, qso, qso.dx_call, True) # from the dx POV

    # see if there are any PERFECT matches (except time)
    potential_matches = s.qso_index_dict[k]
    if len(potential_matches) == 0:
        # We found a fuzzy match between de's de_call and dx's dx_call
        if get_fuzzy_match(qso, result['cab'].qso):
            # we have a fuzzy match
            return True
        else:
            # NIL because dx_call has a log, but matching qso not in it
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
            # using Cabrillo package function
            # NOT checking time match and not checking exchanges
            match = QSO.match_against(qso, p, -1, False) and qso.dx_exch[1] == p.de_exch[1]
            if match:  
                return True
            '''Was not a PERFECT match BUT this op still may
                get points and we may have to invalidate the
                receiver's QSO. If the receiver's dx_call 
                is not exactly the
                same as the sender's de_call, we see if they
                are a "fuzzy" match, meaning that the receiver's
                dx_call must all the characters in the sender's
                de_call except it can be missing two characters.
                And the characters that are present must be in 
                the same order
                '''
            # fuzzy callsign first
            if get_fuzzy_match(qso, result['cab'].qso):
                return True
            '''  NONE of the potential_matches matches and there 
                 no fuzzy match, so this is a case where 
                 the dx_call in the qso DID submit a log (because 
                 has callsign key and index in s.all_callsigns)
                 but no matching qso was found in the log of the dx_call'''
            result['busteds'] += 1
            result['busted_calls'].append([qso.de_call, qso.dx_call])
            c['busteds'] += 1
            c['busted_calls'].append([qso.de_call, qso.dx_call])
            qso.valid = False
            s.out_files['busteds'].write(f'''BUSTED from-to {qso.de_call}-{qso.dx_call} exchs:{qso.de_exch[1]}-{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H%M")}Z\n''')
            result["errors"].append(f'''BUSTED QSO to {qso.dx_call} exchs:{qso.de_exch[1]}-{qso.dx_exch[1]} mode:{qso.mo} band:{frequency_to_band_m(qso.freq)} Sept {qso.date.strftime("%d")}th {qso.date.strftime("%H%M")}Z\n''')
            return False
    return False

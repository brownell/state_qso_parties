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
from config.config import CONTEST_YEAR, CW_DIGITAL_QSO_POINTS, EXTRA_BONUS_POINTS, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE, DATABASE_FILE, TIME_WINDOW_MINUTES, ENABLE_FUZZY_MATCHING, MAX_EDIT_DISTANCE, BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS, US_PREFIXES, CANADIAN_PREFIXES,QRZ_CALLSIGN, QRZ_PASSWORD, PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE, CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES


printout = False # printout
all_callsigns = set() # populated in cross_check_all_logs

def score_qsos(result: Dict, contest_year: str) -> None:
    """Phase 3: Score QSOs and calculate multipliers"""
    global all_callsigns, processor
    # A mult dup is when a QSO is a duplicate for multiplier purposes (same band/mode/rcvd_qth) but not a point dup (different rcvd_call).  These get qso points (if otherwise valid) but not  multipliers.  
    # A qso dup is when all of band/mode/rcvd_call are the same, in which case it should not count for points or multipliers.
    
    qso_dups = []
    mult_dups = []
    for qso in result['qsos']:
        # Skip QSOs flagged by cross-checking
        if qso.get('xcheck', '') != '':
            continue  # Error from cross-checking, skip for scoring
    
        band = qso['band']
        mode_cat = qso['mode_category']
        sent_call = qso['sent_call']
        rcvd_call = qso['rcvd_call']
        sent_qth = qso['sent_qth']

        ## if rcvd_call is a DX, then replace rcvd_qth with DXCC code (ADIF number as string)
        try:
            dx_rcvd_qth  = processor.my_callinfo.get_all(rcvd_call)
        except Exception as e:
            result['warnings'].append(f"ERROR QSO: cannot get rcvd_qth for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")
            print(f"Exception {e} sender {result['callsign']} cannot get rcvd_qth for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")

        try:            
            if dx_rcvd_qth and ((dx_rcvd_qth['country'] not in ['United States', 'Canada'])): # working DX station
                rcvd_qth = processor.dxcc_entities[int(dx_rcvd_qth['adif'])]
                dx_rcvd_qth['dxcc_entity'] = rcvd_qth
                # print(f"rcvd_qth is dx: sender sent_qth {sent_qth} receiver {rcvd_qth}")
            
                ## make sure this is not DX to DX
                if len(result['dxcc_entity']) > 0: # call from one DX to another -> invalid
                    result['warnings'].append(f"DUPLICATE QSO line one DX station to another {qso['line_num']} band: {band} mode: {mode_cat} sender: {sent_call} sender QTH: {result['dxcc_entity']} remote op: {rcvd_call} remote QTH: {rcvd_qth}")
                    continue
            else:
                rcvd_qth = qso['rcvd_qth']
                dx_rcvd_qth = None
        except Exception as e:
            rcvd_qth = qso['rcvd_qth']
            dx_rcvd_qth = None
            result['warnings'].append(f"ERROR QSO: cannot determine if rcvd_qth is DX for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")
            print(f"Exception {e} sender {result['callsign']} cannot determine if rcvd_qth is DX for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")

        # NOT DX - ROVER gets a qso_check that includes his QTH because he can call same
        # station multiple toimes from different counties
        if result['location_type'] == "LA-ROVER":
                qso_check = band + mode_cat + sent_qth + rcvd_call
                if sent_qth not in result['counties_activated']:
                    result['counties_activated'].add(sent_qth)
        else: ## MUST be LA Fixed or State or Province
            qso_check = band + mode_cat + rcvd_call

        if result['location_type'] == "LA-FIXED" and sent_qth not in result['counties_activated']:
            result['counties_activated'].add(sent_qth)
                
        if qso_check in qso_dups:
            result['warnings'].append(f"DUPLICATE QSO line {qso['line_num']} band/mode/call worked:  {band}, {mode_cat}, {rcvd_call}")
        else:  ## not a duplicate for points, so get points
            result['valid_qsos'] += 1
            # print(f"NOT DUP QSO line {qso['line_num']} band/mode/call worked:  {band}/{mode_cat}/{rcvd_call}")
            # print(f"valid_qsos {result['valid_qsos']} qso_check {qso_check} band/sentqth/rcvd_call: {qso['band']} {qso['rcvd_qth']} {qso['rcvd_call']}")
            qso_dups.append(qso_check)

        # Track bands worked and QSO by band (for display only, does not impact score)
        result['bands_worked'].add(band)
        result['qsos_by_band'][band] += 1

        # Track qsos by hour (2-hour blocks)
        try:
            temp = int(qso['time'][:2] + "00")
            if temp < 999 or temp > 2600:
                temp = 2400
            result['qsos_by_hour'][temp] += 1
        except Exception as e:
            print(f"Error tying to get the QSO time {e}")
            result['warnings'].append(f"Bad time value on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_qth}")
            continue
        
        # Award points
        if mode_cat == 'Phone':
            result['qso_points'] += PHONE_QSO_POINTS
            # print(f"qso_points {result['qso_points']} total_qsos {result['total_qsos']} valid_qsos {result['valid_qsos']}")
            result['qsos_by_mode']['Phone'] += 1
        else:  # CW/Digital
            result['qso_points'] += CW_DIGITAL_QSO_POINTS
            # print(f"qso_points {result['qso_points']} total_qsos {result['total_qsos']} valid_qsos {result['valid_qsos']}")
            result['qsos_by_mode']['CW/Digital'] += 1

        # Check for N5LCC
        if rcvd_call == 'N5LCC':
            result['worked_n5lcc'] = True
            result['num_n5lcc_contacts'] += 1

        ## MULTIPLIERS

        mult_check = band + mode_cat + rcvd_qth
        if mult_check not in mult_dups:
            mult_dups.append(mult_check)

            ## Everyone gets county multiplier for counties, but only LA stations get state/province/DX multipliers
            if rcvd_qth in processor.counties:
                result['counties_worked'].add(rcvd_qth)
                result['counties_worked_multiplier'] += 1
            
            # LA stations get state, province, and DX multipliers
            if result['location_type'] == 'LA-FIXED' or result['location_type'] == 'LA-ROVER':
                if dx_rcvd_qth:  ## DX multiplier
                    result['dx_worked'].add(dx_rcvd_qth['dxcc_entity'])
                    result['dx_worked_multiplier'] += 1
                # LA: states, provinces, DX are multipliers
                elif rcvd_qth in processor.provinces:
                    result['provinces_worked'].add(rcvd_qth)
                    result['provinces_worked_multiplier'] += 1
                elif rcvd_qth in processor.states:
                    result['states_worked'].add(rcvd_qth)
                    # print(result['states_worked'])
                    # print(f"rcvd_qth: {rcvd_qth}")
                    result['states_worked_multiplier'] += 1

    # print("break before points")
    # Finished with points, now sum the individual multipliers
    for i in ['counties', 'states', 'provinces', 'dx']:
        result['total_multipliers'] += result[f'{i}_worked_multiplier']
        
    ## score before bonuses
    result['final_score'] = result['qso_points'] * result['total_multipliers']

    ## add bonus points for one or more N5LCC contacts
    if result['worked_n5lcc']:
        result['final_score'] += CALLSIGN_BONUS_POINTS

    ## Add rover bonus points for activated counties
    if result['location_type'] == 'LA-ROVER':
        result['rover_bonus_points'] = len(result['counties_activated']) * ROVER_COUNTY_BONUS
        result['final_score'] += result['rover_bonus_points']

    ## Bonus for something outside of QSOs
    if result['callsign'] in EXTRA_BONUS_CALLS and contest_year == EXTRA_BONUS_YEAR:
        result['final_score'] += EXTRA_BONUS_POINTS


## END of score_qsos

def cross_check_all_logs(all_results, contest_year: str) -> Dict:

    global printout, all_callsigns, processor
    """
    Main cross-checking function.
    
    Process:
    1. Load all contest results for the year
    2. Build QSO index for fast lookups
    3. Cross-check each operator's QSOs
    4. calculate final scores using only valid QSOs
    
    Args:
        year: Contest year to process (default from config)
    
    Returns:
        dict: Summary statistics of cross-checking
    """
    # print(f"Cross-checking logs for {year}...")
    
    # Load all results
    # all_results = load_all_results(year)
    print(f"Loaded {len(all_results)} logs")
    print(f"Total QSOs across all logs: {sum(len(r.get('qsos', [])) for r in all_results)}")

    # Get all callsigns that submitted logs (for UNIQUE detection)
    all_callsigns = set(r['callsign'] for r in all_results)
    
    # Build QSO index
    qso_index = build_qso_index(all_results)
    print(f"Built QSO index with {sum(len(v) for v in qso_index.values())} entries")
    
    # Cross-check each operator
    stats = {
        'total_qsos': 0,
        'confirmed': 0,
        'nil': 0,
        'busted': 0,
        'exchange_error': 0,
        'unique': 0
    }
    

    # Now that all cross-checkling is done, calculate scores using only valid QSOs and collect all the stats for the final report
    for result in all_results:
        score_qsos(result, contest_year)
        operator_stats = cross_check_operator(result, qso_index)
        for key in stats:
            if key in operator_stats:
                stats[key] += operator_stats[key]
    

    print(f"Cross-check complete:")
    print(f"  Total QSOs: {stats['total_qsos']}")
    # print(f"  Confirmed: {stats['confirmed']} ({100*stats['confirmed']/stats['total_qsos']:.1f}%)")
    print(f"  NIL: {stats['nil']}")
    print(f"  Busted: {stats['busted']}")
    print(f"  Exchange errors: {stats['exchange_error']}")
    print(f"  Unique: {stats['unique']}")

    return all_results, stats


def build_qso_index(all_results):

    global printout, all_callsigns, processor
    """
    Build an index of all QSOs for fast cross-checking lookups.
    
    Index structure:
    {
        'W5XYZ': [
            {
                'operator': 'K5ABC',
                'band': '20m',
                'mode': 'PH',
                'date': '2023-04-01',
                'time': '1430, # or 14:30`
                'sent_qth': 'ORLEANS',
                'rcvd_qth': 'TX',
                'line_num': 42
            },
            ...
        ]
    }
    
    Args:
        all_results: List of all contest results
        
    Returns:
        dict: QSO index keyed by callsign worked
    """
    index = defaultdict(list)
    
    for result in all_results:
        operator = result['callsign']
        
        for qso in result.get('qsos', []):
            # Skip QSOs that are already marked invalid (mode mismatches, etc.)
            if qso.get('is_valid', True) == False:
                continue
            
            # Parse timestamp
            # try:
            #     qso_time = parse_qso_timestamp(qso['date'], qso['time'])
            # except:
            #     continue  # Skip QSOs with invalid timestamps
            
            # Add to index under the callsign worked
            index[qso['rcvd_call']].append({
                'operator': operator,
                'band': qso['band'],
                'mode': qso['mode'],
                'date': qso['date'],
                'time': qso['time'],
                'sent_call': qso['sent_call'],
                'sent_qth': qso['sent_qth'],
                'rcvd_qth': qso['rcvd_qth'],
                'line_num': qso.get('line_num', 0)
            })
    
    return index


def cross_check_operator(result, qso_index):

    global printout, all_callsigns, processor
    """
    Cross-check all QSOs for a single operator.
    Marks QSOs with error codes and adds warning messages.
    
    QSO error codes (xcheck field):
    - '' (empty string): Valid QSO
    - 'NIL': Not found in other station's log
    - 'B': Busted callsign (typo detected)
    - 'XCH': Exchange error (wrong info received)
    
    Args:
        result: Operator's contest result dictionary
        qso_index: QSO index for lookups
        all_results: List of all results (for UNIQUE detection)
        
    Returns:
        dict: Statistics for this operator
    """
    operator = result['callsign']
    stats = {
        'total_qsos': 0,
        'confirmed': 0,
        'nil': 0,
        'busted': 0,
        'exchange_error': 0,
        'unique': 0,
        'had_xcheck': 0
    }

    for qso in result.get('qsos', []):
        stats['total_qsos'] += 1
        
        # Skip QSOs already marked invalid (mode mismatches, etc.)
        # Check if they already have an error set during initial processing
        if 'xcheck' in qso and qso['xcheck'] != '':
            stats['had_xcheck'] += 1
            stats['valid_qsos'] = min(0, stats['valid_qsos'] - 1)  # Decrement valid QSOs if already marked valid
            continue
        
        # Initialize xcheck field if not present
        if 'xcheck' not in qso:
            qso['xcheck'] = ''
        
        # Find matching QSO
        match_result = find_matching_qso(result, operator, qso, qso_index)
        
        status = match_result['status']
        stats[status] += 1
        
        # Mark QSO and add warning if needed
        if status == 'CONFIRMED':
            qso['xcheck'] = ''  # Valid - for _score_qsos to check
            qso['cross_check_status'] = 'CONFIRMED'  # For reporting
            
        elif status == 'NIL':
            qso['xcheck'] = 'NIL'
            qso['cross_check_status'] = 'NIL'
            stats['had_xcheck'] += 1
            result['warnings'].append(
                f"ERROR QSO at line {qso.get('line_num', '?')}: "
                f"{qso['rcvd_call']} on {qso['band']} {qso['mode']} on {qso['date']} at {qso['time']} - "
                f"Not found in {qso['rcvd_call']}'s log (NIL)"
            )
            
        elif status == 'BUSTED':
            qso['xcheck'] = 'B'
            qso['cross_check_status'] = 'BUSTED'
            actual_call = match_result.get('actual_call', '?')
            stats['had_xcheck'] += 1
            result['warnings'].append(
                f"ERROR QSO at line {qso.get('line_num', '?')}: "
                f"{qso['rcvd_call']} on {qso['band']} {qso['mode']} on {qso['date']} at {qso['time']} - "
                f"Callsign error, possibly {actual_call} (BUSTED)"
            )
            
        elif status == 'EXCHANGE_ERROR':
            qso['xcheck'] = 'XCH'
            qso['cross_check_status'] = 'EXCHANGE_ERROR'
            stats['had_xcheck'] += 1
            result['warnings'].append(
                f"ERROR QSO at line {qso.get('line_num', '?')}: "
                f"{qso['rcvd_call']} on {qso['band']} {qso['mode']} on {qso['date']} at {qso['time']} - "
                f"Exchange mismatch (sent {qso['sent_qth']}, they logged {match_result.get('their_rcvd', '?')})"
            )
            
        elif status == 'UNIQUE':
            # No penalty for unique - station may not have submitted log
            qso['cross_check_status'] = 'UNIQUE'
            # No warning added
    
    
    return stats


def find_matching_qso(result, operator, qso, qso_index):

    global printout, all_callsigns, processor
    """
    Find a matching QSO in other logs.
    
    Matching criteria:
    1. Reciprocal callsigns (A worked B, B worked A)
    2. Band matches exactly
    3. Mode matches (accounting for mode mapping)
    4. Time within ±30 minutes
    5. Exchange information matches
    
    Args:
        operator: This operator's callsign
        qso: QSO to check
        qso_index: QSO index for lookups
        all_callsigns: Set of all callsigns that submitted logs
        
    Returns:
        dict: {
            'status': 'CONFIRMED'|'NIL'|'BUSTED'|'EXCHANGE_ERROR'|'UNIQUE',
            'actual_call': corrected callsign if busted,
            'their_rcvd': what they received if exchange error
        }
    """
    rcvd_call = qso['rcvd_call']
    
    # Check if this callsign submitted a log
    if rcvd_call not in all_callsigns:
        # Station didn't submit - check if similar callsign exists (BUSTED)
        if ENABLE_FUZZY_MATCHING:
            fuzzy_match = find_fuzzy_callsign_match(all_callsigns, rcvd_call) 
            if fuzzy_match:
                return {
                    'status': 'busted',
                    'actual_call': fuzzy_match
                }
        # No log from this station - UNIQUE (not penalized)
        return {'status': 'unique'}
    
    # Look for reciprocal QSO in their log
    their_qsos = qso_index.get(operator, [])  # They should have worked us
   
    # Find matching QSO
    for their_qso in their_qsos:
        # Must be from the station we're checking
        if their_qso['operator'] != rcvd_call:
            continue
        
        # Band must match exactly
        if their_qso['band'] != qso['band']:
            continue
        
        # Mode must match (account for mode equivalence)
        if not modes_match(qso['mode'], their_qso['mode']):
            continue
        
        # Time must be within window
        time_match = time_check([qso['date'], qso['time']], [their_qso['date'], their_qso['time']])
        if not time_match:
            result['warnings'].append(f"ERROR QSO - send and receive had different times: {operator}: {qso['date']} {qso['time']} vs {rcvd_call}: {their_qso['date']} {their_qso['time']} for QSO at line {qso.get('line_num', '?')}")
            continue
        
        # Found a matching QSO!
        # Now check if exchange matches
        # We sent them our QTH, they should have received it
        # They sent us their QTH, we should have received it
        
        our_sent = qso['sent_qth']
        their_rcvd = their_qso['rcvd_qth']
        
        if our_sent != their_rcvd:
            # Exchange mismatch
            return {
                'status': 'exchange_error',
                'their_rcvd': their_rcvd
            }
        
        # Everything matches!
        return {'status': 'confirmed'}
    
    # No matching QSO found in their log
    return {'status': 'nil'}


def modes_match(mode1, mode2):

    global printout, all_callsigns, processor
    """
    Check if two modes are equivalent for matching purposes.
    
    Mode mappings:
    - PH (Phone) and FM are equivalent
    - CW, RY (RTTY), DG (Digital) are all digital modes
    
    Args:
        mode1, mode2: Mode strings (CW, PH, FM, RY, DG)
        
    Returns:
        bool: True if modes match
    """
    # Normalize modes to categories
    phone_modes = {'PH', 'FM'}
    digital_modes = {'CW', 'RY', 'DG'}
    
    if mode1 in phone_modes and mode2 in phone_modes:
        return True
    if mode1 in digital_modes and mode2 in digital_modes:
        return True
    if mode1 == mode2:
        return True
    
    return False


def find_fuzzy_callsign_match(all_callsigns, callsign):
    global printout, processor
    """
    Find a similar callsign using fuzzy matching.
    Detects common errors like:
    - Single character differences (O/0, I/1, S/5)
    - Adjacent key typos
    - Missing/extra characters
    
    Args:
        callsign: Callsign to match
        all_callsigns: Set of valid callsigns
        
    Returns:
        str|None: Matching callsign or None
    """
    for candidate in all_callsigns:
        if edit_distance(callsign, candidate) <= MAX_EDIT_DISTANCE:
            return candidate
    
    return None


def edit_distance(s1, s2):
    """
    Calculate Levenshtein edit distance between two strings.
    
    Args:
        s1, s2: Strings to compare
        
    Returns:
        int: Minimum number of single-character edits needed
    """
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Parse a date string (YYYY-MM-DD) and a time string (HHMM or HH:MM) into a datetime object."""
    time_str = time_str.replace(":", "")  # normalize to HHMMSS
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H%M%S")

def within_60_minutes(dt1: datetime, dt2: datetime) -> bool:
    """Return True if dt1 and dt2 are within 60 minutes of each other."""
    delta = abs(dt2 - dt1)
    return delta <= timedelta(minutes=60)

def time_check(ours, theirs):
    try:
        dt1 = parse_datetime(ours[0], ours[1])
        dt2 = parse_datetime(theirs[0], theirs[1])
        delta = abs(dt2 - dt1)
        return delta <= timedelta(minutes=60)
    except Exception as e:
        print('printout: exception', e)
        return False


if __name__ == '__main__':
    """Run cross-checking from command line"""
    import sys
    
    year = sys.argv[1] if len(sys.argv) > 1 else CONTEST_YEAR
    stats = cross_check_all_logs(year)
    
    print("\n=== Cross-Check Summary ===")
    print(f"Year: {year}")
    print(f"Total QSOs checked: {stats['total_qsos']}")
    print(f"Confirmed: {stats['confirmed']} ({100*stats['confirmed']/stats['total_qsos']:.1f}%)")
    print(f"Not in log (NIL): {stats['nil']}")
    print(f"Busted calls: {stats['busted']}")
    print(f"Exchange errors: {stats['exchange_error']}")
    print(f"Unique (no log): {stats['unique']}")

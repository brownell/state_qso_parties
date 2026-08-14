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

import json
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from config.config import CONTEST_YEAR, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE, DATABASE_FILE
from database import ContestDatabase, save_result
from processor import UnifiedLogProcessor

# Cross-check configuration
TIME_WINDOW_MINUTES = 30  # ±30 minutes for time matching
ENABLE_FUZZY_MATCHING = True  # Check for callsign errors
MAX_EDIT_DISTANCE = 2  # Maximum character differences for fuzzy matching


def cross_check_all_logs(year=CONTEST_YEAR):
    """
    Main cross-checking function.
    
    Process:
    1. Load all contest results for the year
    2. Build QSO index for fast lookups
    3. Cross-check each operator's QSOs
    4. Recalculate final scores using only valid QSOs
    5. Save updated results to database
    
    Args:
        year: Contest year to process (default from config)
    
    Returns:
        dict: Summary statistics of cross-checking
    """
    print(f"Cross-checking logs for {year}...")
    
    # Load all results
    all_results = load_all_results(year)
    print(f"Loaded {len(all_results)} logs")
    
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
    
    for result in all_results:
        operator_stats = cross_check_operator(result, qso_index, all_results)
        for key in stats:
            if key in operator_stats:
                stats[key] += operator_stats[key]
    
    print(f"Cross-check complete:")
    print(f"  Total QSOs: {stats['total_qsos']}")
    print(f"  Confirmed: {stats['confirmed']} ({100*stats['confirmed']/stats['total_qsos']:.1f}%)")
    print(f"  NIL: {stats['nil']}")
    print(f"  Busted: {stats['busted']}")
    print(f"  Exchange errors: {stats['exchange_error']}")
    print(f"  Unique: {stats['unique']}")
    
    # Create processor instance for recalculation
    print("\nInitializing processor for score recalculation...")
    processor = UnifiedLogProcessor(Path(COUNTIES_FILE), Path(STATES_FILE), Path(PROVINCES_FILE), Path(DXCC_ENTITIES_FILE))
    
    # Recalculate final scores
    print("Recalculating final scores...")
    for result in all_results:
        recalculate_final_score(result, processor)
    
    # Save updated results
    print("Saving updated results to database...")
    for result in all_results:
        save_result(result, DATABASE_FILE)
    
    print("Cross-checking complete!")
    return stats


def load_all_results(year):
    """
    Load all contest results for a given year.
    
    Args:
        year: Contest year
        
    Returns:
        list: List of result dictionaries
    """
    conn = get_connection()
    cursor = conn.execute(
        'SELECT data FROM contest_results WHERE year = ?',
        (str(year),)
    )
    
    results = []
    for row in cursor:
        result = json.loads(row[0])
        results.append(result)
    
    return results


def build_qso_index(all_results):
    """
    Build an index of all QSOs for fast cross-checking lookups.
    
    Index structure:
    {
        'W5XYZ': [
            {
                'operator': 'K5ABC',
                'band': '20m',
                'mode': 'PH',
                'time': datetime(2026, 4, 12, 14, 30),
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
            try:
                qso_time = parse_qso_timestamp(qso['date'], qso['time'])
            except:
                continue  # Skip QSOs with invalid timestamps
            
            # Add to index under the callsign worked
            index[qso['rcvd_call']].append({
                'operator': operator,
                'band': qso['band'],
                'mode': qso['mode'],
                'time': qso_time,
                'sent_call': qso['sent_call'],
                'sent_qth': qso['sent_qth'],
                'rcvd_qth': qso['rcvd_qth'],
                'line_num': qso.get('line_num', 0)
            })
    
    return index


def cross_check_operator(result, qso_index, all_results):
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
        'unique': 0
    }
    
    # Get all callsigns that submitted logs (for UNIQUE detection)
    all_callsigns = set(r['callsign'] for r in all_results)
    
    for qso in result.get('qsos', []):
        stats['total_qsos'] += 1
        
        # Skip QSOs already marked invalid (mode mismatches, etc.)
        # Check if they already have an error set during initial processing
        if 'xcheck' in qso and qso['xcheck'] != '':
            continue
        
        # Initialize xcheck field if not present
        if 'xcheck' not in qso:
            qso['xcheck'] = ''
        
        # Find matching QSO
        match_result = find_matching_qso(operator, qso, qso_index, all_callsigns)
        
        status = match_result['status']
        stats[status] += 1
        
        # Mark QSO and add warning if needed
        if status == 'CONFIRMED':
            qso['xcheck'] = ''  # Valid - for _score_qsos to check
            qso['cross_check_status'] = 'CONFIRMED'  # For reporting
            
        elif status == 'NIL':
            qso['xcheck'] = 'NIL'
            qso['cross_check_status'] = 'NIL'
            result['warnings'].append(
                f"QSO at line {qso.get('line_num', '?')}: "
                f"{qso['rcvd_call']} on {qso['band']} {qso['mode']} at {qso['time']} - "
                f"Not found in {qso['rcvd_call']}'s log (NIL)"
            )
            
        elif status == 'BUSTED':
            qso['xcheck'] = 'B'
            qso['cross_check_status'] = 'BUSTED'
            actual_call = match_result.get('actual_call', '?')
            result['warnings'].append(
                f"QSO at line {qso.get('line_num', '?')}: "
                f"{qso['rcvd_call']} on {qso['band']} {qso['mode']} at {qso['time']} - "
                f"Callsign error, possibly {actual_call} (BUSTED)"
            )
            
        elif status == 'EXCHANGE_ERROR':
            qso['xcheck'] = 'XCH'
            qso['cross_check_status'] = 'EXCHANGE_ERROR'
            result['warnings'].append(
                f"QSO at line {qso.get('line_num', '?')}: "
                f"{qso['rcvd_call']} on {qso['band']} {qso['mode']} at {qso['time']} - "
                f"Exchange mismatch (sent {qso['sent_qth']}, they logged {match_result.get('their_rcvd', '?')})"
            )
            
        elif status == 'UNIQUE':
            # No penalty for unique - station may not have submitted log
            qso['xcheck'] = ''  # Valid
            qso['cross_check_status'] = 'UNIQUE'
            # No warning added
    
    return stats


def find_matching_qso(operator, qso, qso_index, all_callsigns):
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
            fuzzy_match = find_fuzzy_callsign_match(rcvd_call, all_callsigns)
            if fuzzy_match:
                return {
                    'status': 'BUSTED',
                    'actual_call': fuzzy_match
                }
        
        # No log from this station - UNIQUE (not penalized)
        return {'status': 'UNIQUE'}
    
    # Look for reciprocal QSO in their log
    their_qsos = qso_index.get(operator, [])  # They should have worked us
    
    # Parse our QSO time
    try:
        our_time = parse_qso_timestamp(qso['date'], qso['time'])
    except:
        return {'status': 'NIL'}  # Can't parse time, can't match
    
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
        time_diff = abs((their_qso['time'] - our_time).total_seconds())
        if time_diff > TIME_WINDOW_MINUTES * 60:
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
                'status': 'EXCHANGE_ERROR',
                'their_rcvd': their_rcvd
            }
        
        # Everything matches!
        return {'status': 'CONFIRMED'}
    
    # No matching QSO found in their log
    return {'status': 'NIL'}


def modes_match(mode1, mode2):
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


def find_fuzzy_callsign_match(callsign, all_callsigns):
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


def parse_qso_timestamp(date_str, time_str):
    """
    Parse QSO date and time into datetime object.
    
    Args:
        date_str: Date string (YYYY-MM-DD)
        time_str: Time string (HH:MM or HH:MM:SS)
        
    Returns:
        datetime: Parsed timestamp
    """
    # Handle both HH:MM and HH:MM:SS formats
    if len(time_str) == 5:  # HH:MM
        time_str += ':00'
    
    timestamp_str = f"{date_str} {time_str}"
    return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')


def recalculate_final_score(result, processor):
    """
    Recalculate final score using only valid QSOs.
    
    This calls the existing _score_qsos() method from UnifiedLogProcessor,
    which will skip QSOs that have a non-empty 'xcheck' field.
    
    Args:
        result: Contest result dictionary (modified in place)
        processor: UnifiedLogProcessor instance
    """
    # Call the existing scoring function
    # It will skip QSOs where xcheck is not empty
    processor._score_qsos(result)
    
    # Calculate score reduction percentage
    if result.get('claimed_score', 0) > 0:
        reduction = (result['claimed_score'] - result['final_score']) / result['claimed_score'] * 100
        result['score_reduction_pct'] = round(reduction, 1)
    else:
        result['score_reduction_pct'] = 0


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

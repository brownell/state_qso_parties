"""
Test script for LAQP cross-checking module

This creates synthetic test data to verify cross-checking logic works correctly.
Run this before processing real contest data.

NOTE: This test requires:
- UnifiedLogProcessor class in processor.py with _score_qsos() method
- Reference data files (counties, states, provinces, DXCC entities)
"""

import json
from database import get_connection, save_contest_result
from cross_check import cross_check_all_logs

def create_test_data():
    """Create synthetic test logs for cross-checking validation"""
    
    print("Creating test data...")
    
    # Test Log 1: K5ABC
    result1 = {
        'year': '2026',
        'callsign': 'K5ABC',
        'name': 'Test Operator 1',
        'location_type': 'LA-FIXED',
        'mode_category': 'MIXED',
        'power_level': 'LOW',
        'claimed_score': 3000,
        'final_score': 3000,
        'qso_points': 100,
        'total_qsos': 5,
        'valid_qsos': 5,
        'total_multipliers': 30,
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
        'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 5, '15': 0, '10': 0, '6': 0, '2': 0},
        'qsos_by_mode': {'Phone': 3, 'CW/Digital': 2},
        'qsos_by_hour': {i: 0 for i in range(12)},
        'bands_worked': {'20'},
        'errors': [],
        'warnings': [],
        'is_valid': True,
        'qsos': [
            # QSO 1: Will be CONFIRMED (W5XYZ has reciprocal)
            {
                'band': '20m',
                'mode': 'PH',
                'mode_category': 'PHONE',
                'date': '2026-04-12',
                'time': '14:30:00',
                'sent_call': 'K5ABC',
                'sent_rst': '59',
                'sent_qth': 'ORLEANS',
                'rcvd_call': 'W5XYZ',
                'rcvd_rst': '59',
                'rcvd_qth': 'TX',
                'line_num': 1
            },
            # QSO 2: Will be NIL (N5TEST doesn't have this in log)
            {
                'band': '20m',
                'mode': 'PH',
                'mode_category': 'PHONE',
                'date': '2026-04-12',
                'time': '15:00:00',
                'sent_call': 'K5ABC',
                'sent_rst': '59',
                'sent_qth': 'ORLEANS',
                'rcvd_call': 'N5TEST',
                'rcvd_rst': '59',
                'rcvd_qth': 'AL',
                'line_num': 2
            },
            # QSO 3: Will be BUSTED (typo - should be W5XYZ)
            {
                'band': '20m',
                'mode': 'CW',
                'mode_category': 'CW-DIGITAL',
                'date': '2026-04-12',
                'time': '16:00:00',
                'sent_call': 'K5ABC',
                'sent_rst': '599',
                'sent_qth': 'ORLEANS',
                'rcvd_call': 'W5XYY',  # Typo!
                'rcvd_rst': '599',
                'rcvd_qth': 'TX',
                'line_num': 3
            },
            # QSO 4: Will be EXCHANGE_ERROR (W5XYZ logged different exchange)
            {
                'band': '20m',
                'mode': 'CW',
                'mode_category': 'CW-DIGITAL',
                'date': '2026-04-12',
                'time': '17:00:00',
                'sent_call': 'K5ABC',
                'sent_rst': '599',
                'sent_qth': 'ORLEANS',
                'rcvd_call': 'W5XYZ',
                'rcvd_rst': '599',
                'rcvd_qth': 'TX',  # K5ABC logged TX, but W5XYZ sent LA
                'line_num': 4
            },
            # QSO 5: Will be UNIQUE (K9ZZZ didn't submit log)
            {
                'band': '20m',
                'mode': 'PH',
                'mode_category': 'PHONE',
                'date': '2026-04-12',
                'time': '18:00:00',
                'sent_call': 'K5ABC',
                'sent_rst': '59',
                'sent_qth': 'ORLEANS',
                'rcvd_call': 'K9ZZZ',
                'rcvd_rst': '59',
                'rcvd_qth': 'IL',
                'line_num': 5
            }
        ]
    }
    
    # Test Log 2: W5XYZ
    result2 = {
        'year': '2026',
        'callsign': 'W5XYZ',
        'name': 'Test Operator 2',
        'location_type': 'NON-LA',
        'mode_category': 'MIXED',
        'power_level': 'LOW',
        'claimed_score': 2000,
        'final_score': 2000,
        'qso_points': 80,
        'total_qsos': 3,
        'valid_qsos': 3,
        'total_multipliers': 25,
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
        'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 3, '15': 0, '10': 0, '6': 0, '2': 0},
        'qsos_by_mode': {'Phone': 1, 'CW/Digital': 2},
        'qsos_by_hour': {i: 0 for i in range(12)},
        'bands_worked': {'20'},
        'errors': [],
        'warnings': [],
        'is_valid': True,
        'qsos': [
            # Reciprocal for K5ABC QSO 1 - CONFIRMED
            {
                'band': '20m',
                'mode': 'PH',
                'mode_category': 'PHONE',
                'date': '2026-04-12',
                'time': '14:31:00',  # 1 minute off - within window
                'sent_call': 'W5XYZ',
                'sent_rst': '59',
                'sent_qth': 'TX',
                'rcvd_call': 'K5ABC',
                'rcvd_rst': '59',
                'rcvd_qth': 'ORLEANS',
                'line_num': 1
            },
            # Reciprocal for K5ABC QSO 3 - different call (W5XYY vs W5XYZ)
            {
                'band': '20m',
                'mode': 'CW',
                'mode_category': 'CW-DIGITAL',
                'date': '2026-04-12',
                'time': '16:02:00',
                'sent_call': 'W5XYZ',
                'sent_rst': '599',
                'sent_qth': 'TX',
                'rcvd_call': 'K5ABC',
                'rcvd_rst': '599',
                'rcvd_qth': 'ORLEANS',
                'line_num': 2
            },
            # Reciprocal for K5ABC QSO 4 - EXCHANGE_ERROR
            {
                'band': '20m',
                'mode': 'CW',
                'mode_category': 'CW-DIGITAL',
                'date': '2026-04-12',
                'time': '17:01:00',
                'sent_call': 'W5XYZ',
                'sent_rst': '599',
                'sent_qth': 'LA',  # W5XYZ sent LA, not TX!
                'rcvd_call': 'K5ABC',
                'rcvd_rst': '599',
                'rcvd_qth': 'ORLEANS',
                'line_num': 3
            }
        ]
    }
    
    # Test Log 3: N5TEST (has K5ABC in log, but K5ABC doesn't have N5TEST)
    result3 = {
        'year': '2026',
        'callsign': 'N5TEST',
        'name': 'Test Operator 3',
        'location_type': 'NON-LA',
        'mode_category': 'PHONE',
        'power_level': 'LOW',
        'claimed_score': 500,
        'final_score': 500,
        'qso_points': 25,
        'total_qsos': 1,
        'valid_qsos': 1,
        'total_multipliers': 20,
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
        'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 1, '15': 0, '10': 0, '6': 0, '2': 0},
        'qsos_by_mode': {'Phone': 1, 'CW/Digital': 0},
        'qsos_by_hour': {i: 0 for i in range(12)},
        'bands_worked': {'20'},
        'errors': [],
        'warnings': [],
        'is_valid': True,
        'qsos': [
            # Has K5ABC in log - will be NIL for N5TEST
            {
                'band': '20m',
                'mode': 'PH',
                'mode_category': 'PHONE',
                'date': '2026-04-12',
                'time': '16:30:00',
                'sent_call': 'N5TEST',
                'sent_rst': '59',
                'sent_qth': 'AL',
                'rcvd_call': 'K5ABC',
                'rcvd_rst': '59',
                'rcvd_qth': 'ORLEANS',
                'line_num': 1
            }
        ]
    }
    
    # Save test data to database
    save_contest_result(result1)
    save_contest_result(result2)
    save_contest_result(result3)
    
    print("Test data created:")
    print("  - K5ABC: 5 QSOs (expect 1 CONFIRMED, 1 NIL, 1 BUSTED, 1 EXCHANGE_ERROR, 1 UNIQUE)")
    print("  - W5XYZ: 3 QSOs (expect all CONFIRMED)")
    print("  - N5TEST: 1 QSO (expect 1 NIL)")
    print()


def verify_results():
    """Verify cross-checking results"""
    
    print("\n=== Verifying Results ===\n")
    
    # Load results
    from cross_check import load_all_results
    results = load_all_results('2026')
    
    # Check K5ABC
    k5abc = next(r for r in results if r['callsign'] == 'K5ABC')
    print("K5ABC Results:")
    print(f"  Total QSOs: {len(k5abc['qsos'])}")
    print(f"  Valid QSOs: {sum(1 for q in k5abc['qsos'] if q.get('is_valid', True))}")
    print(f"  Warnings: {len(k5abc['warnings'])}")
    print()
    
    for qso in k5abc['qsos']:
        status = qso.get('cross_check_status', 'UNKNOWN')
        valid = qso.get('is_valid', True)
        print(f"  Line {qso['line_num']}: {qso['rcvd_call']} -> {status} (valid={valid})")
    
    print()
    print("Warnings:")
    for warning in k5abc['warnings']:
        print(f"  - {warning}")
    
    # Check expected results
    print("\n=== Verification ===")
    
    qso_statuses = {qso['line_num']: qso.get('cross_check_status') for qso in k5abc['qsos']}
    
    checks = [
        (1, 'CONFIRMED', "QSO 1 should be CONFIRMED"),
        (2, 'NIL', "QSO 2 should be NIL"),
        (3, 'BUSTED', "QSO 3 should be BUSTED"),
        (4, 'EXCHANGE_ERROR', "QSO 4 should be EXCHANGE_ERROR"),
        (5, 'UNIQUE', "QSO 5 should be UNIQUE")
    ]
    
    all_passed = True
    for line_num, expected, description in checks:
        actual = qso_statuses.get(line_num, 'UNKNOWN')
        passed = actual == expected
        all_passed = all_passed and passed
        status_symbol = "✅" if passed else "❌"
        print(f"{status_symbol} {description}: {actual}")
    
    print()
    if all_passed:
        print("🎉 All tests PASSED!")
    else:
        print("⚠️  Some tests FAILED - check implementation")
    
    return all_passed


def clear_test_data():
    """Remove test data from database"""
    conn = get_connection()
    conn.execute("DELETE FROM contest_results WHERE year = '2026'")
    conn.commit()
    print("Test data cleared from database")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clear_test_data()
    else:
        print("=" * 70)
        print("LAQP Cross-Checking Test Suite")
        print("=" * 70)
        print()
        
        # Create test data
        create_test_data()
        
        # Run cross-checking
        print("Running cross-check...")
        stats = cross_check_all_logs('2026')
        
        # Verify results
        all_passed = verify_results()
        
        print()
        print("=" * 70)
        print("Test complete!")
        print("To clear test data: python test_cross_check.py clear")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)

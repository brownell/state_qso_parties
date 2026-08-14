#!/usr/bin/env python3
"""
Quick test script for the Louisiana QSO Party web app

This script tests the key components without requiring a full Flask server.
"""

import sys
import json


def test_format_functions():
    """Test the formatting functions"""
    print("Testing format functions...")
    
    # Test data
    test_set = {'ORL', 'JEF', 'STB', 'PLQ', 'TAN'}
    test_dict = {
        '40-Phone': {'ORL', 'JEF', 'STB'},
        '20-Phone': {'ORL', 'TAN'},
        '80-Phone': {'ORL', 'JEF'}
    }
    
    # Test set formatting
    from web import format_set_as_list
    formatted_set = format_set_as_list(test_set)
    print(f"✓ Set formatted: {formatted_set}")
    assert isinstance(formatted_set, list)
    assert len(formatted_set) == 5

    
    print("✓ All format function tests passed!\n")


def test_result_formatting():
    """Test the complete result formatting"""
    print("Testing complete result formatting...")
    
    from web import format_result_for_display
    
    # Mock result data
    mock_result = {
        'callsign': 'K5ABC',
        'category': 'nl_ph_lo',
        'overlay': None,
        'location_type': 'NON-LA',
        'mode_category': 'Phone',
        'power_level': 'Low',
        'final_score': 1250,
        'qso_points': 625,
        'total_qsos': 350,
        'valid_qsos': 313,
        'total_multipliers': 2,
        'counties_worked': {'ORL', 'JEF', 'STB', 'PLQ', 'TAN'},
        'counties_worked_multiplier': 5,
        'states_worked': set(),
        'states_worked_multiplier': 0,
        'provinces_worked': set(),
        'provinces_worked_multiplier': 0,
        'dx_worked': set(),
        'dx_worked_multiplier': 0,
        'counties_activated': set(),
        'rover_bonus_points': 0,
        'worked_n5lcc': True,
        'num_n5lcc_contacts': 3,
        'qsos_by_band': {'160': 0, '80': 45, '40': 123, '20': 142, '15': 3, '10': 0, '6': 0, '2': 0},
        'qsos_by_mode': {'Phone': 313, 'CW/Digital': 0},
        'qsos_by_hour': {0: 28, 1: 35, 2: 42, 3: 38, 4: 31, 5: 29, 6: 26, 7: 24, 8: 22, 9: 18, 10: 12, 11: 8},
        'bands_worked': ['80', '40', '20', '15'],
        'name': 'John Smith',
        'claimed_score': 1250
    }
    
    # Format the result
    display_result = format_result_for_display(mock_result)
    
    # Verify key fields
    assert display_result['callsign'] == 'K5ABC'
    assert display_result['final_score'] == 1250
    assert isinstance(display_result['counties_worked'], list)
    assert len(display_result['counties_worked']) == 5
    assert isinstance(display_result['qsos_by_band'], list)
    
    print("✓ Result formatting successful!")
    print(f"  - Callsign: {display_result['callsign']}")
    print(f"  - Score: {display_result['final_score']}")
    print(f"  - Counties: {len(display_result['counties_worked'])}")
    print(f"  - Bands: {len([b for b in display_result['qsos_by_band'] if b['count'] > 0])}")
    print("✓ All result formatting tests passed!\n")


def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    import os
    
    required_files = [
        'app.py',
        'templates/upload.html',
        'static/css/upload.css',
        'static/js/upload.js',
        'README.md',
        'requirements.txt'
    ]
    
    missing_files = []
    for filepath in required_files:
        if not os.path.exists(filepath):
            missing_files.append(filepath)
            print(f"✗ Missing: {filepath}")
        else:
            print(f"✓ Found: {filepath}")
    
    if missing_files:
        print(f"\n✗ Missing {len(missing_files)} file(s)")
        return False
    else:
        print("\n✓ All required files present!\n")
        return True


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        try:
            from importlib.metadata import version
            flask_version = version('flask')
        except Exception:
            flask_version = "unknown"
        print(f"✓ Flask {flask_version}")
    except ImportError:
        print("✗ Flask not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import werkzeug
        try:
            from importlib.metadata import version
            werkzeug_version = version('werkzeug')
        except Exception:
            werkzeug_version = "unknown"
        print(f"✓ Werkzeug {werkzeug_version}")
    except ImportError:
        print("✗ Werkzeug not installed")
        return False
    
    print("✓ All required modules available!\n")
    return True


def test_json_serialization():
    """Test that result can be serialized to JSON"""
    print("Testing JSON serialization...")
    
    from web import format_result_for_display
    
    mock_result = {
        'callsign': 'K5ABC',
        'final_score': 1250,
        'counties_worked': {'ORL', 'JEF', 'STB'},
        'qsos_by_band': {'80': 45, '40': 123}
    }
    
    # Format the result (should convert sets to lists)
    display_result = format_result_for_display(mock_result)
    
    # Try to serialize to JSON
    try:
        json_str = json.dumps(display_result)
        print(f"✓ JSON serialization successful ({len(json_str)} bytes)")
        
        # Parse it back
        parsed = json.loads(json_str)
        print(f"✓ JSON parsing successful")
        assert parsed['callsign'] == 'K5ABC'
        print("✓ JSON roundtrip successful!\n")
        return True
    except Exception as e:
        print(f"✗ JSON serialization failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Louisiana QSO Party Web App - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Required Imports", test_imports),
        ("Format Functions", test_format_functions),
        ("Result Formatting", test_result_formatting),
        ("JSON Serialization", test_json_serialization),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ All tests passed! The application is ready to use.")
        print("\nNext steps:")
        print("  1. Replace mock validation in app.py with your actual validator")
        print("  2. Start the app: python app.py")
        print("  3. Visit: http://localhost:5000")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())

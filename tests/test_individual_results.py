#!/usr/bin/env python3
"""
Test script for Individual Results Generator

This creates sample individual result DOCX files to verify formatting.
"""
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from laqp.core.individual_results import IndividualResultsGenerator

def test_individual_results():
    """Test generating individual result files"""
    
    print("=" * 60)
    print("Testing Individual Results Generator")
    print("=" * 60)
    print()
    
    # Create test output directory
    test_output = Path(__file__).parent.parent / 'data' / 'output' / 'individual_results' / 'test'
    test_output.mkdir(parents=True, exist_ok=True)
    
    print(f"Output directory: {test_output}")
    print()
    
    generator = IndividualResultsGenerator(contest_year=2026)
    
    # Test Case 1: NON-LA Phone Low Power with POTA overlay
    print("Test 1: NON-LA Phone Low Power with POTA overlay")
    file1 = generator.generate_individual_result(
        callsign='KJ5BYZ',
        category_short='nl_ph_lo',
        overlay='POTA',
        overall_placement=12,
        total_logs=87,
        category_placement=5,
        category_total=23,
        final_score=12450,
        total_qsos=145,
        multipliers=42,
        counties_worked=28,
        states_worked=35,
        provinces_worked=5,
        dx_contacts=2,
        qsos_by_band={160: 10, 80: 25, 40: 40, 20: 35, 15: 20, 10: 15},
        qsos_by_mode={'Phone': 145, 'CW/Digital': 0},
        bands_worked=[160, 80, 40, 20, 15, 10],
        output_dir=test_output
    )
    print(f"  Created: {file1.name}")
    print()
    
    # Test Case 2: LA Fixed Mixed High Power, no overlay, 1st place
    print("Test 2: LA Fixed Mixed High Power, 1st place overall")
    file2 = generator.generate_individual_result(
        callsign='W5ABC',
        category_short='lf_mx_hi',
        overlay=None,
        overall_placement=1,
        total_logs=87,
        category_placement=1,
        category_total=15,
        final_score=45000,
        total_qsos=200,
        multipliers=90,
        counties_worked=64,
        states_worked=48,
        provinces_worked=10,
        dx_contacts=15,
        qsos_by_band={160: 15, 80: 30, 40: 50, 20: 45, 15: 35, 10: 20, 6: 5},
        qsos_by_mode={'Phone': 120, 'CW/Digital': 80},
        bands_worked=[160, 80, 40, 20, 15, 10, 6],
        output_dir=test_output
    )
    print(f"  Created: {file2.name}")
    print()
    
    # Test Case 3: LA Rover CW Only QRP with Wires overlay
    print("Test 3: LA Rover CW Only QRP with Wires overlay")
    file3 = generator.generate_individual_result(
        callsign='N5XYZ',
        category_short='lr_cw_qp',
        overlay='WIRES',
        overall_placement=25,
        total_logs=87,
        category_placement=2,
        category_total=8,
        final_score=8750,
        total_qsos=95,
        multipliers=52,
        counties_worked=12,
        states_worked=28,
        provinces_worked=3,
        dx_contacts=1,
        qsos_by_band={80: 20, 40: 35, 20: 25, 15: 15},
        qsos_by_mode={'Phone': 0, 'CW/Digital': 95},
        bands_worked=[80, 40, 20, 15],
        output_dir=test_output
    )
    print(f"  Created: {file3.name}")
    print()
    
    # Test Case 4: NON-LA Mixed Low Power, 50th place
    print("Test 4: NON-LA Mixed Low Power, mid-pack placement")
    file4 = generator.generate_individual_result(
        callsign='K5TEST',
        category_short='nl_mx_lo',
        overlay=None,
        overall_placement=50,
        total_logs=87,
        category_placement=18,
        category_total=31,
        final_score=5200,
        total_qsos=68,
        multipliers=30,
        counties_worked=15,
        states_worked=0,  # DX station
        provinces_worked=0,
        dx_contacts=0,
        qsos_by_band={40: 28, 20: 22, 15: 18},
        qsos_by_mode={'Phone': 40, 'CW/Digital': 28},
        bands_worked=[40, 20, 15],
        output_dir=test_output
    )
    print(f"  Created: {file4.name}")
    print()
    
    print("=" * 60)
    print("SUCCESS! Test files created in:")
    print(f"  {test_output}")
    print()
    print("Open the DOCX files to verify formatting:")
    print(f"  - {file1.name}")
    print(f"  - {file2.name}")
    print(f"  - {file3.name}")
    print(f"  - {file4.name}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_individual_results()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

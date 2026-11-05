#!/usr/bin/env python3
"""
Texas QSO Party - Calculate Rankings

Generates all leaderboards and saves individual rankings to database.
Run this after all logs have been processed for a contest year.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from leaderboards import generate_leaderboards

def calculate_rankings(year: str):
    """
    Generate all leaderboards and save rankings for a year.
    
    Args:
        year: Contest year
    """
   
    
    print("Calculating leaderboards and saving rankings...")
    print()
    
    # Generate leaderboards (automatically saves rankings)
    sections = generate_leaderboards(year, LEADERBOARDS, RANKINGS, save_rankings=True)
    
    # Print summary
    total_tables = 0
    total_entries = 0
    
    for section in sections:
        print(f"\n{section['section_title']}")
        print("-" * 60)
        
        for table in section['tables']:
            num_rows = len(table['rows'])
            total_tables += 1
            total_entries += num_rows
            print(f"  {table['title']}: {num_rows} entries")
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total leaderboard tables: {total_tables}")
    print(f"Total ranked entries: {total_entries}")
    print(f"Rankings saved to database for year {year}")
    print()
    print("Next step: Generate HTML reports and individual results")
    print()


if __name__ == "__main__":
    import os, sys
    from datetime import datetime
    from config.config import CONTEST_YEAR
    
    # Get year from environment or command line
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = CONTEST_YEAR
    
    generate_rankings(year)

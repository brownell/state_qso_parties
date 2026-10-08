#!/usr/bin/env python3
"""
Louisiana QSO Party - Leaderboard Generator

Generates leaderboard tables based on declarative configuration.
Interprets LEADERBOARDS configuration to create ranked tables.
Also saves individual rankings to contest_results.rankings field.
"""

import sqlite3
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
from config.config import DATABASE_FILE, BONUS_CALLSIGN
from config.config_txqp import  RANKINGS

load_dotenv()
project_root = Path(__file__).resolve().parent  # or .parent.parent if .env is one level up
db_path = (project_root / os.getenv("DATABASE_FILE")).resolve()
db_path.parent.mkdir(parents=True, exist_ok=True)
  
def get_section(year: str, section_config: List[Dict]) -> Dict:
    """
    Generate a single section with multiple tables.
    
    Args:
        year: Contest year
        section_config: Section configuration (first element is metadata, rest are tables)
        rankings_dict: RANKINGS dict for title lookup
        save_rankings: If True, save individual rankings
        
    Returns:
        Dict with section metadata and tables
    """
    # First element is section metadata
    metadata = section_config[0]
    section_title = metadata['section_title']
    section_fields = metadata['show']
    
    # Rest are table definitions
    tables = []
    table_fields = []
    for table_config in section_config[1:]:
        table_fields = [section_fields[0], section_fields[1]]
        table_fields = table_fields + table_config['show']
        table_fields = table_fields + section_fields[2:]
        table = generate_table(year, table_config, table_fields)
        if table['rows']:  # Only include tables with data (skip empty tables)
            tables.append(table)
    
    return {
        'section_title': section_title,
        'table_fields': table_fields,
        'tables': tables
    }
    
def generate_table(year: str, table_config: Dict, table_fields: List) -> Dict:
    """
    Generate a single ranked table.
    
    Args:
        year: Contest year
        table_config: Table configuration with 'title' (ranking code) and 'ands'
        table_fields: Fields to display from section metadata
        rankings_dict: RANKINGS dict to get title from code
        save_rankings: If True, save rankings to database
        
    Returns:
        Dict with table title, headers, and ranked rows
    """
    # title is now a ranking code (e.g., 'NQ')
    cat = table_config['title']
    
    # Get display title from RANKINGS dict
    if RANKINGS and cat in RANKINGS:
        display_title = RANKINGS[cat]
    else:
        # Fallback if RANKINGS not provided
        display_title = table_config['cat']
    
    # Build SQL query - need to also select callsign for saving rankings
    sql, params = build_query(year, cat, table_fields, include_callsign=True)
    
    # Execute query
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        # Add rank column
        ranked_rows = []
        for rank, row in enumerate(rows, 1):
            
            # Build display row: [rank] + [display values]
            ranked_row = [rank] + list(row[0:])
            ranked_rows.append(ranked_row)
    
    # Build headers (Rank + show fields)
    headers = ['Rank'] + [field[1] for field in table_fields]
    
    return {
        'title': display_title,  # Display title, not code
        'category': cat,  # Keep code for reference
        'headers': headers,
        'rows': ranked_rows
    }

def build_query(year: str, cat, table_fields: List, 
                include_callsign: bool = True) -> Tuple[str, List]:
    """
    Build SQL query from AND conditions.
    
    Args:
        year: Contest year
        include_callsign: If True, always include callsign as first field
        
    Returns:
        Tuple of (sql_string, parameters)
    """
    # Extract field names to select
    select_fields = [field[0] for field in table_fields] + ['cat']
    
    # Always include callsign first if requested (for saving rankings)
    if include_callsign and 'callsign' not in select_fields:
        select_clause = 'callsign, ' + ', '.join(select_fields)
    else:
        select_clause = ', '.join(select_fields)
    
    # Build WHERE clause
    where_clause = '''year = ? AND cat = ?'''
    params = [year, cat]

    
    # Build complete query (always ordered by final_score DESC)
    sql = f"""
        SELECT {select_clause}
        FROM contest_results
        WHERE {where_clause}
        ORDER BY final_score DESC
    """
    
    return sql, params

def save_all_rankings():
    """
    Saves the category_rank for all users.
    
    Args:
        year: Contest year
    """

    sql = '''WITH ranked AS (
        SELECT year, callsign, ROW_NUMBER() OVER (ORDER BY final_score DESC) AS calculated_rank
        FROM contest_results
        WHERE year = ? AND cat = ?)
        UPDATE contest_results
        SET category_rank = ranked.calculated_rank
        FROM ranked
        WHERE contest_results.year = ranked.year
        AND contest_results.callsign = ranked.callsign;'''
    
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        
        # for each rank
        for rank in list(RANKINGS.keys()):
            cursor.execute(sql, ('2026', rank))
        
        conn.commit()


if __name__ == "__main__":
    print("LAQP Leaderboard Generator")
    print("This module should be imported, not run directly.")
    print()
    print("Usage:")
    print("  from leaderboards import generate_leaderboards")
    print("  from config.config import LEADERBOARDS, RANKINGS")
    print()
    print("  # Generate leaderboards and save rankings")
    print("  sections = generate_leaderboards('2024', LEADERBOARDS, RANKINGS)")
    print()
    print("  # Just generate without saving")
    print("  sections = generate_leaderboards('2024', LEADERBOARDS, RANKINGS, save_rankings=False)")
    print()
    print("  for section in sections:")
    print("      print(section['section_title'])")
    print("      for table in section['tables']:")
    print("          print(f\"  {table['title']}: {len(table['rows'])} entries\")")


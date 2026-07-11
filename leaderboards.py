#!/usr/bin/env python3
"""
Louisiana QSO Party - Leaderboard Generator

Generates leaderboard tables based on declarative configuration.
Interprets LEADERBOARDS configuration to create ranked tables.
Also saves individual rankings to contest_results.rankings field.
"""

import sqlite3
import json
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from datetime import datetime
from config.config import DATABASE_FILE, BONUS_CALLSIGN


class LeaderboardGenerator:
    """Generates leaderboards from database based on configuration"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        """
        Initialize leaderboard generator.
        
        Args:
            db_path: Path to SQLite database file
        """
        load_dotenv()
        project_root = Path(__file__).resolve().parent  # or .parent.parent if .env is one level up
        self.db_path = (project_root / os.getenv("DATABASE_FILE")).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def generate_leaderboards(self, year: str, leaderboards_config: List, 
                            rankings_dict: Dict = None, 
                            save_rankings: bool = True) -> List[Dict]:
        """
        Generate all leaderboards for a year based on configuration.
        
        Args:
            year: Contest year
            leaderboards_config: LEADERBOARDS configuration from config.py
            rankings_dict: RANKINGS dict mapping codes to descriptions (from config.py)
            save_rankings: If True, save individual rankings to database
            
        Returns:
            List of sections, each containing tables with data
        """
        # Clear all rankings for this year first (if saving)
        if save_rankings:
            self._clear_all_rankings(year)
        
        sections = []
        
        for section_config in leaderboards_config:
            section = self._generate_section(year, section_config, rankings_dict, save_rankings)
            if section['tables']:  # Only include sections with tables
                sections.append(section)
        
        return sections
    
    def _clear_all_rankings(self, year: str):
        """Clear rankings field for all users in a year before regenerating"""
        foo =  datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE contest_results
                SET rankings = ?, updated_at = ?
                WHERE year = ?
            ''', (json.dumps({}), datetime.utcnow().isoformat(), year))

            conn.commit()
    
    def _generate_section(self, year: str, section_config: List[Dict], 
                         rankings_dict: Dict = None, save_rankings: bool = True) -> Dict:
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
        show_fields = metadata['show']
        
        # Rest are table definitions
        tables = []
        for table_config in section_config[1:]:
            table = self._generate_table(year, table_config, show_fields, 
                                        rankings_dict, save_rankings)
            if table['rows']:  # Only include tables with data (skip empty tables)
                tables.append(table)
        
        return {
            'section_title': section_title,
            'show_fields': show_fields,
            'tables': tables
        }
    
    def _generate_table(self, year: str, table_config: Dict, show_fields: List,
                       rankings_dict: Dict = None, save_rankings: bool = True) -> Dict:
        """
        Generate a single ranked table.
        
        Args:
            year: Contest year
            table_config: Table configuration with 'title' (ranking code) and 'ands'
            show_fields: Fields to display from section metadata
            rankings_dict: RANKINGS dict to get title from code
            save_rankings: If True, save rankings to database
            
        Returns:
            Dict with table title, headers, and ranked rows
        """
        # title is now a ranking code (e.g., 'NQ')
        ranking_code = table_config['title']
        ands = table_config['ands']
        
        # Get display title from RANKINGS dict
        if rankings_dict and ranking_code in rankings_dict:
            display_title = rankings_dict[ranking_code]
        else:
            # Fallback if RANKINGS not provided
            display_title = ranking_code
        
        # Build SQL query - need to also select callsign for saving rankings
        sql, params = self._build_query(year, ands, show_fields, include_callsign=True)
        
        # Execute query
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        
        # Add rank column and save rankings
        ranked_rows = []
        for rank, row in enumerate(rows, 1):
            # row[0] is callsign (always included in query)
            # row[1:] are the display fields
            callsign = row[0]
            display_values = row[0:]
            
            # Save this user's ranking if requested
            if save_rankings:
                self._save_user_ranking(year, callsign, ranking_code, rank)
            
            # Build display row: [rank] + [display values]
            ranked_row = [rank] + list(display_values)
            ranked_rows.append(ranked_row)
        
        # Build headers (Rank + show fields)
        headers = ['Rank'] + [field[1] for field in show_fields]
        
        return {
            'title': display_title,  # Display title, not code
            'ranking_code': ranking_code,  # Keep code for reference
            'headers': headers,
            'rows': ranked_rows
        }
    
    def _save_user_ranking(self, year: str, callsign: str, ranking_code: str, rank: int):
        """
        Save a user's ranking in a category.
        
        Adds/updates the ranking code and rank in the user's rankings JSON field.
        
        Args:
            year: Contest year
            callsign: User's callsign
            ranking_code: Ranking category code (e.g., 'NQ')
            rank: User's rank in that category (1, 2, 3, ...)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get current rankings
            cursor.execute('''
                SELECT rankings FROM contest_results
                WHERE year = ? AND callsign = ?
            ''', (year, callsign))
            
            row = cursor.fetchone()
            if not row:
                return  # User not found
            
            # Parse current rankings
            try:
                rankings = json.loads(row[0]) if row[0] else {}
            except (json.JSONDecodeError, TypeError):
                rankings = {}
            
            # Add this ranking
            rankings[ranking_code] = rank
            
            # Save back to database
            cursor.execute('''
                UPDATE contest_results
                SET rankings = ?, updated_at = ?
                WHERE year = ? AND callsign = ?
            ''', (json.dumps(rankings), datetime.utcnow().isoformat(), year, callsign))
            
            conn.commit()
    
    def _build_query(self, year: str, ands: List, show_fields: List, 
                    include_callsign: bool = False) -> Tuple[str, List]:
        """
        Build SQL query from AND conditions.
        
        Args:
            year: Contest year
            ands: List of AND conditions:
                  - 2-element: [field, value] → field = value
                  - 3-element: [field, operator, value] → field operator value
            show_fields: Fields to display
            include_callsign: If True, always include callsign as first field
            
        Returns:
            Tuple of (sql_string, parameters)
        """
        # Extract field names to select
        select_fields = [field[0] for field in show_fields]
        
        # Always include callsign first if requested (for saving rankings)
        if include_callsign and 'callsign' not in select_fields:
            select_clause = 'callsign, ' + ', '.join(select_fields)
        else:
            select_clause = ', '.join(select_fields)
        
        # Build WHERE clause
        where_conditions = ['year = ?', 'is_valid = 1',  """callsign IS NOT ?"""]
        params = [year, BONUS_CALLSIGN]
        
        for and_clause in ands:
            if len(and_clause) == 2:
                # Simple equality: [field, value]
                field, value = and_clause
                where_conditions.append(f"{field} = ?")
                params.append(value)
            elif len(and_clause) == 3:
                # Custom operator: [field, operator, value]
                field, operator, value = and_clause
                where_conditions.append(f"{field} {operator} ?")
                params.append(value)
            elif len(and_clause) == 1:
                where_conditions.append(and_clause[0])  # Raw SQL condition
            else:
                raise ValueError(f"Invalid AND clause: {and_clause} (must be 2 or 3 elements)")
        
        where_clause = ' AND '.join(where_conditions)
        
        # Build complete query (always ordered by final_score DESC)
        sql = f"""
            SELECT {select_clause}
            FROM contest_results
            WHERE {where_clause}
            ORDER BY final_score DESC
        """
        
        return sql, params


# Convenience function
def generate_leaderboards(year: str, leaderboards_config: List, 
                         rankings_dict: Dict = None,
                         save_rankings: bool = True,
                         db_path: str = DATABASE_FILE) -> List[Dict]:
    """
    Generate leaderboards for a year.
    
    Args:
        year: Contest year
        leaderboards_config: LEADERBOARDS configuration from config.py
        rankings_dict: RANKINGS dict from config.py (maps codes to descriptions)
        save_rankings: If True, save individual rankings to database
        db_path: Path to database file
        
    Returns:
        List of sections with tables
    """
    generator = LeaderboardGenerator(db_path)
    return generator.generate_leaderboards(year, leaderboards_config, 
                                          rankings_dict, save_rankings)


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


#!/usr/bin/env python3
"""
Louisiana QSO Party - Database Module

Handles storing and retrieving contest results in SQLite database.
Records are keyed by year and callsign (composite key).
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from config.config import DATABASE_FILE


class ContestDatabase:
    """Manages contest results in SQLite database"""
    
    def __init__(self, db_path: str = 'laqp.db'):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create tables if they don't exist
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Main results table - keyed by year and callsign
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contest_results (
                    year TEXT NOT NULL,
                    callsign TEXT NOT NULL,
                    name TEXT,
                    club TEXT,
                    exchange TEXT,
                    overlay TEXT,
                    location_type TEXT,
                    dxcc_code INTEGER,
                    dxcc_entity TEXT,
                    mode_category TEXT,
                    power_level TEXT,
                    final_score INTEGER,
                    qso_points INTEGER,
                    total_qsos INTEGER,
                    valid_qsos INTEGER,
                    total_multipliers INTEGER,
                    counties_worked TEXT,
                    counties_worked_multiplier INTEGER,
                    states_worked TEXT,
                    states_worked_multiplier INTEGER,
                    provinces_worked TEXT,
                    provinces_worked_multiplier INTEGER,
                    dx_worked TEXT,
                    dx_worked_multiplier INTEGER,
                    counties_activated TEXT,
                    rover_bonus_points INTEGER,
                    worked_n5lcc INTEGER,
                    num_n5lcc_contacts INTEGER,
                    qsos_by_band TEXT,
                    qsos_by_mode TEXT,
                    qsos_by_hour TEXT,
                    bands_worked TEXT,
                    claimed_score INTEGER,
                    errors TEXT,
                    warnings TEXT,
                    is_valid INTEGER,
                    qsos TEXT,
                    rankings TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    PRIMARY KEY (year, callsign)
                )
            ''')
            
            # Create indexes for common queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_year 
                ON contest_results(year)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_location_type 
                ON contest_results(year, location_type)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_mode_category 
                ON contest_results(year, mode_category)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_score 
                ON contest_results(year, final_score DESC)
            ''')
            
            conn.commit()
    
    def _serialize_result(self, result: Dict, contest_year: str) -> Dict:
        """
        Convert result dict to database-storable format.
        Converts sets to JSON lists, handles complex types.
        """
        db_result = {}
        
        # Simple fields
        simple_fields = [
            'year', 'callsign', 'name', 'club', 'exchange', 'overlay',
            'location_type', 'dxcc_code', 'dxcc_entity', 'mode_category', 'power_level',
            'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
            'total_multipliers', 'counties_worked_multiplier',
            'states_worked_multiplier', 'provinces_worked_multiplier',
            'dx_worked_multiplier', 'mobile_bonus_points',
            'num_n5lcc_contacts', 'claimed_score'
        ]
        
        for field in simple_fields:
            db_result[field] = result.get(field, None)
        
        # Boolean fields (convert to 0/1)
        bool_fields = [
            'worked_n5lcc',
              'is_valid'
        ]
        
        for field in bool_fields:
            value = result.get(field, False)
            db_result[field] = 1 if value else 0
        
        # Set fields (convert to JSON lists)
        set_fields = [
            'counties_worked', 'states_worked', 'provinces_worked',
            'dx_worked', 'counties_activated', 'bands_worked'
        ]
        
        for field in set_fields:
            value = result.get(field, set())
            db_result[field] = json.dumps(sorted(list(value)))
        
        # Dict/list fields (convert to JSON)
        json_fields = [
            'qsos_by_band', 'qsos_by_mode', 'qsos_by_hour', 'qsos'
        ]
        
        for field in json_fields:
            value = result.get(field, {})
            # Convert sets in dict values to lists
            db_result[field] = json.dumps(value)
        
        # List fields (convert to JSON)
        db_result['errors'] = json.dumps(result.get('errors', []))
        db_result['warnings'] = json.dumps(result.get('warnings', []))

        # QSOs field (NEW - ADD THIS)
        db_result['qsos'] = json.dumps(result.get('qsos', []))
        
        # Rankings field (empty dict initially)
        db_result['rankings'] = json.dumps(result.get('rankings', {}))
        
        # Timestamps
        now = datetime.utcnow().isoformat()
        db_result['created_at'] = now
        db_result['updated_at'] = now
        
        return db_result
    
    def _deserialize_result(self, row: tuple, columns: List[str]) -> Dict:
        """
        Convert database row to result dict.
        Converts JSON back to Python objects.
        """
        result = {}
        
        # Convert row to dict
        for i, col in enumerate(columns):
            result[col] = row[i]
        
        # Convert boolean fields back
        bool_fields = [
            'worked_n5lcc',
            'is_valid'
        ]
        
        for field in bool_fields:
            if field in result:
                result[field] = bool(result[field])
        
        # Convert JSON back to Python objects
        json_fields = [
            'counties_worked', 'states_worked', 'provinces_worked',
            'dx_worked', 'counties_activated', 'bands_worked',
            'qsos_by_band', 'qsos_by_mode', 'qsos_by_hour',
            'errors', 'warnings', 'rankings', 'qsos'
        ]
        
        for field in json_fields:
            if field in result and result[field]:
                try:
                    result[field] = json.loads(result[field])
                    
                    # Convert lists back to sets where appropriate
                    if field in ['counties_worked', 'states_worked', 
                               'provinces_worked', 'dx_worked', 
                               'counties_activated', 'bands_worked']:
                        result[field] = set(result[field])

                except json.JSONDecodeError:
                    result[field] = [] if field in ['errors', 'warnings'] else {}
        
        return result
    
    def save_result(self, contest_year: str, result: Dict) -> bool:
        """
        Save or update a contest result.
        
        If a record exists for (year, callsign), it will be replaced.
        
        Args:
            result: Result dictionary from processor
            
        Returns:
            True if saved successfully
        """
        # Ensure year is present
        if 'year' not in result or (not result['year']) or result['year'] != contest_year:
            raise ValueError("Result must include 'year' field")
        
        if 'callsign' not in result or not result['callsign']:
            raise ValueError("Result must include 'callsign' field")
        
        # Serialize result
        db_result = self._serialize_result(result, contest_year)
        
        # Build SQL
        fields = list(db_result.keys())
        placeholders = ','.join(['?' for _ in fields])
        field_names = ','.join(fields)
        
        # Use INSERT OR REPLACE to overwrite existing records
        sql = f'''
            INSERT OR REPLACE INTO contest_results ({field_names})
            VALUES ({placeholders})
        '''
        
        values = [db_result[field] for field in fields]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving result: {e}")
            return False
    
    def get_result(self, year: str, callsign: str) -> Optional[Dict]:
        """
        Get a single result by year and callsign.
        
        Args:
            year: Contest year
            callsign: Station callsign
            
        Returns:
            Result dict or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM contest_results
                WHERE year = ? AND callsign = ?
            ''', (year, callsign.upper()))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return self._deserialize_result(row, columns)
            return None
    
    def update_rankings(self, year: str, rankings_dict: Dict[str, Dict[str, int]]):
        """
        Update rankings for all results in a year.
        
        Args:
            year: Contest year
            rankings_dict: Dict mapping callsign to their rankings
                          e.g., {'K5ABC': {'overall': 1, 'cw': 3}, ...}
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for callsign, rankings in rankings_dict.items():
                rankings_json = json.dumps(rankings)
                updated_at = datetime.utcnow().isoformat()
                
                cursor.execute('''
                    UPDATE contest_results
                    SET rankings = ?, updated_at = ?
                    WHERE year = ? AND callsign = ?
                ''', (rankings_json, updated_at, year, callsign.upper()))
            
            conn.commit()
    
    def get_statistics(self, year: str) -> Dict:
        """
        Get contest statistics for a year.
        
        Args:
            year: Contest year
            
        Returns:
            Dict with statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total logs
            cursor.execute('''
                SELECT COUNT(*) FROM contest_results
                WHERE year = ? AND callsign IS NOT 'N5LCC
            ''', (year,))
            total_logs = cursor.fetchone()[0]
            
            # Valid logs
            cursor.execute('''
                SELECT COUNT(*) FROM contest_results
                WHERE year = ? AND is_valid = 1 AND callsign IS NOT 'N5LCC
            ''', (year,))
            valid_logs = cursor.fetchone()[0]
            
            # Total QSOs
            cursor.execute('''
                SELECT SUM(total_qsos) FROM contest_results
                WHERE year = ? AND is_valid = 1 AND callsign IS NOT 'N5LCC
            ''', (year,))
            total_qsos = cursor.fetchone()[0] or 0
            
            # Top score
            cursor.execute('''
                SELECT callsign, final_score FROM contest_results
                WHERE year = ? AND is_valid = 1 AND callsign IS NOT 'N5LCC
                ORDER BY final_score DESC
                LIMIT 1
            ''', (year,))
            top_result = cursor.fetchone()
            
            return {
                'year': year,
                'total_logs': total_logs,
                'valid_logs': valid_logs,
                'invalid_logs': total_logs - valid_logs,
                'total_qsos': total_qsos,
                'top_callsign': top_result[0] if top_result else None,
                'top_score': top_result[1] if top_result else 0
            }


# Convenience functions

def save_result(result: Dict, contest_year: str, db_path: str = DATABASE_FILE) -> bool:
    """
    Save a result to the database.
    
    Args:
        result: Result dictionary from processor
        db_path: Path to database file
        
    Returns:
        True if saved successfully
    """
    db = ContestDatabase(db_path)
    return db.save_result(contest_year, result)


def get_result(year: str, callsign: str, db_path: str = DATABASE_FILE) -> Optional[Dict]:
    """
    Get a result from the database.
    
    Args:
        year: Contest year
        callsign: Station callsign
        db_path: Path to database file
        
    Returns:
        Result dict or None if not found
    """
    db = ContestDatabase(db_path)
    return db.get_result(year, callsign)


if __name__ == "__main__":
    print("LAQP Database Module")
    print("This module should be imported, not run directly.")
    print()
    print("Usage:")
    print("  from database import ContestDatabase, save_result, get_result")
    print()
    print("  # Save a result")
    print("  save_result(result)")
    print()
    print("  # Get a result")
    print("  result = get_result('2026', 'K5ABC')")

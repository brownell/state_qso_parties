#!/usr/bin/env python3
"""
Louisiana QSO Party - Database Module

Handles storing and retrieving contest results in SQLite database.
Records are keyed by year and callsign (composite key).
"""
'''
Fields in CAB object
['address', 'address_city', 'address_country', 'address_postalcode', 'address_state_province', 'callsign', 'category_assisted', 'category_band', 'category_mode', '****category_operator', 'category_overlay', 'category_power', 'category_station', 'category_time', 'category_transmitter', 'certificate', 'claimed_score', 'club', 'contest', 'created_by', 'email', 'grid_locator', 'hq_anything', 'ignore_order', 'location', 'name', 'offtime', 'operators', 'qso', 'soapbox', 'version', 'x_anything']
PLUS fields added by us:
    'cat', 'category'
'''

'''Fields in QSO object
['date', 'de_call', 'de_exch', 'dx_call', 'dx_exch', 'freq', 'mo', 't', 'valid']
'''

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from config.config import DATABASE_FILE

class ContestDatabase:
    """Manages contest results in SQLite database"""
    
    def __init__(self, db_path: str = 'txqp.db'):
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
                    location TEXT,
                    dxcc_code INTEGER,
                    dxcc_entity TEXT,
                    mode TEXT,
                    power TEXT,
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
                    mobile_bonus_points INTEGER,
                    worked_special_station INTEGER,
                    qsos_by_band TEXT,
                    qsos_by_mode TEXT,
                    qsos_by_hour TEXT,
                    bands_worked TEXT,
                    grid_square TEXT,
                    claimed_score INTEGER,
                    errors TEXT,
                    warnings TEXT,
                    is_valid INTEGER,
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
                ON contest_results(year, location)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_mode_category 
                ON contest_results(year, mode)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_score 
                ON contest_results(year, final_score DESC)
            ''')

        #  # QSO  results table - keyed by year and callsign
        #     cursor.execute('''
        #         CREATE TABLE IF NOT EXISTS qsos (
        #         qso_date_time INTEGER,
        #         de_call TEXT, 
        #         de_exc TEXT,
        #         dx_call TEXT,
        #         dx_exch TEXT,
        #         freq TEXT,
        #         mo TEXT
        #         valid BOOLEAN,
        #         PRIMARY KEY (year, callsign)
        #         )
        #     ''')

        # # Create indexes for common queries
        #     cursor.execute('''
        #         CREATE INDEX IF NOT EXISTS idx_year 
        #         ON qsos(year)
        #     ''')
            
        #     cursor.execute('''
        #         CREATE INDEX IF NOT EXISTS idx_location_type 
        #         ON qsos(year, location)
        #     ''')
            
        #     cursor.execute('''
        #         CREATE INDEX IF NOT EXISTS idx_mode_category 
        #         ON qsos(year, mode)
        #     ''')
            
        #     cursor.execute('''
        #         CREATE INDEX IF NOT EXISTS idx_score 
        #         ON qsos(year, final_score DESC)
        #     ''')
            
            conn.commit()
    
    def _serialize_result(self, result: Dict, contest_year: str) -> Dict:
        """
        Adds simple fields from the "result" object
        Adds attributes of the "CAB" objext
        Convert result dict to database-storable format.
        Convert lists to JSONF
        Converts sets to JSON lists, handles complex types.
        """
        db_result = {}
        cab = result['cab']
        
        ##### RESULT SIMPLE FIELDS
        simple_fields = [  # from the result object
            'year', 'callsign', 'dxcc_code', 'dxcc_entity',
            'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
            'total_multipliers', 'mobile_bonus_points', 'cw_qsos',
            'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus'
            'special_station_contacts', 'claimed_score', 'uniques', 'nils',
            'busteds', 'dup_qsos'
        ]
        for field in simple_fields:
            db_result[field] = result.get(field, None)

        ##### CAB SIMPLE FIELDS
        cab_attributes = [
            'club', 'name', 'location', 'name', 'category_band', 'email',
            'category_mode', 'category_power', 'category_station', 'cat', 'category'
        ]
        for field in cab_attributes:
             db_result[field] = getattr(field, None)
        
        ##### SET FIELDS (convert to JSON lists)
        set_fields = [
            'counties_worked', 'states_worked', 'provinces_worked',
            'dx_worked', 'counties_activated', 'bands_worked'
        ]
        for field in set_fields:
            value = result.get(field, set())
            db_result[field] = json.dumps(sorted(list(value)))
        
        ###### DICT FIELDS  (convert to JSON)
        json_fields = [
            'qsos_by_band', 'qsos_by_mode', 'de_exch_rcvd'
        ]
        for field in json_fields:
            value = result.get(field, {})
            # Convert sets in dict values to lists
            db_result[field] = json.dumps(value)
        
        # List fields (convert to JSON)
        db_result['errors'] = json.dumps(result.get('errors', []))
        db_result['warnings'] = json.dumps(result.get('warnings', []))
        db_result['qsos_by_hour'] = json.dumps(result.get('qsos_by_hour', []))
        
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
    print("TXQP Database Module")
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

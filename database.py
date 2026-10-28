#!/usr/bin/env python3
"""
Texas QSO Party - Database Module

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
from datetime import datetime, timezone
from share import SHARED as s
from config.config import DATABASE_FILE, DB_DROP
from config.config_txqp import RANKINGS

def create_tables():
    """Create database tables if they don't exist"""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        
        # Main results table - keyed by year and callsign
        # While debugging
        # if DB_DROP and db.drop_db:
        #     db.drop_db = False
        #     cursor.execute('''DROP TABLE IF EXISTS contest_results''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contest_results (
                callsign TEXT NOT NULL,
                year TEXT NOT NULL,
                name TEXT,
                email TEXT,
                club TEXT,
                exchange TEXT,
                overlay TEXT,
                location TEXT,
                dxcc_code INTEGER,
                dxcc_entity TEXT,
                category_mode TEXT,
                category_power TEXT,
                category_band TEXT,
                category_station TEXT,
                cat TEXT,
                final_score INTEGER,
                cw_qsos INTEGER,
                ph_qsos INTEGER,
                dg_qsos INTEGER,
                ry_qsos INTEGER,
                qso_points INTEGER,
                total_qsos INTEGER,
                valid_qsos INTEGER,
                total_multipliers INTEGER,
                uniques INTEGER,
                nils INTEGER,
                nil_calls TEXT,
                busteds INTEGER,
                busted_calls TEXT,
                dup_qsos INTEGER,
                other_invalid_qsos  INTEGER,
                counties_worked TEXT,
                states_worked TEXT,
                provinces_worked TEXT,
                dx_worked TEXT,
                de_exch_rcvd TEXT,
                dx_exch_sent TEXT,
                counties_activated TEXT,
                special_station_contacts INTEGER,
                score_wo_bonus INTEGER,
                mobile_activation_counts TEXT,
                worked_counties_mobile TEXT,
                cab_mobile_points INTEGER,
                mtb_mobile_points INTEGER,
                mobile_counties_worked TEXT,
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
                category_rank INTEGER,
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
            CREATE INDEX IF NOT EXISTS idx_cat 
            ON contest_results(year, cat)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_club 
            ON contest_results(year, club)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_score 
            ON contest_results(year, final_score DESC)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contest_stats (
                year TEXT NOT NULL,
                stats TEXT,
                PRIMARY KEY (year)
            )
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
    #         CREATE INDEX IF NOT EXISTS idx_category_mode 
    #         ON qsos(year, category_mode)
    #     ''')
        
    #     cursor.execute('''
    #         CREATE INDEX IF NOT EXISTS idx_score 
    #         ON qsos(year, final_score DESC)
    #     ''')
        
        conn.commit()

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

        self.drop_db = True

        self.field_types = {'integer': 0, 'string': '',
                            'set': set(), 'list': [], 'dict': {}, 'cab': ''}
        self.result_fields = {'integer': [
            'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
            'total_multipliers', 'cab_mobile_points', 
            'mtb_mobile_points', 'cw_qsos',
            'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
            'special_station_contacts', 'claimed_score', 'uniques', 'nils',
            'busteds', 'dup_qsos', 'category_rank', 
            'other_invalid_qsos'
        ],
        'string': [  # from the result object
            'year',   'dxcc_entity'
        ],
        'set': [ 'states_worked', 'provinces_worked',
            'de_exch_rcvd', 'dx_exch_sent', 'bands_worked', 
            'counties_worked', 'dx_worked', 'counties_activated'
        ],
        'list': ['errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls'],
        'cab': [
            'club', 'name', 'location', 'name', 'category_band', 'email', 'callsign',
            'category_mode', 'category_power', 'category_station', 
            'cat', 'claimed_score', 'category_power', 'category_station', 'callsign',
        ],
        'dict': ['qsos_by_band', 'qsos_by_mode','mobile_activation_counts', 'worked_counties_mobile', 'mobile_counties_worked']
        }
        self.stats_fields = {
            'integer': ['total_logs', 'rejected_logs', 'dx_logs', 'us_logs', 'cdn_logs', 'tx_mobile_logs', 'tx_fixed_logs', 'unclassed_logs', 'total_qsos', 'valid_qsos', 'qsos_with_tx', 'qsos_with_us', 
                        'qsos_with_canada', 'qsos_with_dx', 'duplicate_qsos', 'nils', 'busteds', 'other_invalid_qsos', 'uniques'],
            'string': ['year'],  # from the result object 
            'list': ['rejected_logs_filenames', 'qsos_by_hour', 'nil_calls', 'busted_calls'],
            'dict': ['qsos_by_band', 'qsos_by_mode', 'mobile_activation_counts', 'worked_counties_mobile'],
            'set': ['counties_worked', 'states_worked', 'provinces_worked', 'dx_worked', 'counties_activated'],
            'cab': []  # placeholder so serial deserial can do both types
        }
    
    def _serialize_result(self, result: Dict, field_types: Dict, fields: Dict) -> Dict:
        """
        Adds simple fields from the "result" object
        Adds attributes of the "CAB" objext
        Convert result dict to database-storable format.
        Convert lists to JSONF
        Converts sets to JSON lists, handles complex types.
        """
        db_result = {}
        cab = result.get('cab', None)
        try:
            # put values from the above listed fields into db_result
            for typ in list(field_types.keys()):
                if typ == 'set':
                    for fld in fields[typ]:
                        value = result.get(fld, field_types[typ])
                        db_result[fld] = json.dumps(sorted(list(value)))

                elif typ == 'list':
                    for fld in fields[typ]:
                        value = result.get(fld, field_types[typ])
                        db_result[fld] = json.dumps(list(value))

                elif typ in ['integer', 'string']:
                    for fld in fields[typ]:
                        db_result[fld] = result.get(fld, field_types[typ])
           
                elif typ == 'dict':
                    for fld in fields[typ]:
                        value = result.get(fld, {})
                        # Convert sets in dict values to lists
                        for k in list(value.keys()):
                            if isinstance(value[k], set):
                                value[k] = list(value[k])
                        db_result[fld] = json.dumps(value)

                elif typ == 'cab':
                    flds = fields.get(typ, [])
                    for fld in flds:
                        db_result[fld] = getattr(cab, fld, '')
            
            # Timestamps
            now =  datetime.now(timezone.utc).isoformat()
            db_result['created_at'] = now
            db_result['updated_at'] = now
        except Exception as e:
            s.stats['exceptions'].append(f"serialize result: {result['callsign']}: {e}")
            print(f"exception {e} in creating db_result")
            # print('BREAK')
        return db_result
    
    def _deserialize_result(self, result: Dict, field_types: Dict, fields: Dict) -> Dict:
        """ The opposite of serialize_result
            Reads data from the databaser one operator record
            Adds simple fields from the "result" object
            Adds attributes of the "CAB" objext
            Convert result dict to JSON-usable format.
            Convert lists to JSON
            Converts sets to JSON lists, handles complex types.
            """
        if result:
            display_result = {}
            try:
                for typ in list(field_types.keys()):
                # INTEGERS AND STRINGS
                    if typ in ['integer', 'string']:
                        for fld in fields[typ]:
                            display_result[fld] = result.get(fld, field_types[typ])

                    # SETS AND LISTS
                    elif  typ in list([ 'set', 'list']):
                        for fld in fields[typ]:
                            display_result[fld] = json.loads(result.get(fld, field_types[typ]))

                    # DICT_FIELDS
                    elif typ == 'dict':
                        for field in fields[typ]:
                            if field in result and result[field]:
                                display_result[field] = json.loads(result[field])

                    # the cab fields saved in the DB are all strings. We are not going to
                    # reconstitute the cab object, but just storing the fiels in display_result
                    elif typ == 'cab_attributes' and len(fields[typ]) > 0:
                        for fld in fields[typ]:
                            display_result[fld] = result.get(fld, '')

                display_result['cat'] = RANKINGS[display_result['cat']]

            except Exception as e:
                s.stats['exceptions'].append(f"de-serialize result: {result['callsign']}: {e}")
                s.out_files['errors'].write(f"could not deserialize {result}\n")
        
        return display_result
    
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
        try:
            if 'year' not in result or result['year'] != contest_year:
                raise ValueError("Result must include 'year' field")
            
            if 'callsign' not in result or not result['callsign']:
                raise ValueError("Result must include 'callsign' field")
        except ValueError as e:
            print(f"ValueError {e} in save_result")
        
        # Serialize result
        db_result = self._serialize_result(result, self.field_types, self.result_fields)
        
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
            s.stats['exceptions'].append(f"save result: {result['callsign']}: {e}")
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
            cursor.execute('''SELECT * FROM contest_results WHERE year = ? AND callsign = ?''', ('2026', callsign.upper()))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                result = {}
                for i, col in enumerate(columns):
                    result[col] = row[i]
                return self._deserialize_result(result, self.field_types, self.result_fields)
                
            return None

    def save_stats(self, s, year, stats):
        db_result = self._serialize_result(stats, self.field_types, self.stats_fields)
                
        # Build SQL
        
        # Use INSERT OR REPLACE to overwrite existing records
        sql = f'''INSERT OR REPLACE INTO contest_stats (year, stats) VALUES (?, ?);'''
        
        values = [year, json.dumps(db_result)]
        s.out_files['debug'].write(json.dumps(db_result))
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit()
            return True
        
        except Exception as e:
            s.stats['exceptions'].append(f"save stats: {s.stats['total_logs']}: {e}")
            print(f"Error saving statistics: {e}")
            return False
           
    def get_stats(self, year: str) -> Dict:
        """  Get contest statistics for a year.
                Args:
                    year: Contest year
                Returns:
                    Dict with statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM contest_stats WHERE year = ?''', (year))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                result = {}
                for i, col in enumerate(columns):
                    result[col] = row[i]
                return self._deserialize_result(result, self.field_types, self.result_fields)
                
        return None

db = ContestDatabase(Path(DATABASE_FILE))
create_tables()
# Convenience functions

def get_clubs_section(s, year):
    db_path = Path(DATABASE_FILE)
    with sqlite3.connect(db_path, timeout=20.0) as conn:
        sql = '''SELECT
                club,
                COUNT(*) AS person_count,
                SUM(final_score) AS total_score
                FROM contest_results
                WHERE club IS NOT NULL
                GROUP BY club
                ORDER BY total_score DESC;'''
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit
        all_clubs = cursor.fetchall()
        rows = []
        j = 1
        for i, t in enumerate(all_clubs):
            rows.append([j] + list(all_clubs[i]))
            j += 1

        sections =  [
            {
                'section_title': 'Clubs Summary Results',
                'tables': [
                    {
                    'title': '',
                    'headers': ['Rank', 'Club', 'Entries', 'Score'],
                    'rows': rows
                    }
                ]
            },
            {
                'section_title': 'Results By Club',
                'tables': []
            }
        ]

        
        for club in all_clubs:
            sql = '''
                    select callsign,  final_score, club
                        from contest_results
                        where club = ?
                        order by final_score DESC; '''
            val = list(club)[0]
            cursor = conn.cursor()
            cursor.execute(sql, [val])
            conn.commit
            temp = cursor.fetchall()
            rows = []
            j = 1
            for i, t in enumerate(temp):
                if int(list(temp[i])[2]) == 1:
                    break
                rows.append([j] + list(temp[i])[:-1])
                j += 1

            table = {
                'title': f"Results for {club[0]}",
                'headers': ['Rank',  'Entries', 'Total Score'],
                'rows': rows
                }

            sections[1]['tables'].append(table)

    return sections

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
    db.drop_db = False
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
    db.drop_db = False
    return db.get_result(year, callsign)

def save_stats(s, contest_year: str, result: Dict, db_path: str = DATABASE_FILE) -> bool:
    """
    Save a result to the database.
    
    Args:
        result: Result dictionary from processor
        db_path: Path to database file
        
    Returns:
        True if saved successfully
    """
    db = ContestDatabase(db_path)
    db.drop_db = False
    return db.save_stats(s, contest_year, result)

def get_stats(year: str, db_path: str = DATABASE_FILE) -> Dict:
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
    db.drop_db = False
    return db.get_stats(year)

# def store_rankings(year: str):
#     db = ContestDatabase(DATABASE_FILE)
#     db.drop_db = False
#     return db.store_rankings(year)

# def store_rankings(self, year):
#     """
#     Store rankings for all results in a year.
    
#     Args:
#         year: Contest year
#     """
#     with sqlite3.connect(self.db_path, timeout=20.0) as conn:
#         cursor = conn.cursor()
#         sql = f'''
#             WITH ranked AS (
#                 SELECT year, callsign, ROW_NUMBER() OVER (ORDER BY final_score DESC) AS calculated_rank
#                 FROM contest_results
#                 WHERE year = ? AND cat = ?
#             )
#             UPDATE contest_results
#             SET category_rank = ranked.calculated_rank
#             FROM ranked
#             WHERE contest_results.year = ranked.year
#             AND contest_results.callsign = ranked.callsign;
#         '''
#         for c in list(RANKINGS.keys()):
#             try:
#                 cursor = conn.cursor()
#                 cursor.execute(sql, [year, c])
#                 conn.commit
#                 continue
#             except Exception as e:
#                 print(f"***** ERROR could not set category for cat {c}")
#                 print(f"***** EXCEPTION saving result: {e}")
#                 return False
# stats_fields = {
#     ""
# }


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

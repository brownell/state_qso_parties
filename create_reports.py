''' Creates both the individual operator reports with certificate, 
and the aggregate final report with rankings in each of the categories   
When the web visitor goes to the HTML shells for both reports are
presented in the response page. If the visitor chooses an individual
report, the data is sent from the server as JSON and javascript
is used to insert it into the HTML shell. If the visitor chooses
the aggregate final report, the HTML for it has already been created
and the web app simply reads the HTML from a stored file and sends
it to the browser where javascript inserts it into the page'''


import sqlite3
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
from share import SHARED as s
from database import deserialize_result

from config.config import DATABASE_FILE, CONTEST_YEARS
from config.config_txqp import RANKINGS, LEADERBOARDS

''' Gets the data for an individual from the database and returns
    the results in a format that can easily be converted to JSON.
    This function is ONLY CALLED by the Web app. It is not used
    in the batch app.   '''

db_path = Path(DATABASE_FILE)
db_path.parent.mkdir(parents=True, exist_ok=True)

def get_individual_result(year: str, callsign: str) -> Dict:
    # check arguments
    if not (type(year) != str and year in CONTEST_YEARS and callsign):
        print(f"ERROR: year and  or callsign not valid")
    else:
        # query the database and validate good results
        sql = '''Select * from contest_results
                    where year = '?' and callsign = '?';
                '''
        values = [year, callsign]
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit()
            return True
        except Exception as e:
            print(f"Error getting result: {e}")
            return False

        return deserialize_result(dict(row))

        
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

    # return the Dict to the web app

''' Gets the data for one category from the database and returns
    the results in a format that can easily be converted to JSON.
    This function is ONLY CALLED by the Web app. It is not used
    in the batch app.
    '''

def get_category_data(year: str, category: str) -> Dict:
    # check arguments
    if type(year) != str and year in list(RANKINGS.keys()):

        pass



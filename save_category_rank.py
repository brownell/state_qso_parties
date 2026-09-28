############################################
# For each user the category_rank is the 
# operator's rank in the category operated in
############################################


import sqlite3
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
from config.config import DATABASE_FILE
from config.config_txqp import RANKINGS

def save_all_ranks(year: str):

    db_path = Path(DATABASE_FILE)
    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    for cat in list(RANKINGS.keys()):
        sql = f'''
            WITH ranked AS (
                SELECT year, callsign, ROW_NUMBER() OVER (ORDER BY final_score DESC) AS calculated_rank
                FROM contest_results
                WHERE year = 2026 AND cat = '{cat}'
            )
            UPDATE contest_results
            SET category_rank = ranked.calculated_rank
            FROM ranked
            WHERE contest_results.year = ranked.year
            AND contest_results.callsign = ranked.callsign;
        '''

        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                print(f"SAVED cat: {cat}")
            continue
        except Exception as e:
            print(f"***** ERROR could not set category for cat {cat}")
            print(f"***** EXCEPTION saving result: {e}")
            return False
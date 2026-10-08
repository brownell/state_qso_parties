from pathlib import Path
import sqlite3
from config.config_txqp import RANKINGS, RANK_TABLES
from config.config import DATABASE_FILEtry:
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

SCRIPT_DIR = Path(__file__).resolve().parent

print(type(RANK_TABLES))

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
        print('DONE')


save_all_rankings()
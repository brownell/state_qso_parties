"""
State QSO Party - Configuration
Application logic and contest rules (NOT secrets/credentials)

This file must be copied to config.py to do a run as TQP

NOTE: set up for Windows dev and deployment
"""
import os

from pathlib import Path

# Load environment variables from .env file (for local development)
# In production (Fly.io), environment variables are already set
try:
    from dotenv import load_dotenv
    # Find .env file in parent directory
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # dotenv not installed (production), that's OK
    pass


# ============================================================================
# ENVIRONMENT VARIABLES (read from .env)
# ============================================================================

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in environment!")

FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
CONTEST_NAME = os.environ.get('CONTEST_NAME', False)
CONTEST_YEAR = os.environ.get('CONTEST_YEAR', False)


# ============================================================================
# REFERENCE DATA FILES
# Reference data (from repo, in /app/)
# ============================================================================
# 
REFERENCE_DATA_DIR = os.environ.get('REFERENCE_DATA_DIR', '/app/reference_data')
# Reference files
COUNTIES_FILE = REFERENCE_DATA_DIR + '/counties.txt'
STATES_FILE = REFERENCE_DATA_DIR + '/states.txt'
PROVINCES_FILE = REFERENCE_DATA_DIR + '/provinces.txt'
COUNTRY_FILE = REFERENCE_DATA_DIR + '/cty.plist'
DXCC_ENTITIES_FILE = REFERENCE_DATA_DIR + '/dxcc_entities.csv'
QRZ_CALLSIGN=os.environ.get('QRZ_CALLSIGN')
QRZ_PASSWORD=os.environ.get('QRZ_PASSWORD')


# ============================================================================
# PERSISTENT DATA FILES
# User data (on volume, in /data/)
# ============================================================================
BATCH_INPUT_DIR = os.environ.get('BATCH_INPUT_DIR', '/data/batch_input')
DATABASE_FILE = os.environ.get('DATABASE_FILE', '/data/database/tqp.db')
FINAL_REPORTS_DIR = os.environ.get('FINAL_REPORTS_DIR', '/data/final_reports')

# ============================================================================
# CONTEST CONFIGURATION
# ============================================================================

# Available years for results lookup
CONTEST_YEARS = os.environ.get('CONTEST_YEARS', '2025').split(',')
CONTEST_YEAR = os.environ.get('CONTEST_YEAR', '2026')

COUNTIES_ACTIVATED_POINTS = 1000 # each county
COUNTIES_WORKED_POINTS = 500 # per 5 QSOs
MOBILE_REQUIRED_QSOS = 5

# Log file extensions allowed for upload
ALLOWED_LOG_EXTENSIONS = {'log', 'txt', 'cbr'}

# Scoring rules
POINTS = {
    'TX': {
        'CW': 3,
        'PH': 2,
        'DG': 3,
        'RY': 3
    },
    'NTX': {
        'CW': 3,
        'PH': 2,
        'DG': 3,
        'RY': 3,
        "mobile_bonus": 500
    }
}



# Bonus points
BONUS_CALLSIGN = 'xxxxx'  # Bonus for working N5LCC (Louisiana Contest Club)
CALLSIGN_BONUS_POINTS = 100  # Bonus for working N5LCC (Louisiana Contest Club)
ROVER_COUNTY_BONUS = 50  # Bonus per county activated (rovers only)
EXTRA_BONUS_CALLS = os.environ.get('EXTRA_BONUS_CALLS', ['KI5ZAW', 'N5SCJ', 'K5TD'])
EXTRA_BONUS_YEAR = os.environ.get('EXTRA_BONUS_YEAR', '2026')
HQ_FIELDS = os.environ.get('HQ_FIELDS', {})

# ============================================================
# for fuzzy matching of callsigns during cross-checking, we can use the Levenshtein distance to allow for minor typos. For example, if two callsigns differ by only one character (e.g., K5TD vs K5T0), we can consider them a match for cross-checking purposes. This helps catch common errors while still allowing for some flexibility in the logs.
# ============================================================
ENABLE_FUZZY_MATCHING = False  # Check for callsign errors
MAX_EDIT_DISTANCE = 2  # Maximum character differences for fuzzy matching (e.g.,

# ============================================================
# MAPPING of HQ fields added to log by Bruce Horn's uploader
# ============================================================



# ============================================================
# BAND AND MODE DEFINITIONS
# ============================================================

# need to convert freq in KHz to band
# Band frequency ranges (in kHz) - tuples of (min, max) for each band
BAND_RANGES = {
    160: (1800, 2000),      # 160m: 1.8 - 2.0 MHz
    80:  (3500, 4000),      # 80m:  3.5 - 4.0 MHz
    40:  (7000, 7300),      # 40m:  7.0 - 7.3 MHz
    20:  (14000, 14350),    # 20m:  14.0 - 14.35 MHz
    15:  (21000, 21450),    # 15m:  21.0 - 21.45 MHz
    10:  (28000, 29700),    # 10m:  28.0 - 29.7 MHz
    6:   (50000, 54000),    # 6m:   50.0 - 54.0 MHz
    2:   (144000, 148000),  # 2m:   144.0 - 148.0 MHz
}

# Phone modes (for scoring)
PHONE_MODES = ['PH', 'FM', 'SSB', 'LSB', 'USB']

# CW/Digital modes (for scoring)
CW_DIGITAL_MODES = ['CW/DIGITAL', 'CW', 'RY', 'DIG', 'RTTY', 'FT8', 'FT4']

# ============================================================================
# CATEGORIES
# ============================================================================

# Log value options
POWER_VALUE_OPTIONS = ('QRP', 'LOW', 'HIGH')
STATION_VALUE_OPTIONS = ('FIXED', 'PORTABLE', 'MOBILE', 'ROVER')
OVERLAY_VALUE_OPTIONS = ('WIRES', 'TB-WIRES', 'POTA')

# ============================================================
# US AND CANADIAN PREFIXES and Provinces
# ============================================================

US_PREFIXES = [
    'K', 'W', 'N', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK',
    'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KV', 'KW', 'KX', 'KY', 'KZ',
    'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY', 'NZ',
    'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL', 'WM', 'WN', 'WO', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WU', 'WV', 'WW', 'WX', 'WY', 'WZ'
]

CANADIAN_PREFIXES = [
    'VA', 'VE', 'VY', 'VO', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CY', 'CZ',
    'XJ', 'XK', 'XL', 'XM', 'XN', 'XO'
]

PROVINCES = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']

# ============================================================================
# for cross-checkiing time strings, we want to allow for some flexibility (e.g., 232034 vs 23:20) and also handle day rollover (e.g., 23:55 vs 00:25 the next day). The key is to parse both times into datetime objects and then compare them with a tolerance.
# ============================================================================

TIME_WINDOW_MINUTES = 60  # ±60 minutes for time matching
ENABLE_FUZZY_MATCHING = True  # Check for callsign errors
MAX_EDIT_DISTANCE = 2  # Maximum character differences for fuzzy matching

# # ============================================================================
# # Admin settings
# # ============================================================================
HQ_FIELDS = {
    'Loc': 'location',
    'Pwr': "category_power",
    "Ops": "category_operator",
    "Mode": "category_mode",
    "Station": 'category_station'
}
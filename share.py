
from typing import Dict, List, Set, Optional
import csv
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from collections import defaultdict
from config.config import (
    CONTEST_YEAR,
    BONUS_CALLSIGN, COUNTIES_FILE, BATCH_INPUT_DIR, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, 
    STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS,
    US_PREFIXES, CANADIAN_PREFIXES, QRZ_CALLSIGN, QRZ_PASSWORD,
    PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE,
    CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, CONTEST_YEAR,
    PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE
    )
import sys
from pathlib import Path
# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))
input_dir = Path(f"{BATCH_INPUT_DIR}/{CONTEST_YEAR}")

'''
Much of the processing of log files is done with the log data in memory in a large
data structure called results. Each log file is processed and the results are stored in this structure.
The results structure is a list of python dicts, one entry for each log file. 
'''
class SHARED:
    """
    Data and methods shared across the processing of all logs. 
    This includes reference data for counties, states, provinces, and DXCC entities, 
    as well as methods for initializing result dictionaries and tracking 
    the first QTH sent in a log.
    """
    
    def __init__(self):
        """Initialize with reference data files"""
        # Load counties, states, and provinces
        with open(COUNTIES_FILE, 'r') as f:
            self.counties = set(line.strip().upper() for line in f if line.strip())

        with open(STATES_FILE, 'r') as f:
            self.states = set(line.strip().upper() for line in f if line.strip())

        with open(PROVINCES_FILE, 'r') as f:
            self.provinces = set(line.strip().upper() for line in f if line.strip())

        ## create DXCC code (same as ADIF number) to DXCC entity. Needed for DX mults
        self.dxcc_entities = [None] * 750
        with open(DXCC_ENTITIES_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.dxcc_entities[int(row[0])] = row[1].split('  ')[0]
        self.out_files = {
            'error_file': open("ERROR_FILE.txt", "w"),
            'uniques_file': open("UNIQUES_FILE.txt", "w"),
            'busteds_file': open("BUSTEDS_FILE.txt", "w"),
            'nils_file': open("NILS_FILE.txt", "w"),
        }
        
        self.first_call_qth = None  # To track the sent QTH in a log for checking other QSOs against it

        self.results = []  # List to hold results for all logs processed
        '''
            When cross checking, there are four results:
            - QSO has a match in other log
            - NIL - your claimed contact submitted a log, but no matching QSO in it - no points or penalty
            - BUSTED(B) - QSO in contact's log, but something does not match - no points or penalty
            - UNIQUE(U) - claimed contact did not submit a log - points
        '''
        self.stats = {
            'total_logs': 0,
            'valid_logs': 0,
            'rejected_logs': 0,
            'rejected_logs_filenames': [], # logs of PARSER not_valids
            'total_qsos': 0,
            'qso_valids': 0,
            'qso_parser_not_valid': 0,
            'calls_w_not_valid_qsos': set(),
            'nils': 0,
            'nil_calls': [],
            'busteds': 0,
            'busted_calls': [],
            'uniques': 0,
            'dx_log_de_missing': 0,
            'duplicate_qsos': 0,
            'total_multipliers': 0,
            'counties_worked_names': set(),
            'states_worked_names': set(),
            'provinces_worked_names': set(),
            'dx_worked_names': set()
        }
        self.all_callsigns = set()  # To track all callsigns that submitted logs for UNIQUE detection
        self.mobile_callsigns = set() # Track callsigns that have location "mobile"
        self.qso_index_dict = defaultdict(list)
        self.contest_clubs = {"Austin QRP Club": 0, "Baytown Area ARC": 0, "Central Texas DX and Contest Club": 0, "Dallas ARC": 0, "DCT ARC": 0, 
                              "Denton County ARC": 0, "DFW Contest Group": 0, "Ellis County ARC": 0, "Irving ARC": 0, "Lake Area Amateur Radio Club": 0, 
                              "Las Moras ARC": 0, "Longview/East Texas ARC": 0, "McKinney ARC": 0, "Medina County ARC": 0, "Midland ARC": 0,
                              "Naturist ARC": 0, "North Texas ARS": 0, "Panhandle ARC": 0, "Red River Valley ARC": 0, "Road Runners Microwave Group": 0,
                              "Saginaw Haslet ARC": 0, "South Texas DX and Contest Club": 0, "Texas DX Society": 0, "University of Texas ARC": 0, 
                              "West Texas ARC": 0, "West Texas Pemian Network": 0, "Williamson County ARC": 0}
        # non-TX stations working TX mobile stations need to be tracked for bonus points
        self.ntx_bonus = {}

    # One of these is created for each log file
    # Each of the objects in self.results is a python with the following structure:      
    def _init_result(self) -> Dict:
        """Initialize result dictionary with standardized structure"""
        return {
            'callsign': '', #callsign for this log file
            'cab': None,    # the Cabrillo object from the cabrillo.parser
            'header_attribs': {},  # Parsed attributes from Cabrillo header
            'qso_data': [],     # list of dicts, one for each qso
            'year': CONTEST_YEAR,
            'exchange': '',     # from first QSO in this operator's log
            'category': 'NON-LA',  # 'DX', 'NON-LA', 'LA-FIXED', 'LA-ROVER'
            'dxcc_code': 0, # code is 0 if not a DX station, else DXCC code
            'dxcc_entity': '', # if same as callsign if not DX 
            'final_score': 0,
            'cw_qsos': 0,
            'ph_qsos': 0,
            'dg_qsos': 0,
            'ry_qsos': 0,
            'qso_points': 0,
            'total_qsos': 0, # total number validated, whether dups or not
            'valid_qsos': 0, #number of qsos that are not dups and contribute to the score
            'total_multipliers': 0,
            'counties_worked': set(),
            'counties_worked_multiplier': 0,
            'states_worked': set(),
            'states_worked_multiplier': 0,
            'provinces_worked': set(),
            'provinces_worked_multiplier': 0,
            'dx_worked': set(),
            'dx_worked_multiplier': 0,
            'counties_activated': set(),
            'de_exch_rcvd': set(),
            'dx_exch_sent': set(),
            'score_wo_bonus': 0,
            'rover_bonus_points': 0,
            'county_bonus_points': 0,
            'worked_special_station': False,
            'num_n5lcc_contacts': 0,
            'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 0, '15': 0, '10': 0, '6': 0, '2': 0},
            'qsos_by_mode': {'PH': 0, 'CW': 0, 'RY': 0, 'DG': 0},
            'qsos_by_hour': [0] * 24,
            'bands_worked': set(),
            'uniques': 0,
            'nils': 0,
            'busteds': 0,
            'dup_qsos': 0,
            'errors': [],
            'warnings': [],
            'is_valid': True
        }
#END of SHARED class
"""
Texas QSO Party - Specific Configuration
Application logic and contest rules (NOT secrets/credentials)

This file must be at config_txqp.py for TXQP

NOTE: set up for Windows dev and deployment
"""
import os
from datetime import datetime

from pathlib import Path

# contest times
CONTEST_TIMES = [
        {'start': datetime(2026, 9, 19, 14, 0, 0),
         'end': datetime(2026, 9, 20, 2, 0, 0)},
        {'start': datetime(2026, 9, 20, 14, 0, 0),
                 'end': datetime(2026, 9, 21, 2, 0, 0)} 
    ]

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

''' From the rules at https://www.txqp.net/?page_id=23
    # Texas – Fixed Station
    TX SO LP — 'TSL': 'Single Operator Mixed Mode (150 watts power limit)',
    TX SO HP — 'TSH':  'Single Operator Mixed Mode High-Power (>150 watts power)',
    TX MO LP — 'TML':  'Multi Operators (150 watts power limit)',
    TX MO HP — 'TMH':  'Multi Operators High-Power (>150 watts power)',
    TX QRP SO — 'TQS':  'QRP Single Operator (10 watts or less phone and 5 watts or less CW and other modes)',
    TX CWO SO LP — 'TCAL':  'CW Only Single Operator (150 watts power limit)',
    TX CWO SO HP — 'TCSH':  'CW Only Single Operator High-Power (>150 watts power)',
    TX PHO SO LP — 'TPSL':  'Phone Only Single Operator (150 watts power limit)',
    TX PHO SO HP — 'TPSH':  'Phone Only Single Operator High-Power (>150 watts power)',
    
    # Texas – Mobile Stations
    TXM SO — 'TMS':  'Texas Mobile Single Operator Mixed Mode–may be assisted (no contest power limit)',
    TXM MO — 'TMM':  'Texas Mobile Multi Operators (no contest power limit)',
    TXM SO CWO — 'TSC':  'Texas Mobile CW Only Single Operator–may be assisted (no contest power limit)',
    TXM SO PHO — 'TSP':  'Texas Mobile Phone Only Single Operator–may be assisted (no contest power limit)',
    # Note: The spirit of the mobile category is for vehicle-based *or* non-permanent stations who work from multiple counties during the event.',

    # Non-Texas Stations
    NTX SO — 'NS':  'Single Operator Mixed Mode (no contest power limits)',
    NTX SO QRP — 'NSQ':  'QRP Single Operator (10 watts or less phone and 5 watts or less CW and other modes)',
    NTX SO CWO — 'NSC':  'CW Only Single Operator (no contest power limits)',
    NTX SO PHO — 'NSP':  'Phone Only Single Operator (no contest power limits)',
    DX Stations
    DX SO — 'DS':  'Single Operator Mixed (no contest power limits)',
}
'''
'''
['C', 'DS', 'NS', 'NSC', 'NSP', 'NSQ', 'TCSH', 'TCSL', 'TMH', 'TML', 'TMS', 'TMSC', 'TMSP', 'TPSH', 'TPSL', 'TQS', 'TSH', 'TSL']
'''

TX = ['TSL', 'TSH', 'TML', 'TMH', 'TQS', ]
NTX = []
TXM = []
# ============================================================================
# FINAL REPORT TEXT
# ============================================================================

FINAL_REPORT_TXT = """
<p class=final-intro>Congratulations to all participants in the Texas QSO Party!

The Texas DX Society is proud to present the final results.
Thank you for your participation and we look forward to seeing you next year!
73,
Texas DX Society</p>
"""
STATISTICS_TEXT = {
    # LOGS
    'title_logs': 'LOGS',
    'total_logs': 'Total Number of Logs Received',
    'rejected_logs': 'Number of Logs Rejected',
    # Sources of Logs
    'title_log_sources': 'Sources of Logs',
    'us_logs': 'US Non-Texas',
    'cdn_logs': 'Canada',
    'tx_fixed_logs': 'Texas Fixed Logs',
    'tx_mobile_logs': 'Texax Mobile Logs',
    'dx_logs': 'Outside North America',
    'unclassed_logs': 'Unclassified Logs',
    # QSOS
    'title_qsos': 'QSOS',
    'total_qsos': 'Total Number of QSOs',
    'scored_qsos': 'Number of Scored QSOs',
    'uniques': 'Number of Unique QSOs',
    # QSOS BY MODE
    'title_mode': "QSOs by Mode",
    'scored_mode': 'QSO Count for Mode',
    'qsos_by_mode': 'QSOs by Mode',
    # QSOS BY bAND
    'title_band': "QSOs by Band",
    'scored_band': 'QSO Count for Band',
    'qsos_by_band': "QSOs by Band",
    # QSOS BY HOUR
    'title_hour': 'QSOs by Hour',
    'scored_hour': 'QSO Count for hour',
    'qsos_by_hour': 'QSOs by Hour',
    # Counts of QSOS BY DESTINATION
    'title_dest': 'QSO Counts From TX to Destination',
    'with_receiver': 'Total Counted With a Receiver',
    'qsos_with_tx': 'Number With Texas',
    'qsos_with_us': 'Number With US Non Texas',
    'qsos_with_canada': 'Number With Canada',
    'qsos_with_dx': 'Number With Non North America',
    # QSO ERRORS
    'title_qso_issues': 'QSO Issues',
    'duplicate_qsos': 'Numbre of Duplicate QSOs',
    'nils': 'Number of NILs',
    'busteds': 'Number of Busteds',
    'other_invalid_qsos': 'Number Invalidated for Other Reasons',
    'multi_county_exchanges': 'Number of Exchanges With Multiple Counties',
    # Activity
    'title_activity': 'Counts of Some Activities',
    # checks
    'checks_title': 'Sums to Check the Previous Values',
    'uncategorized_logs': 'Number of Uncategorized Logs',
    'invalidated_qsos': 'Number of QSOs Invalidated',
    'with_receiver': 'Number of QSOs With a Receiver',
    'num_states_worked': 'Number of Non-TX States Worked',
    'num_provinces_worked': 'Number of Provinces Worked',
    'num_dx_worked': 'Number of Non North America Worked',
    'num_counties_activated': 'Number of Counties Activated - Non-Mobile',
    'num_counties_activated_mobile': 'Number of Counties Activated - Mobile',
    # lists
    'title_counties': 'Areas Activated and Worked',
    'mobile_activation_counts': 'Number Mobile Activations by County',
    'worked_counties_mobile': 'Number Mobiles Worked By County',
    'counties_activated': 'Counties Activated',
    'counties_worked': 'List Counties Worked by Any Station',
    'states_worked': 'List of Non-TX States Worked',
    'provinces_worked': 'List of Provinces Worked',
    'dx_worked': 'List of Non North America Worked',
        }
RANKINGS = {

    # Texas – Fixed Station
    'TSL': 'Single Operator Mixed Mode (150 watts power limit)',
	'TSH':  'Single Operator Mixed Mode High-Power (>150 watts power)',
	'TML':  'Multi Operators Mixed Mode  (150 watts power limit)',
	'TMH':  'Multi Operators Mixed Mode  High-Power (>150 watts power)',
	'TQS':  'QRP Single Operator Mixed Mode (10 watts or less phone and 5 watts or less',
	'TCSL':  'CW Only Single Operator  (150 watts power limit)',
	'TCSH':  'CW Only Single Operator High-Power (>150 watts power)',
	'TPSL':  'Phone Only Single Operator (150 watts power limit)',
	'TPSH':  'Phone Only Single Operator High-Power (>150 watts power)',
    
    # Texas – Mobile Stations
	'TMS':  'Texas Mobile Single Operator Mixed Mode–may be assisted (no contest power limit)',
	'TMM':  'Texas Mobile Multi Operators (no contest power limit)',
	'TMSC':  'Texas Mobile CW Only Single Operator–may be assisted (no contest power limit)',
	'TMSP':  'Texas Mobile Phone Only Single Operator–may be assisted (no contest power limit)',
    # Note: The spirit of the mobile category is for vehicle-based *or* non-permanent stations who work from multiple counties during the event.',

    # Non-Texas Stations
	'NS':  'Single Operator Mixed Mode (no contest power limits)',
	'NSQ':  'QRP Single Operator (10 watts or less phone and 5 watts or less CW and other modes)',
	'NSC':  'CW Only Single Operator (no contest power limits)',
	'NSP':  'Phone Only Single Operator (no contest power limits)',

    # DX Stations
	'DS':  'DX Single Operator Mixed (no contest power limits)',

    # CheckLog
    'C': 'Check Log Not Including in Rankings'
}

RANK_TABLES = [ 
    ###############
    # SECTION 1 #
    ###############
    [
        {
            'section_title': 'Texas - Fixed Stations',
            'show': [
                ['callsign', 'Call'],
                ['final_score', 'Score'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'No Bonus'],
                ['mtb_mobile_points', 'MTBPts']
            ],
            'discussion': f"This is an area where discussion can be added",
        },
        # the 'show' list, if not empty adds columns after the final score column
        #   shows field name and column header 
        {'title': 'TSL', 'category': 'TX SO LP', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TSH', 'category': 'TX SO HP', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TML', 'category': 'TX MO LP', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMH', 'category': 'TX', 'show':  [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TQS', 'category': 'TX QRP SO', 'show':  [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TCSL', 'category': 'TX CWO SO LP', 'show': [['cw_qsos', 'CWQs']]},
        {'title': 'TCSH', 'category': 'TX CWO SO HP', 'show': [['cw_qsos', 'CWQs']]},
        {'title': 'TPSL', 'category': 'TX PHO SO LP', 'show': [['ph_qsos', 'PHQs']]},
        {'title': 'TPSH', 'category': 'TX PHO SO HP', 'show':  [['ph_qsos', 'PHQs']]}
    ],
    ###############
    # SECTION 2 #
    ###############
    [
        {
            'section_title': 'Texas - Mobile Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['final_score', 'Score'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'No Bonus'],
                ['cab_mobile_points', 'CABPts'],
                ['mtb_mobile_points', 'MTBPts']
            ],
        },
        {'title': 'TMS', 'category': 'TXM SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMM', 'category': 'TXM MO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMSC', 'category': 'TXM SO CWO', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMSP', 'category': 'TXM SO PHO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
    ],
    ###############
    # SECTION   3 #
    ###############
    [
        {
            'section_title': 'Non-Texas Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['final_score', 'Score'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'No Bonus'],
                ['mtb_mobile_points', 'MTBPts']
            ],
        },
        {'title': 'NS', 'category': 'NTX SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'NSQ', 'category': 'NTX SO QRP', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'NSC', 'category': 'NTX SO CWO', 'show':[['cw_qsos', 'CWQs']]},
        {'title': 'NSP', 'category': 'NTX SO PHO', 'show':[['ph_qsos', 'PHQs']]},
    ],

    ###############
    # SECTION   4 #
    ###############
    [
        {
            'section_title': 'DX Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['final_score', 'Score'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'QSO Score'],
                ['mtb_mobile_points', 'MTBPts']
            ],
        },
        {'title': 'DS', 'category': 'DX SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
    ],

    ###############
    # SECTION  5 #
    ###############
    [
        {
            'section_title': 'Check Log',
            'show': [
                ['callsign', 'CallSign'],
                ['final_score', 'Score'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'No Bonus'],
                ['mtb_mobile_points', 'MTBPts']
            ],
        },
        {'title': 'C', 'category': 'CHK', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
    ]
]
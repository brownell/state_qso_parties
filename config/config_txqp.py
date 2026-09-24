"""
Texas QSO Party - Specific Configuration
Application logic and contest rules (NOT secrets/credentials)

This file must be at config_txqp.py for TXQP

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
RANKINGS = {
    # All Operators
    'ALL': 'All Operators',

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
	'DS':  'Single Operator Mixed (no contest power limits)',

    # CheckLog
    'C': 'Check Log Not Including in Rankings'
}

LEADERBOARDS = [ 
    ###############
    # SECTION 1 #
    ###############
    [
        {
            'section_title': 'Texas - Fixed Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'QSO Score'],
                ['mobile_bonus_points', 'QSO Score'],
                ['final_score', 'Score']
            ],
            'discussion': f"This is an area where discussion can be added",
        },
        {'title': 'TSL', 'cat': 'TX SO LP', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TSH', 'cat': 'TX SO HP', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TML', 'cat': 'TX MO LP', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMH', 'cat': 'TX', 'show':  [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TQS', 'cat': 'TX QRP SO', 'show':  [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TCSL', 'cat': 'TX CWO SO LP', 'show': [['cw_qsos', 'CWQs']]},
        {'title': 'TCSH', 'cat': 'TX CWO SO HP', 'show': ['cw_qsos', 'CWQs']},
        {'title': 'TPSL', 'cat': 'TX PHO SO LP', 'show': ['ph_qsos', 'PHQs']},
        {'title': 'TPSH', 'cat': 'TX PHO SO HP', 'show':  ['ph_qsos', 'PHQs']}
    ],
    ###############
    # SECTION 2 #
    ###############
    [
        {
            'section_title': 'Texas - Mobile Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'QSO Score'],
                ['mobile_bonus_points', 'QSO Score'],
                ['final_score', 'Score']
            ],
        },
        {'title': 'TMS', 'cat': 'TXM SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMM', 'cat': 'TXM MO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMSC', 'cat': 'TXM SO CWO', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'TMSP', 'cat': 'TXM SO PHO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
    ],
    ###############
    # SECTION   3 #
    ###############
    [
        {
            'section_title': 'Non-Texas Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'QSO Score'],
                ['mobile_bonus_points', 'QSO Score'],
                ['final_score', 'Score']
            ],
        },
        {'title': 'NS', 'cat': 'NTX SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'NSQ', 'cat': 'NTX SO QRP', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
        {'title': 'NSC', 'cat': 'NTX SO CWO', 'show':[['cw_qsos', 'CWQs']]},
        {'title': 'NSP', 'cat': 'NTX SO PHO', 'show':[['ph_qsos', 'PHQs']]},
    ],

    ###############
    # SECTION   4 #
    ###############
    [
        {
            'section_title': 'DX Stations',
            'show': [
                ['callsign', 'CallSign'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'QSO Score'],
                ['mobile_bonus_points', 'QSO Score'],
                ['final_score', 'Score']
            ],
        },
        {'title': 'DX', 'cat': 'DX SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
    ],

    ###############
    # SECTION  5 #
    ###############
    [
        {
            'section_title': 'Check Log',
            'show': [
                ['callsign', 'CallSign'],
                ['qso_points', 'QSOPts'],
                ['total_multipliers', 'Mults'],
                ['score_wo_bonus', 'QSO Score'],
                ['mobile_bonus_points', 'QSO Score'],
                ['final_score', 'Score']
            ],
        },
        {'title': 'C', 'cat': 'CHK', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
    ]
]
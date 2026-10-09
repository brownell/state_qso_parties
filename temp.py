from pathlib import Path
import sqlite3
from pprint import pprint
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from config.config_txqp import RANKINGS, RANK_TABLES
from config.config import DATABASE_FILE
# def format_result_for_display(result):
#     """
#     Convert the result dictionary to a format suitable for HTML display
#     Handles sets, dicts, and other complex type
#     """
#     display_result = {}
    
#     # Copy simple values
#     simple_fields = [
#         'callsign', 'exchange', 'overlay', 'location_type', 'mode_category',
#         'power_level', 'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
#         'total_multipliers', 'counties_worked_multiplier', 'states_worked_multiplier',
#         'provinces_worked_multiplier', 'dx_worked_multiplier', 'mtb_mobile_points',
#         'worked_n5lcc', 'num_n5lcc_contacts', 'name', 'club', 'claimed_score', 'year'
#     ]
    
#     for field in simple_fields:
#         display_result[field] = result.get(field, 'N/A')
    
#     # Convert sets to sorted lists
#     display_result['counties_worked'] = format_set_as_list(result.get('counties_worked', set()))
#     display_result['states_worked'] = format_set_as_list(result.get('states_worked', set()))
#     display_result['provinces_worked'] = format_set_as_list(result.get('provinces_worked', set()))
#     display_result['dx_worked'] = format_set_as_list(result.get('dx_worked', set()))
#     display_result['counties_activated'] = format_set_as_list(result.get('counties_activated', set()))
#     display_result['bands_worked'] = format_set_as_list(result.get('bands_worked', set()))
    
#     # Format QSOs by band
#     qsos_by_band = result.get('qsos_by_band', {})
#     display_result['qsos_by_band'] = [
#         {'band': band, 'count': count}
#         for band, count in sorted(qsos_by_band.items(), key=lambda x: x[0])
#     ]
    
#     # Format QSOs by mode
#     qsos_by_mode = result.get('qsos_by_mode', {})
#     display_result['qsos_by_mode'] = [
#         {'mode': mode, 'count': count}
#         for mode, count in qsos_by_mode.items()
#     ]
    

#     # Format QSOs by hour
#     try:
#         temp = result.get('qsos_by_hour', {})
#         display_result['qsos_by_hour'] = {}
#         for key in temp:
#             display_result['qsos_by_hour'][key] =  temp[key]
#     except Exception as e:
#         print(f"Error formatting qsos_by_hour for display: {e}")
#         display_result['qsos_by_hour'] = []
    
#     ## errors and warnings
#     display_result['errors'] = result['errors']
#     display_result['warnings'] = result['warnings']

#     return display_result
import json
SCRIPT_DIR = Path(__file__).resolve().parent
seq_cab_attributes = [
            'club', 'name', 'location', 'name', 'category_band', 'email',
            'category_mode', 'category_power', 'category_station', 
            'cat', 'claimed_score'
    ]
    # dict fields require different aproach from above fields
seq_dict_fields = [
            'qsos_by_band', 'qsos_by_mode','mobile_activation_counts'
        ]
        
seq_types_of_fields = {'integer': 0, 'string': '','set': set(), 'list': []}
seq_fields = {'integer': [
        'dxcc_code',
        'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
        'total_multipliers', 'cab_mobile_points', 
        'mtb_mobile_points', 'cw_qsos',
        'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
        'special_station_contacts', 'claimed_score', 'uniques', 'nils',
        'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
        'other_bad_qsos'
    ],
    'string': [  # from the result object
        'year', 'callsign',  'dxcc_entity'
    ],
    'set': [
        'counties_worked', 'states_worked', 'provinces_worked',
        'dx_worked', 'counties_activated', 'bands_worked',
        'de_exch_rcvd', 'dx_exch_sent', 'mobile_counties_worked',
        'mobile_activation_counts'
    ],
    'list': ['errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls']
    }

types_of_fields = {'integer': 0, 'string': '', 'set': set(), 'list': []}
fields = {'integer': [
    'dxcc_code',
    'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
    'total_multipliers', 'cab_mobile_points', 
    'mtb_mobile_points', 'cw_qsos',
    'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
    'special_station_contacts', 'claimed_score', 'uniques', 'nils',
    'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
    'other_bad_qsos'
],
'string': [  # from the result object
    'year', 'callsign',  'dxcc_entity', 'club', 'name', 'location', 'name', 'category_band', 'email',
                'category_mode', 'category_power', 'category_station', 
                'cat', 'claimed_score'
],
'list': [ 'mobile_counties_worked', 'counties_worked', 'states_worked', 'provinces_worked',
        'dx_worked', 'counties_activated', 'bands_worked',
        'de_exch_rcvd', 'dx_exch_sent', 'errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls']
}
# dict fields require different aproach from above fields
dict_fields = [
    'qsos_by_band', 'qsos_by_mode','mobile_activation_counts'
    ]

cab_attributes = [
    'club', 'name', 'location', 'name', 'category_band', 'email',
    'category_mode', 'category_power', 'category_station', 
    'cat', 'claimed_score'
    ]

def deserialize_result(result):
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
            # INTEGERS AND sTRINGHS
            for typ in list(['integer', 'string', 'list']):
                for fld in fields[typ]:
                    display_result[fld] = result.get(fld, types_of_fields[typ])

            # SETS
            # for fld in fields['set']:
            #     display_result[fld] = list(set(json.loads(result.get(fld, []))))

            # DICTS
            for field in dict_fields:
                if field in result and result[field]:
                    display_result[field] = result[field]

        except Exception as e:
            print(f"could not deserialize {result}")
    
    return result

def serialize_result(result):
    """
    Adds simple fields from the "result" object
    Adds attributes of the "CAB" objext
    Convert result dict to database-storable format.
    Convert lists to JSONF
    Converts sets to JSON lists, handles complex types.
    """
    db_result = {}
    try:
        # put values from the above listed fields into db_result
        for typ in list(seq_types_of_fields.keys()):   
            if typ == 'set':
                for fld in seq_fields[typ]:
                    value = result.get(fld, seq_types_of_fields[typ])
                    db_result[fld] = json.dumps(sorted(list(value)))
            elif typ == 'list':
                for fld in seq_fields[typ]:
                    value = result.get(fld, seq_types_of_fields[typ])
                    db_result[fld] = json.dumps(list(value))

            else:
                for fld in seq_fields[typ]:
                    db_result[fld] = result.get(fld, seq_types_of_fields[typ])
        
        for field in seq_dict_fields:
            value = result.get(field, {})
            # Convert sets in dict values to lists
            db_result[field] = json.dumps(value)
            # print(f"field: {field} value: {value}")
        
        # Timestamps
        now = datetime.utcnow().isoformat()
        db_result['created_at'] = now
        db_result['updated_at'] = now
    except Exception as e:
        print(f"exception in creating db_result")
        # print('BREAK')
    
    return db_result


result = {
    "bands_worked": [],
    "busted_calls": [["AA5KC", "N5DN"]],
    "busteds": 1,
    "cab_mobile_points": 0,
    "callsign": "AA5KC",
    "cat": "TSL",
    "category_band": "ALL",
    "category_mode": "MIX",
    "category_power": "LP",
    "category_rank": 12,
    "category_station": "FIX",
    "claimed_score": 9204,
    "club": "None",
    "counties_activated": {"KINN"},
    "counties_worked": {"AUST", "BAIL", "BAST", "BURL", "COML", "DALS", "DENT", "FBEN", "GILL", "GRIM", "HARR", "HAYS", "HRSN", "JACK", "JDAV", "KAUF", "KINN", "MEDI", "MILL", "MLEN", "NUEC", "PARK", "SMIT", "SOME", "TARR", "WALK", "WASH", "WHAR", "WLSN"},
    "created_at": "2026-10-08T18:54:53.653180",
    "cw_qsos": 36,
    "de_exch_rcvd": {},
    "dg_qsos": 0,
    "dup_qsos": 1,
    "dx_exch_sent": {},
    "dx_worked": {},
    "dxcc_code": 0,
    "dxcc_entity": "AA5KC",
    "email": "KJ5BYZ@gmail.com",
    "errors": ["BUSTED QSO to N5DN exchs:KINN-SOME mode:PH band:40 Sept 19th 1548Z\\n", "NIL QSO from-to AA5KC-KF5VDX exchs:KINN-NUEC mode:PH band:40 Sept 19th 1648Z\\n", "Duplicate QSO from-to: AA5KC-K5LSU exchs:KINN-LA mode:CW band:20 Sept 19th 1846Z\\n", "NIL QSO from-to AA5KC-W5RAW exchs:KINN-MLEN mode:PH band:20 Sept 19th 1852Z\\n", "NIL QSO from-to AA5KC-N7EPD exchs:KINN-WA mode:PH band:20 Sept 19th 1856Z\\n"],
    "exchange": '',
    "final_score": 8466,
    "grid_square": '',
    "invalid_exchange_qsos": 0,
    "is_valid": '',
    "location": "TX",
    "mobile_activation_counts": {},
    "mobile_counties_worked": {},
    "mtb_mobile_points": 0,
    "name": "David Loftus",
    "nil_calls": [],
    "nils": 3,
    "other_bad_qsos": 0,
    "overlay": '',
    "ph_qsos": 29,
    "provinces_worked": [],
    "qso_points": 166,
    "qsos_by_band": {"160": 0, "80": 0, "40": 30, "20": 33, "15": 1, "10": 1, "6": 0, "2": 0},
    "qsos_by_hour": [9, 25, 7, 19, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "qsos_by_mode": {"PH": 29, "CW": 36, "RY": 0, "DG": 0},
    "ry_qsos": 0,
    "score_wo_bonus": 8466,
    "special_station_contacts": 0,
    "states_worked": {"AZ", "CA", "FL", "IA", "ID", "IL", "KS", "LA", "MO", "MS", "NC", "NH", "NJ", "NM", "NY", "OH", "OK", "OR", "SC", "TN", "UT", "WI"},
    "total_multipliers": 51,
    "total_qsos": 70,
    "uniques": 0,
    "updated_at": "2026-10-08T18:54:53.653180",
    "valid_qsos": 69,
    "warnings": [],
    "worked_special_station": '',
    "year": "2026"
}
xyzzy = 
foo = serialize_result(result)
pprint(foo)
bar = deserialize_result(foo)
pprint(bar)

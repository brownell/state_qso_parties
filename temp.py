
from pprint import pprint
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest import result
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from utilities import generate_index_key, get_dxcc, writefile
from share import SHARED

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    CONTEST_YEAR, BATCH_INPUT_DIR, HQ_FIELDS
)
SCRIPT_DIR = Path(__file__).resolve().parent

dir_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR).resolve()

def is_fuzzy_match(x: str, y: str, max_missing: int = 2) -> bool:
    """
    Determines if callsign `y` could be a mistyping of callsign `x`.
    The rule: `y` must contain all but `max_missing` characters/numbers 
    from `x`, and they must appear in the same relative order.
    Args:
        x: The original callsign.
        y: The potentially mistyped callsign.
        max_missing: The maximum number of characters from `x` that can 
                     be missing in `y`. (Defaults to 2 based on the rule).
    Returns:
        True if it's a match, False otherwise.
    """
    x = x.upper()
    y = y.upper()
    
    m, n = len(x), len(y)
    
    # Compute the Longest Common Subsequence (LCS)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    lcs_length = dp[m][n]
    if lcs_length == 1 and len(x) == 2:
        return True
    return lcs_length >= len(x) - max_missing

is_fuzzy_match('AI6G', 'AI6O')

# filenames = [p.name for p in dir_path.iterdir() if p.is_file()]
# result_index = 0
# hq_clubs = set()
# added_clubs = set()
# cab_clubs = set()
# s = SHARED()
# for file in filenames:
#     try:
#         file_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR / file).resolve()
#         cab = parse_log_file(file_path, ignore_unknown_key=True, check_categories=False, ignore_order=True, check_mode=False)
#         cab.callsign = cab.callsign.split('/')[0]
#         try:
#             if 'hq_anything' in list(cab.__dict__.keys()):
#                 if "HQ-CLUB" in list(cab.hq_anything.keys()):
#                     hq_club = cab.hq_anything['HQ-CLUB']
#                     if hq_club not in ['None', None]:
#                         hq_clubs.add(hq_club)
#                         if hq_club not in s.contest_clubs_original:
#                             added_clubs.add(hq_club)
#                     else:
#                         club = cab.club
#                         if (cab.club not in ['None', None, 'NONE']) and (cab.club not in list(hq_clubs) and cab.club not in (added_clubs)):
#                             print(f"{cab.club}")
#                             cab_clubs.add(cab.club)
#         except Exception as e:
#             print(f"error getting HQ-CLUB {cab.callsign}  {e}")
#             continue
#     except Exception as e:
#         if file:
#             s.stats["rejected_logs"] += 1
#             s.stats["rejected_logs_filenames"].append(file)
#             print(f"ERROR - REJECTED: log file {file} was rejected by the parser")
#             s.out_files['errors'].write(f"REJECTED log file {file} was rejected by the parser\n")
#             continue
# print(f"# of clubs in HQ-CLUB: that were Bruce's dropdown: {len(hq_clubs)}\n dropdown clubs:\n\n {hq_clubs}\n\n# in HQ-CLUB: that were NOT in Bruce's dropdown: {len(added_clubs)}\nclubs added: {added_clubs} {cab_clubs}\n\n# in Cabrillo CLUB: when HQ-CLUB was NULL\nThese are not in the other two lists: {len(cab_clubs)}\nclubs added: {cab_clubs}")



# [
#     {
#         "club": null
#     },
#     {
#         "club": "Alabama Contest Group"
#     },
#     {
#         "club": "Alabama contest group"
#     },
#     {
#         "club": "Alexandria Radio Club"
#     },
#     {
#         "club": "Amateur Radio Club of Parker County"
#     },
#     {
#         "club": "Arizona Outlaws Contest Club"
#     },
#     {
#         "club": "Arkansas DX Assn"
#     },
#     {
#         "club": "Atlantic Coast DX & Contest Group"
#     },
#     {
#         "club": "Austin Amateur Radio Club"
#     },
#     {
#         "club": "Austin QRP Club"
#     },
#     {
#         "club": "BAY AREA DXERS"
#     },
#     {
#         "club": "Bavarian Contest Club"
#     },
#     {
#         "club": "Bay Area DXers"
#     },
#     {
#         "club": "Big Sky Contesters"
#     },
#     {
#         "club": "Bloomington Amature Radio Club --- K9DIY"
#     },
#     {
#         "club": "Bristol (TN) ARC"
#     },
#     {
#         "club": "Bristol (TN/VA) ARC"
#     },
#     {
#         "club": "CARESS - Coquitlam Amateur Radio Club"
#     },
#     {
#         "club": "CCO"
#     },
#     {
#         "club": "CONTEST CLUB ONTARIO"
#     },
#     {
#         "club": "CW Contest Club"
#     },
#     {
#         "club": "Candlewood ARA"
#     },
#     {
#         "club": "Central Texas DX and Contest Club"
#     },
#     {
#         "club": "Central Virginia Contest Club"
#     },
#     {
#         "club": "Contest Club Ontario"
#     },
#     {
#         "club": "Contest Group du Quebec"
#     },
#     {
#         "club": "Cuyahoga ARS"
#     },
#     {
#         "club": "DCT ARC"
#     },
#     {
#         "club": "DEEP DIXIE CONTEST CLUB"
#     },
#     {
#         "club": "DFW Contest Group"
#     },
#     {
#         "club": "DICKSON COUNTY ARC"
#     },
#     {
#         "club": "DX"
#     },
#     {
#         "club": "Dawn Patrol Surf Club"
#     },
#     {
#         "club": "Dupage ARC"
#     },
#     {
#         "club": "East Lansing DX Club"
#     },
#     {
#         "club": "Ellis County ARC"
#     },
#     {
#         "club": "FCG"
#     },
#     {
#         "club": "FLORIDA CONTEST GROUP"
#     },
#     {
#         "club": "FRANKFORD RADIO CLUB"
#     },
#     {
#         "club": "Fayette County DX Club"
#     },
#     {
#         "club": "Florida Contest Group"
#     },
#     {
#         "club": "Frankford Radio Club"
#     },
#     {
#         "club": "Ft. Smith ARC"
#     },
#     {
#         "club": "Garland Amateur Radio Club"
#     },
#     {
#         "club": "Grayson County ARC"
#     },
#     {
#         "club": "Great Places Contest Club"
#     },
#     {
#         "club": "Houston ECHO Society"
#     },
#     {
#         "club": "Hudson Valley Contesters and DXers"
#     },
#     {
#         "club": "Irving ARC"
#     },
#     {
#         "club": "Jefferson ARC"
#     },
#     {
#         "club": "KANSAS CITY CONTEST CLUB"
#     },
#     {
#         "club": "KARO ECHO"
#     },
#     {
#         "club": "KCCC"
#     },
#     {
#         "club": "Kansas City Contest Cliub"
#     },
#     {
#         "club": "Kansas City Contest Club"
#     },
#     {
#         "club": "Kansas city contest club"
#     },
#     {
#         "club": "Kentucky Contest Group"
#     },
#     {
#         "club": "Lake Area Amateur Radio Club"
#     },
#     {
#         "club": "Lake Area Amateur Radio Klub"
#     },
#     {
#         "club": "MINNESOTA  WIRELESS  ASSN"
#     },
#     {
#         "club": "MINNESOTA WIRELESS ASSN"
#     },
#     {
#         "club": "Mad River Radio Club"
#     },
#     {
#         "club": "Maritime Contest Club"
#     },
#     {
#         "club": "Medina County ARC"
#     },
#     {
#         "club": "Metrocrest Amateur Radio Society"
#     },
#     {
#         "club": "Metrocrest Amateur Radio Society KB5A"
#     },
#     {
#         "club": "Midland ARC"
#     },
#     {
#         "club": "Minnesota Wireless Assn"
#     },
#     {
#         "club": "NAQCC"
#     },
#     {
#         "club": "NASA JSC W5RRR Amateur Radio Club"
#     },
#     {
#         "club": "NCARC"
#     },
#     {
#         "club": "NIAGARA FRONTIER RADIOSPORT"
#     },
#     {
#         "club": "NONE"
#     },
#     {
#         "club": "New Providence ARC"
#     },
#     {
#         "club": "Niagara Frontier Radiosport"
#     },
#     {
#         "club": "None"
#     },
#     {
#         "club": "North Coast Contesters"
#     },
#     {
#         "club": "North Texas ARS"
#     },
#     {
#         "club": "Northwest Amateur Radio Society"
#     },
#     {
#         "club": "ORANGE COUNTY AMATEUR RADIO CLUB"
#     },
#     {
#         "club": "Orca DX and Contest"
#     },
#     {
#         "club": "PART of Westford"
#     },
#     {
#         "club": "POTOMAC VALLEY RADIO CLUB"
#     },
#     {
#         "club": "PVRC"
#     },
#     {
#         "club": "Potomac Valley Radio CLub"
#     },
#     {
#         "club": "Potomac Valley Radio Club"
#     },
#     {
#         "club": "RIOARC"
#     },
#     {
#         "club": "Radio Amateurs of Northern Vermont"
#     },
#     {
#         "club": "Randolph County"
#     },
#     {
#         "club": "Red River Valley ARC"
#     },
#     {
#         "club": "Redwood Empire DX Assn"
#     },
#     {
#         "club": "River Bend Wireless Operators Club"
#     },
#     {
#         "club": "Rushmore Radio Amateurs"
#     },
#     {
#         "club": "SCCC"
#     },
#     {
#         "club": "SOCIETY OF MID-WEST CONTESTERS"
#     },
#     {
#         "club": "SOCIETY OF MIDWEST CONTESTERS"
#     },
#     {
#         "club": "SP DX CLUB"
#     },
#     {
#         "club": "SWAMP FOX CONTEST GROUP"
#     },
#     {
#         "club": "Shenandoah Valley Amateur Radio Cllub"
#     },
#     {
#         "club": "Slovak Contest Group"
#     },
#     {
#         "club": "Snohomish County Hams Club"
#     },
#     {
#         "club": "Society of Midwest Contesters"
#     },
#     {
#         "club": "Soth East Contest Club"
#     },
#     {
#         "club": "South East Contest Club"
#     },
#     {
#         "club": "South Texas Amatuer Radio Club"
#     },
#     {
#         "club": "South Texas DX and Contest Club"
#     },
#     {
#         "club": "Southern California Contest Club"
#     },
#     {
#         "club": "Sterling Park ARC"
#     },
#     {
#         "club": "Sterling Park Amateur Radio Club"
#     },
#     {
#         "club": "Swamp Fox Contest Group"
#     },
#     {
#         "club": "TCG"
#     },
#     {
#         "club": "TDXS"
#     },
#     {
#         "club": "TENNESSEE CONTEST GROUP"
#     },
#     {
#         "club": "Tennesse Contest Club"
#     },
#     {
#         "club": "Tennessee Contest Group"
#     },
#     {
#         "club": "Texas DX Society"
#     },
#     {
#         "club": "The 67 Ham Radio Group"
#     },
#     {
#         "club": "The American Legion Post 42 ARC"
#     },
#     {
#         "club": "The Houston ECHO Society, W5ECO"
#     },
#     {
#         "club": "Tri-County Amateur Radio Club"
#     },
#     {
#         "club": "WVDXC"
#     },
#     {
#         "club": "West Allis RAC"
#     },
#     {
#         "club": "West Allis Radio Amateur Club"
#     },
#     {
#         "club": "Western Washington DX Club"
#     },
#     {
#         "club": "Willamette Valley DX Club"
#     },
#     {
#         "club": "YANKEE CLIPPER CONTEST CLUB"
#     },
#     {
#         "club": "YCCC"
#     },
#     {
#         "club": "Yankee Clipper Contest Club"
#     },
#     {
#         "club": "dfw cONTEST GROUP"
#     },
#     {
#         "club": "n/a"
#     },
#     {
#         "club": "none"
#     },
#     {
#         "club": "saint paul radio club"
#     },
#     {
#         "club": "yankee clipper contest club"
#     }
# ]

# # import trace
# # trace

# # foo = {'title': 'Single Operator Mixed Mode High-Power (>150 watts power)', 'category': 'TSH', 'headers': ['Rank', 'Call', 'Score', 'CWQs', 'PHQs', 'QSOPts', 'Mults', 'No Bonus', 'MTBPts', 'Claimed'], 'rows': [[...], [...], [...], [...], [...], [...]]}


# # foo = [
# #         {
# #             'section_title': 'Texas - Mobile Stations',
# #             'show': [
# #                 ['callsign', 'CallSign'],
# #                 ['final_score', 'Score'],
# #                 ['qso_points', 'QSOPts'],
# #                 ['total_multipliers', 'Mults'],
# #                 ['score_wo_bonus', 'No Bonus'],
# #                 ['cab_mobile_points', 'CABPts'],
# #                 ['mtb_mobile_points', 'MTBPts'],
# #                 ['claimed_score', 'Claimed']
# #             ],
# #         },
# #         {'title': 'TMS', 'category': 'TXM SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
# #         {'title': 'TMM', 'category': 'TXM MO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
# #         {'title': 'TMSC', 'category': 'TXM SO CWO', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
# #         {'title': 'TMSP', 'category': 'TXM SO PHO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
# #     ]

# # {'title': 'Single Operator Mixed Mode (150 watts power limit)', 'category': 'TSL', 'headers': ['Rank', 'Call', 'Score', 'CWQs', 'PHQs', 'QSOPts', 'Mults', 'No Bonus', 'MTBPts', 'Claimed'], 'rows': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...]]}



# # from pathlib import Path
# # import sqlite3
# # from pprint import pprint
# # from pathlib import Path
# # from typing import Dict, List, Optional
# # from datetime import datetime
# # from config.config_txqp import RANKINGS, RANK_TABLES
# # from config.config import DATABASE_FILE
# # # def format_result_for_display(result):
# # #     """
# # #     Convert the result dictionary to a format suitable for HTML display
# # #     Handles sets, dicts, and other complex type
# # #     """
# # #     display_result = {}
    
# # #     # Copy simple values
# # #     simple_fields = [
# # #         'callsign', 'exchange', 'overlay', 'location_type', 'mode_category',
# # #         'power_level', 'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
# # #         'total_multipliers', 'counties_worked_multiplier', 'states_worked_multiplier',
# # #         'provinces_worked_multiplier', 'dx_worked_multiplier', 'mtb_mobile_points',
# # #         'worked_n5lcc', 'num_n5lcc_contacts', 'name', 'club', 'claimed_score', 'year'
# # #     ]
    
# # #     for field in simple_fields:
# # #         display_result[field] = result.get(field, 'N/A')
    
# # #     # Convert sets to sorted lists
# # #     display_result['counties_worked'] = format_set_as_list(result.get('counties_worked', set()))
# # #     display_result['states_worked'] = format_set_as_list(result.get('states_worked', set()))
# # #     display_result['provinces_worked'] = format_set_as_list(result.get('provinces_worked', set()))
# # #     display_result['dx_worked'] = format_set_as_list(result.get('dx_worked', set()))
# # #     display_result['counties_activated'] = format_set_as_list(result.get('counties_activated', set()))
# # #     display_result['bands_worked'] = format_set_as_list(result.get('bands_worked', set()))
    
# # #     # Format QSOs by band
# # #     qsos_by_band = result.get('qsos_by_band', {})
# # #     display_result['qsos_by_band'] = [
# # #         {'band': band, 'count': count}
# # #         for band, count in sorted(qsos_by_band.items(), key=lambda x: x[0])
# # #     ]
    
# # #     # Format QSOs by mode
# # #     qsos_by_mode = result.get('qsos_by_mode', {})
# # #     display_result['qsos_by_mode'] = [
# # #         {'mode': mode, 'count': count}
# # #         for mode, count in qsos_by_mode.items()
# # #     ]
    

# # #     # Format QSOs by hour
# # #     try:
# # #         temp = result.get('qsos_by_hour', {})
# # #         display_result['qsos_by_hour'] = {}
# # #         for key in temp:
# # #             display_result['qsos_by_hour'][key] =  temp[key]
# # #     except Exception as e:
# # #         print(f"Error formatting qsos_by_hour for display: {e}")
# # #         display_result['qsos_by_hour'] = []
    
# # #     ## errors and warnings
# # #     display_result['errors'] = result['errors']
# # #     display_result['warnings'] = result['warnings']

# # #     return display_result
# # import json
# # SCRIPT_DIR = Path(__file__).resolve().parent
# # seq_cab_attributes = [
# #             'club', 'name', 'location', 'name', 'category_band', 'email',
# #             'category_mode', 'category_power', 'category_station', 
# #             'cat', 'claimed_score'
# #     ]
# #     # dict fields require different aproach from above fields
# # seq_dict_fields = [
# #             'qsos_by_band', 'qsos_by_mode','mobile_activation_counts'
# #         ]
        
# # seq_types_of_fields = {'integer': 0, 'string': '','set': set(), 'list': []}
# # seq_fields = {'integer': [
# #         'dxcc_code',
# #         'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
# #         'total_multipliers', 'cab_mobile_points', 
# #         'mtb_mobile_points', 'cw_qsos',
# #         'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
# #         'special_station_contacts', 'claimed_score', 'uniques', 'nils',
# #         'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
# #         'other_bad_qsos'
# #     ],
# #     'string': [  # from the result object
# #         'year', 'callsign',  'dxcc_entity'
# #     ],
# #     'set': [
# #         'counties_worked', 'states_worked', 'provinces_worked',
# #         'dx_worked', 'counties_activated', 'bands_worked',
# #         'de_exch_rcvd', 'dx_exch_sent', 'mobile_counties_worked',
# #         'mobile_activation_counts'
# #     ],
# #     'list': ['errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls']
# #     }

# # types_of_fields = {'integer': 0, 'string': '', 'set': set(), 'list': []}
# # fields = {'integer': [
# #     'dxcc_code',
# #     'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
# #     'total_multipliers', 'cab_mobile_points', 
# #     'mtb_mobile_points', 'cw_qsos',
# #     'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
# #     'special_station_contacts', 'claimed_score', 'uniques', 'nils',
# #     'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
# #     'other_bad_qsos'
# # ],
# # 'string': [  # from the result object
# #     'year', 'callsign',  'dxcc_entity', 'club', 'name', 'location', 'name', 'category_band', 'email',
# #                 'category_mode', 'category_power', 'category_station', 
# #                 'cat', 'claimed_score'
# # ],
# # 'list': [ 'mobile_counties_worked', 'counties_worked', 'states_worked', 'provinces_worked',
# #         'dx_worked', 'counties_activated', 'bands_worked',
# #         'de_exch_rcvd', 'dx_exch_sent', 'errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls']
# # }
# # # dict fields require different aproach from above fields
# # dict_fields = [
# #     'qsos_by_band', 'qsos_by_mode','mobile_activation_counts'
# #     ]

# # cab_attributes = [
# #     'club', 'name', 'location', 'name', 'category_band', 'email',
# #     'category_mode', 'category_power', 'category_station', 
# #     'cat', 'claimed_score'
# #     ]

# # def deserialize_result(result):
# #     """ The opposite of serialize_result
# #         Reads data from the databaser one operator record
# #         Adds simple fields from the "result" object
# #         Adds attributes of the "CAB" objext
# #         Convert result dict to JSON-usable format.
# #         Convert lists to JSON
# #         Converts sets to JSON lists, handles complex types.
# #         """

# #     if result:
# #         display_result = {}
# #         try:
# #             # INTEGERS AND sTRINGHS
# #             for typ in list(['integer', 'string', 'list']):
# #                 for fld in fields[typ]:
# #                     display_result[fld] = result.get(fld, types_of_fields[typ])

# #             # SETS
# #             # for fld in fields['set']:
# #             #     display_result[fld] = list(set(json.loads(result.get(fld, []))))

# #             # DICTS
# #             for field in dict_fields:
# #                 if field in result and result[field]:
# #                     display_result[field] = result[field]

# #         except Exception as e:
# #             print(f"could not deserialize {result}")
    
# #     return result

# # def serialize_result(result):
# #     """
# #     Adds simple fields from the "result" object
# #     Adds attributes of the "CAB" objext
# #     Convert result dict to database-storable format.
# #     Convert lists to JSONF
# #     Converts sets to JSON lists, handles complex types.
# #     """
# #     db_result = {}
# #     try:
# #         # put values from the above listed fields into db_result
# #         for typ in list(seq_types_of_fields.keys()):   
# #             if typ == 'set':
# #                 for fld in seq_fields[typ]:
# #                     value = result.get(fld, seq_types_of_fields[typ])
# #                     db_result[fld] = json.dumps(sorted(list(value)))
# #             elif typ == 'list':
# #                 for fld in seq_fields[typ]:
# #                     value = result.get(fld, seq_types_of_fields[typ])
# #                     db_result[fld] = json.dumps(list(value))

# #             else:
# #                 for fld in seq_fields[typ]:
# #                     db_result[fld] = result.get(fld, seq_types_of_fields[typ])
        
# #         for field in seq_dict_fields:
# #             value = result.get(field, {})
# #             # Convert sets in dict values to lists
# #             db_result[field] = json.dumps(value)
# #             # print(f"field: {field} value: {value}")
        
# #         # Timestamps
# #         now = datetime.utcnow().isoformat()
# #         db_result['created_at'] = now
# #         db_result['updated_at'] = now
# #     except Exception as e:
# #         print(f"exception in creating db_result")
# #         # print('BREAK')
    
# #     return db_result


# # result = {
# #     "bands_worked": [],
# #     "busted_calls": [["AA5KC", "N5DN"]],
# #     "busteds": 1,
# #     "cab_mobile_points": 0,
# #     "callsign": "AA5KC",
# #     "cat": "TSL",
# #     "category_band": "ALL",
# #     "category_mode": "MIX",
# #     "category_power": "LP",
# #     "category_rank": 12,
# #     "category_station": "FIX",
# #     "claimed_score": 9204,
# #     "club": "None",
# #     "counties_activated": {"KINN"},
# #     "counties_worked": {"AUST", "BAIL", "BAST", "BURL", "COML", "DALS", "DENT", "FBEN", "GILL", "GRIM", "HARR", "HAYS", "HRSN", "JACK", "JDAV", "KAUF", "KINN", "MEDI", "MILL", "MLEN", "NUEC", "PARK", "SMIT", "SOME", "TARR", "WALK", "WASH", "WHAR", "WLSN"},
# #     "created_at": "2026-10-08T18:54:53.653180",
# #     "cw_qsos": 36,
# #     "de_exch_rcvd": {},
# #     "dg_qsos": 0,
# #     "dup_qsos": 1,
# #     "dx_exch_sent": {},
# #     "dx_worked": {},
# #     "dxcc_code": 0,
# #     "dxcc_entity": "AA5KC",
# #     "email": "KJ5BYZ@gmail.com",
# #     "errors": ["BUSTED QSO to N5DN exchs:KINN-SOME mode:PH band:40 Sept 19th 1548Z\\n", "NIL QSO from-to AA5KC-KF5VDX exchs:KINN-NUEC mode:PH band:40 Sept 19th 1648Z\\n", "Duplicate QSO from-to: AA5KC-K5LSU exchs:KINN-LA mode:CW band:20 Sept 19th 1846Z\\n", "NIL QSO from-to AA5KC-W5RAW exchs:KINN-MLEN mode:PH band:20 Sept 19th 1852Z\\n", "NIL QSO from-to AA5KC-N7EPD exchs:KINN-WA mode:PH band:20 Sept 19th 1856Z\\n"],
# #     "exchange": '',
# #     "final_score": 8466,
# #     "grid_square": '',
# #     "invalid_exchange_qsos": 0,
# #     "is_valid": '',
# #     "location": "TX",
# #     "mobile_activation_counts": {},
# #     "mobile_counties_worked": {},
# #     "mtb_mobile_points": 0,
# #     "name": "David Loftus",
# #     "nil_calls": [],
# #     "nils": 3,
# #     "other_bad_qsos": 0,
# #     "overlay": '',
# #     "ph_qsos": 29,
# #     "provinces_worked": [],
# #     "qso_points": 166,
# #     "qsos_by_band": {"160": 0, "80": 0, "40": 30, "20": 33, "15": 1, "10": 1, "6": 0, "2": 0},
# #     "qsos_by_hour": [9, 25, 7, 19, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     "qsos_by_mode": {"PH": 29, "CW": 36, "RY": 0, "DG": 0},
# #     "ry_qsos": 0,
# #     "score_wo_bonus": 8466,
# #     "special_station_contacts": 0,
# #     "states_worked": {"AZ", "CA", "FL", "IA", "ID", "IL", "KS", "LA", "MO", "MS", "NC", "NH", "NJ", "NM", "NY", "OH", "OK", "OR", "SC", "TN", "UT", "WI"},
# #     "total_multipliers": 51,
# #     "total_qsos": 70,
# #     "uniques": 0,
# #     "updated_at": "2026-10-08T18:54:53.653180",
# #     "valid_qsos": 69,
# #     "warnings": [],
# #     "worked_special_station": '',
# #     "year": "2026"
# # }
# # xyzzy = 
# # foo = serialize_result(result)
# # pprint(foo)
# # bar = deserialize_result(foo)
# # pprint(bar)

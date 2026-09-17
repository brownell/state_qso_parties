'''
Scores just a single QSO and passes the score back to the caller
This file will almost certainly be QSO-party-dependent.
'''

"""
    ALL of these values in the "r" object get updated in this method
    * 'cw_qsos': 0,
    * 'ph_qsos': 0,
    * 'dg_qsos': 0,
    * 'ry_qsos': 0,
    * 'total_qsos': 0, # total number validated, whether dups or not
    * 'valid_qsos': 0, #number of qsos that are not dups and contribute to the score
    * 'counties_worked': set(),
    * 'states_worked': set(),
    * 'provinces_worked': set(),
    * 'dx_worked': set(),
    * 'counties_activated': set(),
    'de_exch_rcvd': set(),
    'dx_exch_sent': set(),
    'score_w-o_bonus': 0,
    'rover_bonus_points': 0,
    'county_bonus_points': 0,
    'worked_special_station': False,
    'num_special_station_contacts': 0,
    * 'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 0, '15': 0, '10': 0, '6': 0, '2': 0},
    * 'qsos_by_mode': {'PH': 0, 'CW': 0, 'DG': 0, 'RY': 0},
    * 'qsos_by_hour': {i: 0 for i in range(1400,2600, 100)},  # Hour of day (1400 - 2500)
    'errors': [],
    'warnings': [],
    * 'is_valid': True
"""
from datetime import datetime
from cabrillo.qso import frequency_to_band_m
from read_prepare import get_dxcc

qso_modes = ['CW', 'PH', 'DG', 'RY']
qso_mode_names = ['cw_qsos', 'ph_qsos', 'dg_qsos', 'dg_qsos']

def score_a_qso(s, r, q, dup):
    if not q.valid:
        return 0
    
    qso_dup = make_dup(s, r, q)
    
    if qso_dup in dup['qsos']:
        q.valid = False
        return 0
    dup['qsos'].append(qso_dup)

    gets_mult = False
    if q.dx_exch not in dup['mults']:
        dup['mults'].append(q.dx_exch[1])
        r['total_multipliers'] += 1

    # increment qsos count for each mode
    r[f"{q.mo.lower()}_qsos"] += 1
    # increment qsos count for dx_exch
    # increment qsos SET for areas activated and worked
    if q.de_exch[1] in s.counties:
        r['counties_activated'].add(q.de_exch[1])
    elif q.dx_exch[1] in s.counties:
        r['counties_worked'].add(q.dx_exch[1])
    elif q.dx_exch[1] in s.states:
        r['states_worked'].add(q.dx_exch[1])
    elif q.dx_exch[1] in s.provinces:
        r['provinces_worked'].add(q.dx_exch[1])
    elif r['cab'].location == "DX":
        r['dx_worked'].add(get_dxcc(s, q.dx_exch[1], q.dx_call)[1])
    else:
        q.valid = False
        r.valid_qsos -= 1

    r['qsos_by_band'][frequency_to_band_m(q.freq)] += 1
    r['qsos_by_mode'][q.mo] += 1

    # qsos by hour
    hour = int(q.date.strftime("%H"))
    if hour > 1:
        hour -= 14
    else:
        hour -= 2
    r["qsos_by_hour"][hour + ((int(q.date.strftime("%d")) - 19) * 12)] += 1
    print('BREAK')

def make_dup(s, r, qso):
    de = get_dxcc(s, r['cab'].location, r['callsign'])[1]
    dx = get_dxcc(s, qso.dx_exch[1].upper(), qso.dx_call.upper())[1]
    return "_".join([de, dx, qso.de_exch[1].upper(), qso.dx_exch[1].upper(), frequency_to_band_m(qso.freq), qso.mo.upper()])
        




'''
Scores just a single QSO and passes the score back to the caller
This file will almost certainly be QSO-party-dependent.
'''

from datetime import datetime
from cabrillo.qso import frequency_to_band_m
from utilities import get_dxcc, debug_print
from config import COUNTIES_ACTIVATED_POINTS, COUNTIES_WORKED_POINTS, MOBILE_REQUIRED_QSOS

qso_modes = ['CW', 'PH', 'DG', 'RY']
qso_mode_names = ['cw_qsos', 'ph_qsos', 'dg_qsos', 'dg_qsos']

def score_a_qso(s, r, q, dup):
    if not q.valid:
        return 0
    
    qso_dup = make_dup(s, r, q)
    
    if qso_dup in dup['qsos']:
        q.valid = False
        r['valid_qsos'] -= 1
        return 0
    dup['qsos'].append(qso_dup)

    gets_mult = False
    if q.dx_exch not in dup['mults']:
        dup['mults'].append(q.dx_exch[1])
    else:
        return 0

    # increment qsos count for each mode
    if q.mo.upper() not in list(s.mode_points.keys()):
        r['errors'].append(f"BAD mode {q.mo} to {q.dx_call} Sept {q.date.strftime("%d")}th {q.date.strftime("%H:%M")}Z\n")
        return 0
    r[f"{q.mo.lower()}_qsos"] += 1

    # for ALL operators, record all counties they work
    if q.de_exch[1] in s.counties:
        r['counties_activated'].add(q.de_exch[1])
        # mobile operators - record their activations separately
        if q.de_call in s.mobile_callsigns:
            if q.de_exch[1] in list(r['mobile_activation_counts'].keys()):
                r['mobile_activation_counts'][q.de_exch[1]] += 1
            else:
                r['mobile_activation_counts'][q.de_exch[1]] = 1

    # for ALL operators, record each county where mobile op worked
    if q.dx_exch[1] in s.counties:
        r['counties_worked'].add(q.dx_exch[1])
        if q.dx_call in s.mobile_callsigns and q.dx_exch[1] in s.counties:
            r['mobile_worked_counties'].add(q.dx_exch[1])

    elif q.dx_exch[1] in s.states:
        r['states_worked'].add(q.dx_exch[1])
    elif q.dx_exch[1] in s.provinces:
        r['provinces_worked'].add(q.dx_exch[1])
    elif r['cab'].location == "DX":
        r['dx_worked'].add(get_dxcc(s, q.dx_exch[1], q.dx_call)[1])
    else:
        q.valid = False
        r['valid_qsos'] -= 1

    try:
        if q.freq[:2] == '50':
            band = '6'
        elif len(q.freq) in [4, 5]:
            band = frequency_to_band_m(q.freq)
        else:
            band = frequency_to_band_m(q.freq[:2] + '000')
        r['qsos_by_band'][band] += 1
        r['qsos_by_mode'][q.mo] += 1
    except:
        r['errors'].append(f"BAD frequency {q.freq} in call from {q.de_call} to {q.dx_call} Sept {q.date.strftime("%d")}th {q.date.strftime("%H:%M")}Z\n\n")

    # qsos by hour
    hour = int(q.date.strftime("%H"))
    if hour > 1:
        hour -= 14
    else:
        hour -= 2
    r["qsos_by_hour"][hour + ((int(q.date.strftime("%d")) - 19) * 12)] += 1
    # print(f"AFTER qsos_by_hour de {q.de_call}: total_qsos: {r['total_qsos']} valid: {r['valid_qsos']} hours {sum(r['qsos_by_hour'])}")

    # print('BREAK')

def score_an_operator(s, r):
    # accumulate all the points from qsos and mults for this one operator and score
    # See if operator is disqualified for multiple activated counties when not mobile
    # if r['callsign'] not in s.mobile_callsigns and len(r['counties_activated']) > 1:
    #     s.out_files['errors'].write(f"{r['callsign']} log disqualified: not mobile but activated multiple counties\n")
    #     return False, 0
    
    #accumulate qsos and mults and get score BEFORE BONUSES
    for m in list(s.mode_points.keys()):
        r['qso_points'] += r[f"{m.lower()}_qsos"] * s.mode_points[m]

    r['total_multipliers'] = (len(r['counties_worked']) + 
                              len(r['states_worked']) + 
                              len(r['provinces_worked']) + 
                              len(r['dx_worked']))
    r['score_wo_bonus'] = r['qso_points'] * r['total_multipliers']

    ''' bonus points for MOBILE OPERATORS for activations in counties
        mobile operator gets 500 for each county activated with
        at least 5 qsos.'''
    if r['callsign'] in s.mobile_callsigns:
        counties = 0
        for key in list(r['mobile_activation_counts'].keys()):
            if r['mobile_activation_counts'][key] >= 5:
                counties += 1
        r['mobile_bonus_points'] += (counties * COUNTIES_ACTIVATED_POINTS)

    ''' Bonus points for ALL operators for each county in which
        they worked a mobile operator'''
    r['mobile_bonus_points'] += (int(len(r['mobile_worked_counties'])  / ( MOBILE_REQUIRED_QSOS)) * COUNTIES_WORKED_POINTS)
    r['final_score'] = r['score_wo_bonus'] + r['mobile_bonus_points']
    

    # debug_print(s, r, "SCORED", False)
    return True, 0

def make_dup(s, r, qso):
    de = get_dxcc(s, r['cab'].location, r['callsign'])[1]
    dx = get_dxcc(s, qso.dx_exch[1].upper(), qso.dx_call.upper())[1]
    return "_".join([de, dx, qso.de_exch[1].upper(), qso.dx_exch[1].upper(), frequency_to_band_m(qso.freq), qso.mo.upper()])




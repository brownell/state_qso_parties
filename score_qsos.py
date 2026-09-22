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
from utilities import get_dxcc, debug_print

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
        r['errors'].append(f"BAD mode {q.mo} to {q.dx_call}")
        return 0
    r[f"{q.mo.lower()}_qsos"] += 1

    # increment qsos count for dx_exch
    # increment qsos SET for areas activated and worked
    if q.de_call == 'AA5AH':
        print('BREAK')
    if q.de_exch[1] in s.counties:
        r['counties_activated'].add(q.de_exch[1])

    if q.dx_exch[1] in s.counties:
        r['counties_worked'].add(q.dx_exch[1])

        '''mobile designation is added to each qso where dx_call is a 
          mobile station and dx_exch is a county '''
        # if q.dx_call in s.mobile_callsigns and q.dx_exch[1] in s.counties:
        #     if q.dx_call in list(r['mobile_counties_worked'].keys()):
        #         # callsign already here s   o add to set of dx_exch
        #         r['mobile_counties_worked'][q.dx_call].add(q.dx_exch[1])
        #     else: # adding new dx_call and creating new set
        #         r['mobile_counties_worked'][q.dx_call] = set([q.dx_exch[1]])

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
        r['errors'].append(f"BAD frequency {q.freq} in call from {q.de_call} to {q.dx_call}\n")

    # qsos by hour
    hour = int(q.date.strftime("%H"))
    if hour > 1:
        hour -= 14
    else:
        hour -= 2
    r["qsos_by_hour"][hour + ((int(q.date.strftime("%d")) - 19) * 12)] += 1
    # print(f"AFTER qsos_by_hour de {q.de_call}: total_qsos: {r['total_qsos']} valid: {r['valid_qsos']} hours {sum(r['qsos_by_hour'])}")

    '''Capturing calls to and from mobile operators is tricky. The structure serves three different purposes
        depending on whether the operator is 1. TX mobile, 2. NTX, or 3. TX NON-mobile
        Since all the bonus points depend on counts of QSOs related to exchange, both de and dx, we
        store separate de_exch and dx_exch counts IFF one of the exchanges is a county.
        1. mobile: every qso is stored here, with
        mobile_qsos: {
            'key is MOBILE callsign': {
                'key is exchange of OTHER operator
            }
        }
        '''

    # non-TX stations working TX mobile stations need to be tracked for bonus points
    if q.de_exch[1] != 'TX' and q.dx_exch[1] in s.mobile_callsigns:
        if q.de_exch not in list(s.ntx_bonus.keys()):
            # add this ntx station with the mobile is connected to
            s.ntx_bonus.setdefault(q.de_call, {q.dx_exch[1]: 1})
        elif q.de_call in list(s.ntx_bonus[q.de_call].keys()):
            # this pair of NTX op and TX mobile user exch already here, just increment
            s.ntx_bonus[q.de_call][q.dx_exch[1]] += 1
        else: # dx_call here, but add new dx_exch
            s.ntx_bonus[q.de_call].setdefault(q.dx_exch[1], 1)

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
    
    ''' MOBILE bonuses for TEXAS MOBILE operators
        Texas Mobiles—Add one thousand (1000) points to your FINAL SCORE per every county covered with at least five non-duplicate. Add five hundred (500) bonus points to your FINAL SCORE for each Texas mobile worked in five (5) different counties regardless of band or mode. If you work the same Texas mobile in five (5) additional counties, you add an additional five hundred (500) bonus points to your FINAL SCORE, etc. However, for bonus points you can only count one (1) contact per county per mobile.'''
    # if r['callsign'] in s['mobile_callsigns']:
    #     for county_count in r['mobile_counties_worked'][r['callsign']]:
    #         if county_count >= 5:





    ''' MOBILE bonuses for NON-TEXAS operators
        Non – Texas Stations—Add five hundred (500) bonus points to your FINAL SCORE for each Texas mobile worked in five (5) different counties regardless of band or mode. If you work the same Texas mobile in five (5) additional counties, you add an additional five hundred (500) bonus points to your FINAL SCORE, etc. However, for bonus points you can only count one (1) contact per county per mobile.'''
    

    ''' MOBILE bonuses for NON-MOBILE TEXAS operators
        Texas Stations—Add five hundred (500) bonus points to your FINAL SCORE for each Texas mobile worked in five (5) different counties regardless of band or mode. If you work the same Texas mobile in five (5) additional counties, you add an additional five hundred (500) bonus points to your FINAL SCORE, etc. However, for bonus points you can only count one (1) contact per county per mobile.'''

    debug_print(s, r, "SCORED", False)
    return True, 0

def make_dup(s, r, qso):
    de = get_dxcc(s, r['cab'].location, r['callsign'])[1]
    dx = get_dxcc(s, qso.dx_exch[1].upper(), qso.dx_call.upper())[1]
    return "_".join([de, dx, qso.de_exch[1].upper(), qso.dx_exch[1].upper(), frequency_to_band_m(qso.freq), qso.mo.upper()])




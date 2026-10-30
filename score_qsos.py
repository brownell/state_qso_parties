'''
Scores just a single QSO and passes the score back to the caller
This file will almost certainly be QSO-party-dependent.
'''
from datetime import datetime
import re
from cabrillo.qso import frequency_to_band_m
from utilities import get_dxcc
from database import save_result
from utilities import writefile, code_to_dxcc, exch_to_dxcc
from config import COUNTIES_ACTIVATED_POINTS, COUNTIES_WORKED_POINTS, MOBILE_REQUIRED_QSOS, CONTEST_YEAR
qso_types = ['CW', 'PH', 'DG', 'RY']
qso_type_names = ['cw_qsos', 'ph_qsos', 'dg_qsos', 'dg_qsos']

# after cross-check, we are going to score and save all the qsos

def score_all_qsos(s):
    for result in s.results:
        dup = {
            'qsos': [],
            'num_qso': 0,
            'mults': [],
            'num_mult': 0
        }
        for qso in result['cab'].qso:
            try:
                score_a_qso(s, result, qso, dup)
            except Exception as e:
                s.stats['exceptions'].append(f"failed to score a qso: {str(qso)}: {e}")
                if qso.valid:
                    # exception trying to score qso
                    qso.valid = False
                    s.stats['invalidated_qsos'] += 1
                    # result['valid_qsos'] -= 1
                    temp = f"Exception {e} when trying to score QSO"
                    writefile(s, result, qso, temp, ['errors'])
                continue
            if not qso.valid:
                continue

        score_an_operator(s, result)

        # save this operator and move on to the next
        try:
            saved = save_result(result, CONTEST_YEAR)
            if not saved:
                temp = f"Failed to save result for {result['callsign']}"
                writefile(s, result, qso, temp, ['errors'])
                print (f"could not save result for {result['callsign']}\n {str(qso)}")
        except Exception as e:
            s.stats['exceptions'].append(f"save result 2: {result['callsign']}: {e}")
            if qso and qso.valid:
                qso.valid = False
                s.stats['invalidated_qsos'] += 1
                result['valid_qsos'] -= 1
            temp = f"Exception {e} when trying to save result for {result['callsign']}"
            writefile(s, result, None, temp, ['errors'])
            print(f"Exception {e} when trying to save result (result)")

def score_a_qso(s, r, q, dup):
    if not q.valid:
        return False
    try:
        if q.dx_exch[1] not in dup['mults']:
            dup['mults'].append(q.dx_exch[1])
        else:
            dup['num_mult'] += 1
        # increment qsos count for each mode
        if q.mo.upper() == 'FM':
            q.mo = 'PH'
        if q.mo.upper() not in list(s.mode_points.keys()):
            temp = f"BAD mode {q.mo}"
            writefile(s, r, q, temp, ['errors'])
            q.valid = False
            s.stats['invalidated_qsos'] += 1
            return False

        # add 1 to qso type (CW, PH, etc)
        if q.mo.upper() not in list(s.stats['qsos_by_mode'].keys()):
            temp = f"Bad mode in qso: "
            writefile(s, r, q, temp, ['errors'])
            q.valid = False
            s.stats['invalidated_qsos'] += 1
            return False

        if q.freq[:2] == '50':
            band = '6'
        elif q.freq == '144':
            band = '2'
        elif '.' in q.freq:
            q.freq = q.freq.split('.')[0]
            band = frequency_to_band_m(q.freq)
        elif len(q.freq) in [4, 5]:
            band = frequency_to_band_m(q.freq)
        else:
            band = frequency_to_band_m(q.freq[:2] + '000')
        if band not in list(r['qsos_by_band'].keys()):
            temp = f"Frequency {q.freq} could not be converted to a band:"
            writefile(s, r, q, temp, ['errors', 'other_invalid_qsos'])
            q.valid = False
            s.stats['invalidated_qsos'] += 1
            return False

        # qsos by hour
        hour = int(q.date.strftime('%H'))
        if hour > 1:
            hour -= 14
        else:
            hour -= 2
        hour_of_24 = hour + ((int(q.date.strftime("%d")) - 19) * 12)

        # Put all the actual scoring at the end of this "try" block so that if anything goes wrong

        # we can catch it and mark the QSO as invalid
        r[f"{q.mo.lower()}_qsos"] += 1       
        r['qsos_by_mode'][q.mo.upper()] += 1
        s.stats['qsos_by_mode'][q.mo.upper()] += 1
        s.stats['scored_mode']  += 1
        r['qsos_by_band'][str(band)] += 1
        s.stats['qsos_by_band'][str(band)] += 1
        s.stats['scored_band'] += 1
        r["qsos_by_hour"][hour_of_24] += 1
        s.stats["qsos_by_hour"][hour_of_24] += 1
        s.stats['scored_hour'] += 1

        s.stats['scored_qsos'] += 1

    except Exception as e:
        s.stats['exceptions'].append(f"while scoring: {str(q)}: {q.valid}: {e}")
        if q.valid:
            q.valid = False
            s.stats['invalidated_qsos'] += 1
            r['valid_qsos'] -= 1
            r['other_invalid_qsos'] += 1
            temp = f"BAD frequency {q.freq}"
            writefile(s, r, q, temp, ['errors'])
        
    return

        # print(f"AFTER qsos_by_hour de {q.de_call}: total_qsos: {r['total_qsos']} valid: {r['valid_qsos']} hours {sum(r['qsos_by_hour'])}")

        # print('BREAK')

def score_an_operator(s, r):
    # accumulate all the points from qsos and mults for this one operator and score
    # See if operator is disqualified for multiple activated counties when not mobile
    try:
        if r['callsign'] not in s.mobile_callsigns and len(r['counties_activated']) > 1:
            s.out_files['errors'].write(f"{r['callsign']} log disqualified: not mobile but activated multiple counties\n")
            return False        
        #accumulate qsos and mults and get score BEFORE BONUSES
        for m in list(s.mode_points.keys()):
            r['qso_points'] += r[f"{m.lower()}_qsos"] * s.mode_points[m]

        r['total_multipliers'] = (len(r['counties_worked']) + len(r['states_worked']) +  len(r['provinces_worked']) + len(r['dx_worked']))
        r['score_wo_bonus'] = r['qso_points'] * r['total_multipliers'] 

        ''' bonus points for MOBILE OPERATORS for activations in counties
            mobile operator gets 500 for every five activations in a
            single county'''
        if r['callsign'] in s.mobile_callsigns:
            for key in list(r['mobile_activation_counts'].keys()):
                r['cab_mobile_points'] += int(r['mobile_activation_counts'][key] / MOBILE_REQUIRED_QSOS)  * COUNTIES_ACTIVATED_POINTS

        ''' Bonus points for ALL operators for each county in which
            they worked a mobile operator'''
        r['mtb_mobile_points'] += (int(len(r['worked_counties_mobile'])  / ( MOBILE_REQUIRED_QSOS))) * COUNTIES_WORKED_POINTS
        r['final_score'] = r['score_wo_bonus'] + r['mtb_mobile_points'] +  r['cab_mobile_points']
    except Exception as e:
        s.stats['exceptions'].append(f"score op: {r['callsign']}: {e}")
        temp = f"Exception {e} scoring operator {r['callsign']}"
        writefile(s, r, None, temp, ['errors'])
        print(f"could not score {r['callsign']}")
    return True
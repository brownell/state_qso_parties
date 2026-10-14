'''
Scores just a single QSO and passes the score back to the caller
This file will almost certainly be QSO-party-dependent.
'''
from datetime import datetime
from cabrillo.qso import frequency_to_band_m
from utilities import get_dxcc, debug_print
from database import save_result
from utilities import writefile
from config import COUNTIES_ACTIVATED_POINTS, COUNTIES_WORKED_POINTS, MOBILE_REQUIRED_QSOS, CONTEST_YEAR
qso_types = ['CW', 'PH', 'DG', 'RY']
qso_type_names = ['cw_qsos', 'ph_qsos', 'dg_qsos', 'dg_qsos']

# after cross-check, we are going to score and save all the qsos

def score_all_qsos(s):
    print(f"starting score_all_qsos: # results = {len(s.results)}")
    for result in s.results:
        if result['callsign'] == 'AD4EB':
            print('AE4DB')
            print('break')
        dup = {
            'qsos': [],
            'num_qso': 0,
            'mults': [],
            'num_mult': 0
        }
        if result['callsign'] == 'AD4EB':
            print('AE4DB')
            print('break')
        for qso in result['cab'].qso:
            qso.valid = True
            if not qso.valid:
                # already been marked as valid
                result['other_bad_qsos'] += 1
                temp = f"Failed to score QSO str(qso)"
                writefile(s, result, qso, 'errors', temp, errors = True, warning = False)
                continue
            try:
                score_a_qso(s, result, qso, dup)
            except Exception as e:
                # exception trying to score qso
                qso.valid = False
                result['valid_qsos'] -= 1
                temp = f"Exception {e} when trying to score QSO"
                writefile(s, result, qso, 'errors', temp, errors = True, warning = False)
                continue
            if not qso.valid:
                continue


        if result['callsign'] == 'AD4EB':
            print('AE4DB')
            print('break')
        score_an_operator(s, result)

        # save this operator and move on to the next
        try:
            saved = save_result(result, CONTEST_YEAR)
            if not saved:
                temp = f"Failed to save result for {result['callsign']}"
                writefile(s, result, qso, 'errors', temp, errors = True, warning = False)
                print (f"could not save result for {result['callsign']}\n {str(qso)}")
        except Exception as e:
            qso.valid = False
            result['valid_qsos'] -= 1
            temp = f"Exception {e} when trying to save QSO"
            writefile(s, result, qso, 'errors', temp, errors = True, warning = False)
            result['errors'].append(f"Exception {e} when trying to save QSO {str(qso)}")
            print(f"Exception {e} when trying to save QSO {str(qso)}")

def score_a_qso(s, r, q, dup):
    if not q.valid:
        if 'busted' in list(vars(q).keys()):
            # was marked busted previously so need to record this
            # in this op's result
            writefile(s, r, q, 'busteds', 'Busted QSO')
            writefile(s, r, q, 'errors', 'Busted QSO')
            r['busteds'] += 1
            r['busted_calls'].append([q.de_call, q.dx_call])
            s.stats['busteds'] += 1
        return False
    try:
        if q.dx_exch[1] not in dup['mults']:
            dup['mults'].append(q.dx_exch[1])
        else:
            dup['num_mult'] += 1

        # increment qsos count for each mode
        if q.mo.upper() not in list(s.mode_points.keys()):
            temp = f"BAD mode {q.mo}"
            writefile(s, r, q, 'errors', temp)
            raise Exception

        # add 1 to qso type (CW, PH, etc)
        r[f"{q.mo.lower()}_qsos"] += 1
        r['qsos_by_mode'][q.mo] += 1

        # for ALL operators, record all counties they work
        if q.de_exch[1] in s.counties:
            r['counties_activated'].add(q.de_exch[1])

        if q.dx_exch[1] in s.counties:
            r['counties_worked'].add(q.dx_exch[1])
        elif q.dx_exch[1] in s.states:
            r['states_worked'].add(q.dx_exch[1])
        elif q.dx_exch[1] in s.provinces:
            r['provinces_worked'].add(q.dx_exch[1])
        elif r['cab'].location == "DX":
            r['dx_worked'].add(r['dx_entity'])
        else:
            q.valid = False
            r['valid_qsos'] -= 1
            r['other_bad_qsos'] += 1
            temp = "Receiver's exch invalid:"
            writefile(s, r, q, 'invalid_qsos', temp)
        if q.freq[:2] == '50':
            band = '6'
        elif q.freq == '114':
            band = '2'
        elif '.' in q.freq:
            q.freq = q.freq.split('.')[0]
        elif len(q.freq) in [4, 5]:
            band = frequency_to_band_m(q.freq)
        else:
            band = frequency_to_band_m(q.freq[:2] + '000')
        r['qsos_by_band'][band] += 1

        # qsos by hour
        hour = int(q.date.strftime("%H"))
        if hour > 1:
            hour -= 14
        else:
            hour -= 2
        r["qsos_by_hour"][hour + ((int(q.date.strftime("%d")) - 19) * 12)] += 1

    except Exception as e:
        q.valid = False
        r['valid_qsos'] -= 1
        r['other_bad_qsos'] += 1
        temp = f"BAD frequency {q.freq}"
        writefile(s, r, q, 'errors', temp)
        writefile(s, r, q, 'errors', temp)
        
    return

        # print(f"AFTER qsos_by_hour de {q.de_call}: total_qsos: {r['total_qsos']} valid: {r['valid_qsos']} hours {sum(r['qsos_by_hour'])}")

        # print('BREAK')

def score_an_operator(s, r):
    # accumulate all the points from qsos and mults for this one operator and score
    # See if operator is disqualified for multiple activated counties when not mobile
    if r['callsign'] == 'AD4EB':
        print('AE4DB')
        print('break')
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
        temp = f"Exception {e} scoring operator {r['callsign']}"
        writefile(s, r, None, 'errors', temp)
        print(f"could not score {r['callsign']}")
    return True
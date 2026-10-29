'''
Utility functions for the State QSO Party contest. These don't have any role in the main processing logic.
They simply provide functions related to ham radio, like converting a frequency to its corresponding band, 
or checking if a callsign is valid. 
'''
from config import QRZ_CALLSIGN, QRZ_PASSWORD
from pyhamtools import LookupLib, Callinfo
from pprint import pprint
import json
from datetime import datetime, timedelta
from cabrillo import QSO
from share import SHARED as s
from config.config_txqp import STATISTICS_TEXT
import re
from cabrillo.qso import frequency_to_band_m

# to get country name and ADIF number from callsign
my_lookup_lib = LookupLib(lookuptype='countryfile', filename='./reference_data/cty.plist', username=QRZ_CALLSIGN, pwd=QRZ_PASSWORD)
my_callinfo = Callinfo(my_lookup_lib)

def exch_to_dxcc(s, exch):
    if exch in (s.exch_to_dxcc):
        return s.exch_to_dxcc(exch)
    else:
        return None, None

def code_to_dxcc(s, code):
    if code in (s.code_to_dxcc):
        return s.code_to_dxcc(code)
    else:
        return None

def get_dxcc(s, location, callsign):
    ## check if this log is from a DX station, and save the dxcc_entity which will be used for cross-checking
    if location == 'DX' or (location not in s.states and location not in s.provinces and location not in s.counties):
        # it's not in US or Canada
        try:
            callinfo = my_callinfo.get_all(callsign)
        except:
            try:
                callinfo = my_callinfo.get_all(callsign)
            except:
                return 0, callsign

        if len(callinfo) > 0 and (callinfo['country'] not in ['United States', 'Canada']):
            return callinfo['adif'], callinfo['country']
            
    return 0, callsign

def writefile(s, result, qso, intro, err_types = ['errors']):
    if type(err_types) is not list:
        err_types = [err_types]
    for err in err_types:
        temp = f"{intro}"
        if qso == None:
            try:
                s.out_files[err].write(f"{temp}\n")
            except:
                pass
            try:
                result[err].append([f"{temp}"])
            except:
                pass
        else:
            try:
                s.out_files[err].write(f"{temp}: {str(qso)}\n")
            except:
                pass
            try:
                result[err].append([f"{temp}: {str(qso)}"])
            except:
                pass

def generate_index_key(s, qso, call_to_use, mirror):
    # to generate the index key for the qso_index_dict
    # this is used to search for matches in cross_check
    if mirror == False:
        return call_to_use.split('/')[0] + qso.de_exch[1].split('/')[0].upper() + qso.dx_exch[1].split('/')[0].upper() + qso.mo.upper() + frequency_to_band_m(qso.freq)
    else:
        return call_to_use.split('/')[0] + qso.dx_exch[1].split('/')[0].upper() + qso.de_exch[1].split('/')[0].upper() + qso.mo.upper() + frequency_to_band_m(qso.freq)
    
COUNTS = [
    'counties_worked', 
    'states_worked', 
    'provinces_worked', 
    'dx_worked' 
    ]
INTG = ['final_score', 'score_wo_bonus', 'mtb_mobile_points', 'total_multipliers', 'qso_points', 'total_qsos', 'valid_qsos', 'cw_qsos', 'ph_qsos', 'dg_qsos', 'ry_qsos'
    ] 

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

def is_exchange_match(qso, dx_qso, min_time, max_time) -> bool:
    # frequency, mode, and the sender's callsign must match
    # and the time must be a near match
    if min_time <= getattr(dx_qso, 'date') <= max_time:
        if is_fuzzy_match(qso.de_exch[1], dx_qso.dx_exch[1]) and is_fuzzy_match(qso.dx_exch[1], dx_qso.de_exch[1]) :
            return True
    else: 
        return False
    
def get_near_match(s, qso, result, dx_result, within: int = 1):
    '''return one and only one match.
        We are only doing a fuzzy match on the sender's de_call
         and the receiver's dx_call. The exchanges must be an
            EXACT match '''
    dx_qsos = dx_result['cab'].qso
    target_time = getattr(qso, 'date')
    delta = timedelta(minutes=within)
    min_time = target_time - delta
    max_time = target_time + delta
    matched_q = None
    for q in dx_qsos:
        matched_q = None
        potential_fuzzies = 0
        # everything must match Exactly except the callsign.
        # we know the qso.dx_call == q.de_call, because we would not be
        # looking in this log file otherwise
        if not (frequency_to_band_m(q.freq) == frequency_to_band_m(q.freq) and q.mo == q.mo and qso.de_call == q.dx_call and (min_time <= getattr(q, 'date') <= max_time)):
            continue
        potential_fuzzies += 1
        # if exch exact, calls must fuzzy match
        if qso.de_exch[1] == q.dx_exch[1] and qso.dx_exch[1] == q.de_exch[1]:
            # qsos exact match, see if callsigns fuzzy match
            if is_fuzzy_match(qso.de_call, q.dx_call):
                matched_q = q
                break
        continue # matched on base values in qsos   
    if matched_q == None:
        qso_nil(s, qso, result)
        return None
    else:
        qso_busted(s, matched_q, dx_result)
        return matched_q

def qso_busted(s, qso, result):
    # if result['dxcc_entity'] != result['callsign']:
    #     print(f"busted with dxcc_entity {result['dxcc_entity']}\n{qso}")
    qso.valid = False
    s.stats['invalidated_qsos'] += 1
    result['busteds'] += 1
    result['busted_calls'].append([qso.de_call, qso.dx_call])
    s.stats['busteds'] += 1
    s.stats['busted_calls'].append([qso.de_call, qso.dx_call])
    writefile(s, result, qso, "Busted: error in sender log in fuzzy match", ['busteds', 'errors'])

def qso_nil(s, qso, result):
    qso.valid = False
    s.stats['invalidated_qsos'] += 1
    result['nils'] += 1
    result['nil_calls'].append([qso.de_call, qso.dx_call])
    s.stats['nils'] += 1
    s.stats['nil_calls'].append([qso.de_call, qso.dx_call])
    writefile(s, result, qso, "Not In Log: no match found in dx_call's log", ['nils'])

def capture_mobile(s, result, dx_result, qso, match):
    '''mobile_activation counts = {'county': # activations}
        worked_counties_mobile = {mobile call:  set(counties mobile contacted in)}
        call capture_qsos twice, reversing the order of the arguments
        to account for either of the ops being modile'''
    if qso.de_call not in s.mobile_callsigns and match != None and match.de_call not in s.mobile_callsigns:
        return
    # for the mobile users, save the county they are activating
    if qso.de_call in s.mobile_callsigns:
        capture_contacts(s, result, dx_result, qso)
    if match != None and match.de_call in s.mobile_callsigns:
        capture_contacts(s, dx_result, result, match)

def capture_contacts(s, result1, result2, qso):
    if qso.de_exch[1] in list(result1['mobile_activation_counts'].keys()):
        result1['mobile_activation_counts'][qso.de_exch[1]] += 1
        s.stats['mobile_activation_counts'][qso.de_exch[1]] += 1
    else:
        result1['mobile_activation_counts'][qso.de_exch[1]] = 1
        s.stats['mobile_activation_counts'][qso.de_exch[1]] = 1

    if qso.de_call in list(result2['worked_counties_mobile'].keys()):
        result2['worked_counties_mobile'][qso.de_call].add(qso.de_exch[1])
        s.stats['worked_counties_mobile'][qso.de_call].add(qso.de_exch[1])
    else:
        result2['worked_counties_mobile'][qso.de_call] = {qso.de_exch[1]}
        s.stats['worked_counties_mobile'][qso.de_call] = {qso.de_exch[1]}

def fix_stats(s):
    # do some fixup of the stats after all are collected
    s.stats['num_states_worked'] = len(s.stats['states_worked'])
    s.stats['num_provinces_worked'] = len(s.stats['provinces_worked'])
    s.stats['num_dx_worked'] = len(s.stats['dx_worked'])
    s.stats['num_counties_activated'] = len(s.stats['counties_activated'])
    s.stats['num_counties_activated_mobile'] = 0
    s.stats['num_counties_worked'] = len(s.stats['counties_worked'])

    save_stats(s, "Statistics")

def save_stats(s, message):
    stats_keys = list(s.stats.keys())
    for k in list(STATISTICS_TEXT.keys()):
        if k in stats_keys:
            print(f"{STATISTICS_TEXT[k]}: {s.stats[k]}")
            s.out_files['stats'].write(f"{STATISTICS_TEXT[k]}: {s.stats[k]}\n")
        else:
             print(f"\n*** {STATISTICS_TEXT[k]} ***")
             s.out_files['stats'].write(f"\n*** {STATISTICS_TEXT[k]} ***\n")

# def debug_print(s, r, title, p=True):
    # x = {}
    # y = {}
    # for z in COUNTS:
    #     x[z] = r[z]
    # for w in  INTG:
    #     y[w] = r[w]
    # s.out_files['debug'].write(f"{title.upper()} {r['callsign']}\n")
    # for z in x:
    #      s.out_files['debug'].write(f"{z}")
    # s.out_files['debug'].write(f"\n")   
    # for z in y:
    #      s.out_files['debug'].write(f"{len(z)}")
    # s.out_files['debug'].write(f"{r['final_score']} {r['mtb_mobile_points']} {r['score_wo_bonus']} {r['total_multipliers']} {r['qso_points']} {r['ph_qsos']} {r['cw_qsos']} {r['callsign']}\n")   
    # counts: {y}  sets: {x} mobile {r['callsign'] in s.mobile_callsigns}\n")
    # if len(r['errors']) > 0:
    #      s.out_files['debug'].write(f"{r['errors']}\n")
    # s.out_files['debug'].write(f"\n")
    # if p:
    #     pprint(f"{title.upper()} {r['callsign']} hours: {sum(r['qsos_by_hour'])} counts: {y}  sets: {x} hours: {sum(r['qsos_by_hour'])}")
    #     if len(r['errors']) > 0:
    #         print(f"{r['errors']}")


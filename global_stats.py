
from pprint import pprint
import sys
import copy
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest import result
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from utilities import generate_index_key, get_dxcc, writefile

# Import your existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    CONTEST_YEAR, BATCH_INPUT_DIR, HQ_FIELDS
)
SCRIPT_DIR = Path(__file__).resolve().parent

def fix_exchange(s, exchange, callsign, code = 0, entity=""):
    """
    Fix the exchange to be "DX" + the DXCC code (integer) if the exchange is a foreign exchange.
    This function is called after reading and preparing each log file.
    It checks the exchange to determine if it is a foreign exchange, and if so, it modifies the exchange to be "DX" + the DXCC code.
    Returns True if was a foreign exchange, False if not.
    """
    if entity == "":
        code, entity = get_dxcc(s, 'DX', callsign)
    if entity != callsign and exchange.isalpha():
        # store the results of this get_dxcc call for later use in scoring and reporting
        s.code_to_dxcc[code] = entity
        exchange = 'DX' + str(code)
    return code, entity

def categorize_log(s, result, qso):
    """
    Categorize the log based on the exchanges in the QSOs.
    This function is called after reading and preparing each log file.
    It checks the exchanges in the QSOs to determine if the log is from a TX county, state, province, or DX station.
    It also updates the stats counters for the number of logs in each category.
    """
    # categorize the logs as to where they come from
    # we can't just compare the exchanges to the lists of counties, states, and provinces because
    # some of the foreigh exchanges may have the same string as these. So first we need to check
    # the sender and receiver exchanges, and capture the DXCC information for them if 
    # the are foreign. We also modify the exchanges to be "DX" + the DXCC code 
    #  so that we can use them in scoring and reporting.
    
    # categorize the logs as to where they come from
    # we can't just compare the exchanges to the lists of counties, states, and provinces because
    # some of the foreigh exchanges may have the same string as these. So first we need to check
    # the sender and receiver exchanges, and capture the DXCC information for them if 
    # the are foreign. We also modify the exchanges to be "DX" + the DXCC code 
    #  so that we can use them in scoring and reporting.
    cab = result['cab']

    # first look at the sender, since we have the result and cab object
    # if de_exch CAN be a country, fix the exchange to be "DX" + dxcc entity code (integer)
    code, entity = fix_exchange(s, qso.de_exch[1], qso.de_call, result['dxcc_entity'])
    if code > 0:
        s.stats['dx_logs'] += 1
        return True
    # see if de exchange is a county
    elif qso.de_exch[1] in s.counties:
        # this is a TX log, so add it to the set of TX callsigns
        # is it mobile or fixed? check the cab.category for "MOBILE"
        if 'MOBILE' in cab.category:
            s.mobile_callsigns.add(cab.callsign)
            s.stats['tx_mobile_logs'] += 1
            return True
        else:
            s.stats['tx_fixed_logs'] += 1
            return True
    # see if de exchange is a state
    elif qso.de_exch[1] in s.states:
        s.stats['us_logs'] += 1
        return True
    # see if de exchange is a province
    elif qso.dx_exch[1] in s.provinces or (len(qso.dx_exch[1]) > 2 and qso.dx_exch[1][:2] == qso.dx_call[:2]):
        s.stats['cdn_logs'] += 1
        return True
    else:
        qso.valid = False  # so it will not be used in scoring
        writefile(s, result, qso, 'Invalid QSO: bad de exchange', ['errors', 'other_invalid_qsos'])
        result['other_invalid_qsos'] += 1
        s.stats['other_invalid_qsos'] += 1
        s.stats['invalidated_qsos'] += 1
        return False

def record_recipient_location(s, qso, result):
    # look at the receiver of the QSO
    # have the result and cab objects
    # if dx_exch CAN be a country, fix the exchange to be "DX" + dxcc entity code (integer)
    # code, entity = get_dxcc(s, 'DX', qso.dx_call)
    # if entity != qso.dx_call and (qso.dx_exch[1].isalpha() or qso.dx_call[:2] == qso.dx_exch[1][:2] or len(qso.dx_exch[1]) == 3):
    code, entity = fix_exchange(s, qso.dx_exch[1], qso.dx_call)
    if code > 0:
        # store the results of this get_dxcc call for later use in scoring and reporting
        s.code_to_dxcc[code] = entity
        s.stats['qsos_with_dx'] += 1
        s.stats['with_receiver'] += 1
        s.stats['dx_worked'].add(entity)
    elif qso.dx_exch[1] in s.counties:
        s.stats['qsos_with_tx'] += 1
        s.stats['with_receiver'] += 1
        s.stats['counties_worked'].add(qso.dx_exch[1])
    elif qso.dx_exch[1] in s.provinces or (len(qso.dx_exch[1]) > 2 and qso.dx_exch[1][:2] == qso.dx_call[:2]):
        s.stats['qsos_with_canada'] += 1
        s.stats['with_receiver'] += 1
        s.stats['provinces_worked'].add(qso.dx_exch[1])
    elif qso.dx_exch[1] in s.states:
        s.stats['qsos_with_us'] += 1
        s.stats['with_receiver'] += 1
        s.stats['states_worked'].add(qso.dx_exch[1])
    else:
        qso.valid = False  # so it will not be used in scoring
        writefile(s, result, qso, 'Invalid QSO: bad dx exchange', ['errors', 'other_invalid_qsos'])
        result['other_invalid_qsos'] += 1
        s.stats['other_invalid_qsos'] += 1
        s.stats['invalidated_qsos'] += 1
        s.stats['bad_exchanges'].add(qso.dx_exch[1])
        return False
    return True
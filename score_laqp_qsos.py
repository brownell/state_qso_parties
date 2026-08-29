'''

'''

import math
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from batch import shared as s
from config.config import CONTEST_YEAR, CW_DIGITAL_QSO_POINTS, EXTRA_BONUS_POINTS, COUNTIES_FILE, STATES_FILE, PROVINCES_FILE, DXCC_ENTITIES_FILE, DATABASE_FILE, TIME_WINDOW_MINUTES, ENABLE_FUZZY_MATCHING, MAX_EDIT_DISTANCE, BONUS_CALLSIGN, COUNTIES_FILE, OVERLAY_VALUE_OPTIONS, POWER_VALUE_OPTIONS, STATION_VALUE_OPTIONS, STATES_FILE, PROVINCES_FILE, EXTRA_BONUS_YEAR, EXTRA_BONUS_CALLS, EXTRA_BONUS_POINTS, US_PREFIXES, CANADIAN_PREFIXES,QRZ_CALLSIGN, QRZ_PASSWORD, PHONE_QSO_POINTS, CW_DIGITAL_QSO_POINTS, DXCC_ENTITIES_FILE, CALLSIGN_BONUS_POINTS, ROVER_COUNTY_BONUS, PHONE_MODES, CW_DIGITAL_MODES, BAND_RANGES

def score_qsos() -> None:
    '''
    The code here is specific to the Louisiana QSO Party.  It scores the QSOs in each log based on the contest rules.  It also checks for duplicate QSOs and multipliers.  The results are stored in the result dictionary for each log.
    A mult dup is when a QSO is a duplicate for multiplier purposes (same band/mode/rcvd_qth) but not a point dup (different rcvd_call).  These get qso points (if otherwise valid) but not  multipliers.  
    # A qso dup is when all of band/mode/rcvd_call are the same, in which case it should not count for points or multipliers.
    '''
    
    qso_dups = []
    mult_dups = []
    for qso in result['qsos']:
        # Skip QSOs flagged by cross-checking
        if qso.get('xcheck', '') != '':
            continue  # Error from cross-checking, skip for scoring
    
        band = qso['band']
        mode_cat = qso['mode_category']
        sent_call = qso['sent_call']
        rcvd_call = qso['rcvd_call']
        sent_qth = qso['sent_qth']

        ## if rcvd_call is a DX, then replace rcvd_qth with DXCC code (ADIF number as string)
        try:
            dx_rcvd_qth  = processor.my_callinfo.get_all(rcvd_call)
        except Exception as e:
            result['warnings'].append(f"ERROR QSO: cannot get rcvd_qth for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")
            print(f"Exception {e} sender {result['callsign']} cannot get rcvd_qth for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")

        try:            
            if dx_rcvd_qth and ((dx_rcvd_qth['country'] not in ['United States', 'Canada'])): # working DX station
                rcvd_qth = processor.dxcc_entities[int(dx_rcvd_qth['adif'])]
                dx_rcvd_qth['dxcc_entity'] = rcvd_qth
                # print(f"rcvd_qth is dx: sender sent_qth {sent_qth} receiver {rcvd_qth}")
            
                ## make sure this is not DX to DX
                if len(result['dxcc_entity']) > 0: # call from one DX to another -> invalid
                    result['warnings'].append(f"DUPLICATE QSO line one DX station to another {qso['line_num']} band: {band} mode: {mode_cat} sender: {sent_call} sender QTH: {result['dxcc_entity']} remote op: {rcvd_call} remote QTH: {rcvd_qth}")
                    continue
            else:
                rcvd_qth = qso['rcvd_qth']
                dx_rcvd_qth = None
        except Exception as e:
            rcvd_qth = qso['rcvd_qth']
            dx_rcvd_qth = None
            result['warnings'].append(f"ERROR QSO: cannot determine if rcvd_qth is DX for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")
            print(f"Exception {e} sender {result['callsign']} cannot determine if rcvd_qth is DX for callsign on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_call}")

        # NOT DX - ROVER gets a qso_check that includes his QTH because he can call same
        # station multiple toimes from different counties
        if result['location_type'] == "LA-ROVER":
                qso_check = band + mode_cat + sent_qth + rcvd_call
                if sent_qth not in result['counties_activated']:
                    result['counties_activated'].add(sent_qth)
        else: ## MUST be LA Fixed or State or Province
            qso_check = band + mode_cat + rcvd_call

        if result['location_type'] == "LA-FIXED" and sent_qth not in result['counties_activated']:
            result['counties_activated'].add(sent_qth)
                
        if qso_check in qso_dups:
            result['warnings'].append(f"DUPLICATE QSO line {qso['line_num']} band/mode/call worked:  {band}, {mode_cat}, {rcvd_call}")
        else:  ## not a duplicate for points, so get points
            result['valid_qsos'] += 1
            # print(f"NOT DUP QSO line {qso['line_num']} band/mode/call worked:  {band}/{mode_cat}/{rcvd_call}")
            # print(f"valid_qsos {result['valid_qsos']} qso_check {qso_check} band/sentqth/rcvd_call: {qso['band']} {qso['rcvd_qth']} {qso['rcvd_call']}")
            qso_dups.append(qso_check)

        # Track bands worked and QSO by band (for display only, does not impact score)
        result['bands_worked'].add(band)
        result['qsos_by_band'][band] += 1

        # Track qsos by hour (2-hour blocks)
        try:
            temp = int(qso['time'][:2] + "00")
            if temp < 999 or temp > 2600:
                temp = 2400
            result['qsos_by_hour'][temp] += 1
        except Exception as e:
            print(f"Error tying to get the QSO time {e}")
            result['warnings'].append(f"Bad time value on line {qso['line_num']} WORKED: band {band} mode {mode_cat} remote op {rcvd_qth}")
            continue
        
        # Award points
        if mode_cat == 'Phone':
            result['qso_points'] += PHONE_QSO_POINTS
            # print(f"qso_points {result['qso_points']} total_qsos {result['total_qsos']} valid_qsos {result['valid_qsos']}")
            result['qsos_by_mode']['Phone'] += 1
        else:  # CW/Digital
            result['qso_points'] += CW_DIGITAL_QSO_POINTS
            # print(f"qso_points {result['qso_points']} total_qsos {result['total_qsos']} valid_qsos {result['valid_qsos']}")
            result['qsos_by_mode']['CW/Digital'] += 1

        # Check for N5LCC
        if rcvd_call == 'N5LCC':
            result['worked_n5lcc'] = True
            result['num_n5lcc_contacts'] += 1

        ## MULTIPLIERS

        mult_check = band + mode_cat + rcvd_qth
        if mult_check not in mult_dups:
            mult_dups.append(mult_check)

            ## Everyone gets county multiplier for counties, but only LA stations get state/province/DX multipliers
            if rcvd_qth in processor.counties:
                result['counties_worked'].add(rcvd_qth)
                result['counties_worked_multiplier'] += 1
            
            # LA stations get state, province, and DX multipliers
            if result['location_type'] == 'LA-FIXED' or result['location_type'] == 'LA-ROVER':
                if dx_rcvd_qth:  ## DX multiplier
                    result['dx_worked'].add(dx_rcvd_qth['dxcc_entity'])
                    result['dx_worked_multiplier'] += 1
                # LA: states, provinces, DX are multipliers
                elif rcvd_qth in processor.provinces:
                    result['provinces_worked'].add(rcvd_qth)
                    result['provinces_worked_multiplier'] += 1
                elif rcvd_qth in processor.states:
                    result['states_worked'].add(rcvd_qth)
                    # print(result['states_worked'])
                    # print(f"rcvd_qth: {rcvd_qth}")
                    result['states_worked_multiplier'] += 1

    # print("break before points")
    # Finished with points, now sum the individual multipliers
    for i in ['counties', 'states', 'provinces', 'dx']:
        result['total_multipliers'] += result[f'{i}_worked_multiplier']
        
    ## score before bonuses
    result['final_score'] = result['qso_points'] * result['total_multipliers']

    ## add bonus points for one or more N5LCC contacts
    if result['worked_n5lcc']:
        result['final_score'] += CALLSIGN_BONUS_POINTS

    ## Add rover bonus points for activated counties
    if result['location_type'] == 'LA-ROVER':
        result['rover_bonus_points'] = len(result['counties_activated']) * ROVER_COUNTY_BONUS
        result['final_score'] += result['rover_bonus_points']

    ## Bonus for something outside of QSOs
    if result['callsign'] in EXTRA_BONUS_CALLS and contest_year == EXTRA_BONUS_YEAR:
        result['final_score'] += EXTRA_BONUS_POINTS
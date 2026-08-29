
from cabrillo.qso import frequency_to_band_m

qso_modes = ['CW', 'PH', 'DG', 'RY']
qso_mode_names = ['cw_qsos', 'ph_qsos', 'dg_qsos', 'dg_qsos']

def score_a_qso(s, result, qso, dup):
    qso_dup = "_".join([qso.dx_call.upper().split("/")[0], frequency_to_band_m(qso.freq), qso.mo.upper(), qso.de_call.upper(), qso.de_exch[1].upper(), qso.dx_exch[1].upper()])
    mult_dup = qso.dx_exch
    if qso_dup in dup['qsos']:
        return
    dup['qsos'].append(qso_dup)

    # increment qsos count for mode
    result[qso_mode_names[qso_modes.index(qso.mo)]]
   
    if qso.dx_exch not in dup['mults']:
        dup['mults'].append(qso.dx_exch)

    if qso.de_exch in s.counties:
        result['counties_activated'].append(qso.de_exch)

    elif qso.dx_exch in s.states:
        result['states_worked'].append(qso.dx_exch)

    elif qso.dx_exch in s.provinces:
        result['states_worked'].append(qso.dx_exch)

    else:
        # should be a DX station - get its DXCC ID
        




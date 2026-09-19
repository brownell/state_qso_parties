'''
These are utility functions that are specific to a particular state QSO party.
Each new state QSO party will modify the functions in this file to reflect the rules of that particular contest.
'''

from batch import shared as s

# get location type of a QSO's sender
# an Example for Louisiana
def determine_location_type() -> str:
        """Determine location type from QSOs"""
        
        initial_qso = True
        
        for qso in s.result['qsos']:
            sent_qth = qso['sent_qth'].replace('DX', '')
            sent_call = qso['sent_call']

            if initial_qso:
                initial_qso = False
                s.result['exchange'] = sent_qth
            
            
            # Check if DX
            callinfo = my_callinfo.get_all(sent_call)
            if callinfo and callinfo['country'] not in ['United States', 'Canada']:
                return 'DX'
            
            # Check if non-LA
            if (sent_qth in s.states) or (sent_qth in s.provinces):
                return 'NON-LA'
        
        # Determine if fixed or rover
        station = s.result['location_type']  # Get station type
        
        if station in ('MOBILE', 'ROVER'):
            return 'LA-ROVER'
        elif station in ('FIXED', 'PORTABLE'):
            return 'LA-FIXED'
        else:
            return 'LA-FIXED'
    
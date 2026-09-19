'''
Utility functions for the State QSO Party contest. These don't have any role in the main processing logic.
They simply provide functions related to ham radio, like converting a frequency to its corresponding band, 
or checking if a callsign is valid. 
'''
from config import QRZ_CALLSIGN, QRZ_PASSWORD
from pyhamtools import LookupLib, Callinfo
from cabrillo.qso import frequency_to_band_m

# to get country name and ADIF number from callsign
my_lookup_lib = LookupLib(lookuptype='countryfile', filename='./reference_data/cty.plist', username=QRZ_CALLSIGN, pwd=QRZ_PASSWORD)
my_callinfo = Callinfo(my_lookup_lib)

def get_dxcc(s, location, callsign):
        ## check if this log is from a DX station, and save the dxcc_entity which will be used for cross-checking
        if location == "DX" or (location not in s.states and location not in s.provinces and location not in s.counties):
            # it's not in US or Canada
            callinfo = my_callinfo.get_all(callsign.split('/')[0])
            if callinfo and callinfo['country'] in ['United States', 'Canada']:
                return 0, callsign
            else:
                return callinfo['adif'], callinfo['country']
        else:
            return 0, callsign

def generate_index_key(s, qso, call_to_use, mirror):
    # to generate the index key for the qso_index_dict
    # this is used to search for matches in cross_check
    if mirror == False:
        return call_to_use + qso.de_exch[1].upper() + qso.mo.upper() + frequency_to_band_m(qso.freq)
    else:
        return call_to_use + qso.dx_exch[1].upper() + qso.mo.upper() + frequency_to_band_m(qso.freq)
"""
    From Chuck NO5W

"""
# def freq_to_band(freq_khz: int) -> int:
#     """
#     Convert frequency in kHz to band in meters.
    
#     Args:
#         freq_khz: Frequency in kHz
    
#     Returns:
#         Band in meters (e.g., 20, 40, 80) or None if not in a valid band
#     """
#     for band, (min_freq, max_freq) in BAND_RANGES.items():
#         if min_freq <= freq_khz <= max_freq:
#             return band
#     return None

# def _get_dx_info(callsign):
#     callinfo = s.my_callinfo.get_all(callsign)
#     if callinfo and callinfo['country'] in ['United States', 'Canada']:
#         return None
#     else:
#         return [callinfo['adif'], callinfo['country']]

# def get_callsign_prefix(call: str) -> str:
#     """Extract prefix from callsign"""
#     for i, char in enumerate(call):
#         if char.isdigit():
#             if i < 1:
#                 return call[:1]
#             else:
#                 return call[:i]
#     return call

# def is_dx_callsign(call: str) -> bool:
#     """Check if callsign is DX (not US or VE)"""
#     prefix = get_callsign_prefix(call)
#     if not prefix:
#         return False
    
#     # US callsigns
#     if prefix[0] in ('K', 'N', 'W'):
#         return False
#     if prefix in US_PREFIXES:
#         return False
    
#     # Canadian callsigns
#     if prefix in CANADIAN_PREFIXES:
#         return False
    
#     return True
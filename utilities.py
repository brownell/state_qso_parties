'''
Utility functions for the State QSO Party contest. These don't have any role in the main processing logic.
They simply provide functions related to ham radio, like converting a frequency to its corresponding band, 
or checking if a callsign is valid. 
'''

def freq_to_band(freq_khz: int) -> int:
    """
    Convert frequency in kHz to band in meters.
    
    Args:
        freq_khz: Frequency in kHz
    
    Returns:
        Band in meters (e.g., 20, 40, 80) or None if not in a valid band
    """
    for band, (min_freq, max_freq) in BAND_RANGES.items():
        if min_freq <= freq_khz <= max_freq:
            return band
    return None

def _get_dx_info(callsign):
    callinfo = s.my_callinfo.get_all(callsign)
    if callinfo and callinfo['country'] in ['United States', 'Canada']:
        return None
    else:
        return [callinfo['adif'], callinfo['country']]

def get_callsign_prefix(call: str) -> str:
    """Extract prefix from callsign"""
    for i, char in enumerate(call):
        if char.isdigit():
            if i < 1:
                return call[:1]
            else:
                return call[:i]
    return call

def is_dx_callsign(call: str) -> bool:
    """Check if callsign is DX (not US or VE)"""
    prefix = get_callsign_prefix(call)
    if not prefix:
        return False
    
    # US callsigns
    if prefix[0] in ('K', 'N', 'W'):
        return False
    if prefix in US_PREFIXES:
        return False
    
    # Canadian callsigns
    if prefix in CANADIAN_PREFIXES:
        return False
    
    return True
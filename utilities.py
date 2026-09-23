'''
Utility functions for the State QSO Party contest. These don't have any role in the main processing logic.
They simply provide functions related to ham radio, like converting a frequency to its corresponding band, 
or checking if a callsign is valid. 
'''
from config import QRZ_CALLSIGN, QRZ_PASSWORD
from pyhamtools import LookupLib, Callinfo
from pprint import pprint
from cabrillo.qso import frequency_to_band_m

# to get country name and ADIF number from callsign
my_lookup_lib = LookupLib(lookuptype='countryfile', filename='./reference_data/cty.plist', username=QRZ_CALLSIGN, pwd=QRZ_PASSWORD)
my_callinfo = Callinfo(my_lookup_lib)

def get_dxcc(s, location, callsign):
    ## check if this log is from a DX station, and save the dxcc_entity which will be used for cross-checking
    if location == "DX" or (location not in s.states and location not in s.provinces and location not in s.counties):
        # it's not in US or Canada
        try:
            callinfo = my_callinfo.get_all(callsign.split('/')[0])
        except:
            try:
                callinfo = my_callinfo.get_all(callsign.split('/')[1])
            except:
                return 0, callsign

        if not (callinfo and callinfo['country'] in ['United States', 'Canada']):
            # print(f"FOREIGN CALLSIGN location: {location} Call: {callsign}")
            return callinfo['adif'], callinfo['country']
            
    return 0, callsign

def generate_index_key(s, qso, call_to_use, mirror):
    # to generate the index key for the qso_index_dict
    # this is used to search for matches in cross_check
    if mirror == False:
        return call_to_use + qso.de_exch[1].upper() + qso.mo.upper() + frequency_to_band_m(qso.freq)
    else:
        return call_to_use + qso.dx_exch[1].upper() + qso.mo.upper() + frequency_to_band_m(qso.freq)
    
COUNTS = [
    'counties_worked', 
    'states_worked', 
    'provinces_worked', 
    'dx_worked' 
    ]
INTG = ['final_score', 'score_wo_bonus', 'mobile_bonus_points', 'total_multipliers', 'qso_points', 'total_qsos', 'valid_qsos', 'cw_qsos', 'ph_qsos', 'dg_qsos', 'ry_qsos'
    ]        

def debug_print(s, r, title, p=True):
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
    s.out_files['debug'].write(f"{r['final_score']} {r['mobile_bonus_points']} {r['score_wo_bonus']} {r['total_multipliers']} {r['qso_points']} {r['ph_qsos']} {r['cw_qsos']} {r['callsign']}\n")   
    # counts: {y}  sets: {x} mobile {r['callsign'] in s.mobile_callsigns}\n")
    # if len(r['errors']) > 0:
    #      s.out_files['debug'].write(f"{r['errors']}\n")
    # s.out_files['debug'].write(f"\n")
    # if p:
    #     pprint(f"{title.upper()} {r['callsign']} hours: {sum(r['qsos_by_hour'])} counts: {y}  sets: {x} hours: {sum(r['qsos_by_hour'])}")
    #     if len(r['errors']) > 0:
    #         print(f"{r['errors']}")

"""
Fuzzy call-sign matcher. We may add this in later but it is not 
being used now 2026-09-22

Finds the callsigns in a set that most closely match a given callsign,
where "closely" means the two strings (ignoring anything after a "/")
share the longest common subsequence (characters in common, in the
same relative order).

Matching rule
--------------
1. Strip everything from the first "/" onward on both sides.
2. Compute the Longest Common Subsequence (LCS) length between the
   two stripped strings.
3. diff_count = max(len(a), len(b)) - LCS(a, b)
   -> this is the number of characters that are "different or missing"
      between the two strings.
4. A candidate qualifies as a close match only if diff_count <= MAX_DIFF
   (default 2, per the problem statement: "no more than two letters
   different or missing").
5. Qualifying candidates are ranked by diff_count ascending (fewer
   differences = higher on the list). Ties are broken alphabetically
   for determinism.
6. Return between MIN_RESULTS and MAX_RESULTS matches (defaults 3-5).
   If fewer than MIN_RESULTS candidates pass the threshold, all that
   passed are returned (there may be fewer than 3).

Comparison is case-insensitive; call signs are conventionally uppercase.
"""

from functools import lru_cache


def strip_slash(callsign: str) -> str:
    """Ignore a trailing slash and anything after it."""
    return callsign.split('/', 1)[0].strip().upper()


def lcs_length(a: str, b: str) -> int:
    """Length of the longest common subsequence of a and b."""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0
    # dp[j] = LCS length of a[:i] and b[:j], rolling row to save memory
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        curr = [0] * (m + 1)
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[m]


def diff_count(a: str, b: str) -> int:
    """Number of characters different or missing between a and b."""
    common = lcs_length(a, b)
    return max(len(a), len(b)) - common


def find_close_matches(target: str,
                        candidates,
                        max_diff: int = 2,
                        min_results: int = 3,
                        max_results: int = 5):
    """
    Find the closest-matching call signs to `target` within `candidates`.

    Parameters
    ----------
    target : str
        The call sign to match against (slash suffix ignored).
    candidates : Iterable[str]
        The set/collection of call signs to search.
    max_diff : int
        Maximum allowed "characters different or missing" (default 2).
    min_results : int
        Soft floor on how many results to try to return (3 by default).
    max_results : int
        Hard cap on how many results to return (5 by default).

    Returns
    -------
    List[str]  (original, un-stripped candidate strings), best match first.
    """
    stripped_target = strip_slash(target)

    scored = []
    for original in candidates:
        stripped_candidate = strip_slash(original)
        if stripped_candidate == stripped_target:
            continue  # skip identical / self matches
        d = diff_count(stripped_target, stripped_candidate)
        if d <= max_diff:
            scored.append((d, original))

    # Fewer differences first; alphabetical as a stable tiebreaker.
    scored.sort(key=lambda pair: (pair[0], pair[1]))

    results = [orig for _, orig in scored[:max_results]]

    if len(results) < min_results:
        # Not enough matches passed the strict threshold; that's fine,
        # we simply return what we have (could be 0-2 items).
        pass

    return results


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
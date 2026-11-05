"""
Fuzzy call-sign matcher.

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


if __name__ == "__main__":
    call_set = {
        "N8PI", "N5EP", "ENP8", "KJ4BYA", "N8EP", "KE7P", "K4BY",
        "NE8P", "N8ZP", "NE8PX/QRP",
    }

    for target in ("NE8P", "KJ5BYZ"):
        print(f"Closest matches to {target}:")
        for cand in find_close_matches(target, call_set):
            a, b = strip_slash(target), strip_slash(cand)
            print(f"  {cand:12s} diff={diff_count(a, b)}")
        print()

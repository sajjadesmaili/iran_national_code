# iran_national_code.py
# ---------------------------------------------------------------------------
#  Normalize and validate Iranian National Identification Numbers (10 digits)
#  Author: Sajjad Esmaili      License: Public Domain
# ---------------------------------------------------------------------------
import re
from typing import Tuple


def validate_iran_national_code(raw_code) -> Tuple[str, bool, str]:
    """
    Normalize and validate a 10-digit Iranian national ID (کد ملّی).

    Parameters
    ----------
    raw_code : str | int
        The code in any form: plain string, integer, or string containing
        spaces / dashes. All non-digit characters will be removed.

    Returns
    -------
    normalized_code : str
        A cleaned 10-digit string (zero-padded on the left if < 10 digits).
        An empty string indicates an invalid input format.
    is_valid : bool
        Final validation result.
    message : str
        Human-readable reason for acceptance or rejection.

    Validation Rules
    ----------------
    1. Exactly 10 digits after cleaning (pad with leading zeros if fewer).
    2. The digits must *not* all be identical (e.g. “1111111111”).
    3. Check-digit algorithm (mod 11):

       total = Σ(dᵢ × (10 − i))  for i = 0 … 8
       remainder = total mod 11

       * if remainder < 2 → check-digit must equal remainder
       * else            → check-digit must equal 11 − remainder
    """
    # 1) keep only digits
    if raw_code is None:
        return "", False, "empty input"

    digits = re.sub(r"\D", "", str(raw_code))
    if not digits:
        return "", False, "no digits found"

    # 2) left-pad with zeros to 10 digits
    if len(digits) < 10:
        digits = digits.zfill(10)
    elif len(digits) > 10:
        return "", False, "more than 10 digits"

    assert len(digits) == 10
    normalized = digits

    # 3) reject codes with all identical digits (000… 999…)
    if len(set(normalized)) == 1:
        return normalized, False, "all digits identical"

    # 4) checksum validation
    check = int(normalized[-1])
    total = sum(int(normalized[i]) * (10 - i) for i in range(9))
    remainder = total % 11

    if (remainder < 2 and check == remainder) or \
       (remainder >= 2 and check == 11 - remainder):
        return normalized, True, "valid national code"
    else:
        return normalized, False, "checksum mismatch"


# ---------------- quick self-test ----------------
if __name__ == "__main__":
    tests = [
        "0371591336",   # valid
        "1111111111",   # invalid: identical digits
        "2222222222",   # invalid
        "090 123 456X", # valid (contains spaces)
        "123",          # padded to 0000000123 → invalid checksum
        "006774982X"    # valid
    ]

    for item in tests:
        code, ok, msg = validate_iran_national_code(item)
        print(f"{item!r:>12}  ->  {code or '¬'}  |  {ok}  |  {msg}")

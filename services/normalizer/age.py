"""
Age Normalization Utility.
Parses numeric age from various string and Bengali representations.
"""

import re
from typing import Optional
from services.normalizer.height import normalize_bengali_digits


def normalize_age(raw_age: Optional[str | int | float]) -> Optional[int]:
    """
    Normalizes raw age into an integer.

    Examples:
        - 27 -> 27
        - "27" -> 27
        - "27 years" -> 27
        - "২৭ বছর" -> 27
        - "Age: 25" -> 25
    """
    if raw_age is None:
        return None

    if isinstance(raw_age, (int, float)):
        val = int(raw_age)
        return val if 18 <= val <= 100 else None

    s = str(raw_age).strip()
    if not s:
        return None

    s = normalize_bengali_digits(s)
    match = re.search(r"\b(\d{2})\b", s)
    if match:
        val = int(match.group(1))
        if 18 <= val <= 100:
            return val

    return None

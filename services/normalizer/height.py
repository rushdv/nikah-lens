"""
Height Normalization Utility.
Converts various height representations (feet/inches, cm, Bengali numerals) to centimeters.
Provides human-readable imperial formatting (e.g. 5'7").
"""

import re
from typing import Optional, Tuple

BENGALI_TO_ENGLISH_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def normalize_bengali_digits(text: str) -> str:
    """Convert Bengali numerical digits to ASCII digits."""
    return text.translate(BENGALI_TO_ENGLISH_DIGITS)


def normalize_height(raw_height: Optional[str | float | int]) -> Optional[float]:
    """
    Normalizes any height string/number into centimeters (float, rounded to 1 decimal place).

    Examples:
        - 5'5" -> 165.1
        - 5'6" -> 167.6
        - 5'7" -> 170.2
        - "5 feet 7 inches" -> 170.2
        - "165 cm" -> 165.0
        - "170.2" -> 170.2
        - "৫ ফুট ৫ ইঞ্চি" -> 165.1
        - "৫'৭\"" -> 170.2
    """
    if raw_height is None:
        return None

    if isinstance(raw_height, (int, float)):
        # If raw number is < 10, likely feet (e.g. 5.58 feet -> cm)
        if raw_height <= 8.5:
            # Assume feet in decimal
            feet = int(raw_height)
            inches = (raw_height - feet) * 12
            return round((feet * 30.48) + (inches * 2.54), 1)
        # Already cm
        return round(float(raw_height), 1)

    s = str(raw_height).strip()
    if not s:
        return None

    s = normalize_bengali_digits(s).lower()

    # Pattern 1: Direct cm match (e.g. "170 cm", "165cm", "170.2 সেমি")
    cm_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:cm|সেমি|সেন্টিমিটার)", s)
    if cm_match:
        return round(float(cm_match.group(1)), 1)

    # Pattern 2: Feet and inches with quotes, dashes, or words:
    # 5'7", 5'7, 5 ft 7 in, 5 feet 7 inches, 5 ফুট 7 ইঞ্চি
    ft_in_match = re.search(
        r"(\d+)\s*(?:'|ft|feet|ফুট|\s*-|\s)\s*(\d+(?:\.\d+)?)\s*(?:\"|''|in|inch|inches|ইঞ্চি)?",
        s
    )
    if ft_in_match:
        feet = int(ft_in_match.group(1))
        inches = float(ft_in_match.group(2))
        total_cm = (feet * 30.48) + (inches * 2.54)
        return round(total_cm, 1)

    # Pattern 3: Feet only (e.g. "5 ft", "5'")
    ft_only_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:'|ft|feet|ফুট)", s)
    if ft_only_match:
        feet = float(ft_only_match.group(1))
        return round(feet * 30.48, 1)

    # Pattern 4: Bare number: if > 100, assume cm; if <= 8, assume feet
    bare_num_match = re.search(r"^(\d+(?:\.\d+)?)$", s)
    if bare_num_match:
        val = float(bare_num_match.group(1))
        if val >= 100:
            return round(val, 1)
        elif val <= 8:
            return round(val * 30.48, 1)

    return None


def format_height_display(cm: Optional[float]) -> Optional[str]:
    """
    Formats centimeters into traditional feet & inches string, e.g. 170.2 -> 5'7" (170 cm).
    """
    if cm is None:
        return None

    total_inches = cm / 2.54
    feet = int(total_inches // 12)
    inches = round(total_inches % 12)
    if inches == 12:
        feet += 1
        inches = 0

    return f"{feet}'{inches}\""

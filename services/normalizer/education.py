"""
Education Normalization Utility.
Normalizes varied degree names and fields of study while preserving raw source text.
"""

import re
from typing import Optional
from packages.schemas.education import EducationInformation


DEGREE_PATTERNS = [
    (r"\b(?:b\.?sc|bachelor of science|bsc)\b", "BSc"),
    (r"\b(?:m\.?sc|master of science|msc)\b", "MSc"),
    (r"\b(?:b\.?a|bachelor of arts|ba)\b", "BA"),
    (r"\b(?:m\.?a|master of arts|ma)\b", "MA"),
    (r"\b(?:b\.?b\.?a|bachelor of business administration|bba)\b", "BBA"),
    (r"\b(?:m\.?b\.?a|master of business administration|mba)\b", "MBA"),
    (r"\b(?:mbbs|m\.?b\.?b\.?s)\b", "MBBS"),
    (r"\b(?:bds|dental surgery)\b", "BDS"),
    (r"\b(?:phd|doctor of philosophy|ph\.?d)\b", "PhD"),
    (r"\b(?:diploma)\b", "Diploma"),
    (r"\b(?:kamil|কামিল)\b", "Kamil"),
    (r"\b(?:fazil|ফাজিল)\b", "Fazil"),
    (r"\b(?:alim|আলিম)\b", "Alim"),
    (r"\b(?:dakhil|দাখিল)\b", "Dakhil"),
    (r"\b(?:hsc|higher secondary)\b", "HSC"),
    (r"\b(?:ssc|secondary school)\b", "SSC"),
    (r"\b(?:hafiz|হিফজ|হাফেজ)\b", "Hafiz"),
]

FIELD_PATTERNS = [
    (r"\b(?:cse|computer science(?: & engineering)?|software engineering)\b", "Computer Science & Engineering"),
    (r"\b(?:eee|electrical(?: & electronic)? engineering)\b", "Electrical & Electronic Engineering"),
    (r"\b(?:civil engineering|ce)\b", "Civil Engineering"),
    (r"\b(?:mechanical engineering|me)\b", "Mechanical Engineering"),
    (r"\b(?:medicine|medical|surgery)\b", "Medicine"),
    (r"\b(?:islamic studies|islamic theology|hadith|tafsir|quran|দাওয়া)\b", "Islamic Studies"),
    (r"\b(?:business administration|accounting|finance|marketing|management)\b", "Business & Commerce"),
    (r"\b(?:english|english literature)\b", "English"),
    (r"\b(?:bengali|bangla)\b", "Bengali"),
    (r"\b(?:law|llb|llm)\b", "Law"),
    (r"\b(?:economics)\b", "Economics"),
    (r"\b(?:mathematics|math)\b", "Mathematics"),
    (r"\b(?:physics)\b", "Physics"),
]


def normalize_education(raw_text: Optional[str]) -> EducationInformation:
    """
    Parses raw education text into normalized degree and field while preserving raw text.

    Examples:
        - "B.Sc. in Computer Science & Engineering" -> degree="BSc", field="Computer Science & Engineering"
        - "CSE" -> degree="BSc", field="Computer Science & Engineering"
        - "Alim from Madrasa" -> degree="Alim", field="Islamic Studies"
    """
    if not raw_text:
        return EducationInformation()

    cleaned = raw_text.strip()
    lowered = cleaned.lower()

    detected_degree = None
    for pattern, deg in DEGREE_PATTERNS:
        if re.search(pattern, lowered, re.IGNORECASE):
            detected_degree = deg
            break

    detected_field = None
    for pattern, fld in FIELD_PATTERNS:
        if re.search(pattern, lowered, re.IGNORECASE):
            detected_field = fld
            break

    # If CSE was specified without degree explicitly named, assume BSc
    if not detected_degree and detected_field == "Computer Science & Engineering":
        detected_degree = "BSc"

    # For traditional madrasa degrees, field is Islamic Studies
    if detected_degree in ["Alim", "Fazil", "Kamil", "Hafiz"] and not detected_field:
        detected_field = "Islamic Studies"

    return EducationInformation(
        degree=detected_degree,
        field=detected_field,
        raw_text=cleaned
    )

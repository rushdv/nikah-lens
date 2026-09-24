"""
Deen Information Extraction and Normalization.
Extracts factual religious practice statements from matrimonial profile descriptions.
Maintains evidence snippets and never generates subjective judgments (e.g. 'pious', 'good').
"""

import re
from typing import Optional, Dict, Any
from packages.schemas.deen import DeenProfile, DeenAttribute, StatedStatus, EvidenceType


def extract_deen_profile(raw_text: Optional[str], raw_data: Optional[Dict[str, Any]] = None) -> DeenProfile:
    """
    Analyzes raw profile text or key-value fields and maps to structured DeenProfile.
    """
    raw_data = raw_data or {}
    text = (raw_text or "") + " " + " ".join(str(v) for v in raw_data.values() if isinstance(v, str))
    lowered = text.lower()

    # 1. Salah
    salah_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:5\s*times|five\s*times|পাঁচ\s*ওয়াক্ত|নিয়মিত\s*নামাজ|regular\s*salah|regular\s*prayer|নামাজি)\b", lowered):
        salah_attr = DeenAttribute(
            value="regular_5_times",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Profile states regular 5 daily prayers"
        )
    elif re.search(r"\b(?:salah|namaz|নামাজ|prayer)\b", lowered):
        salah_attr = DeenAttribute(
            value="prays_salah",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Salah is mentioned in profile"
        )

    # 2. Quran
    quran_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:hafiz|hafez|হিফজ|হাফেজ|memorized\s*quran)\b", lowered):
        quran_attr = DeenAttribute(
            value="hafiz_of_quran",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Profile states memorization of the Holy Quran"
        )
    elif re.search(r"\b(?:quran|telawat|তেলাওয়াত|recites\s*quran|regular\s*quran)\b", lowered):
        quran_attr = DeenAttribute(
            value="regular_recitation",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Regular Quran recitation mentioned"
        )

    # 3. Beard
    beard_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:sunnah\s*beard|সুন্নত\s*দাড়ি|full\s*beard|দাড়ি\s*আছে|has\s*beard)\b", lowered):
        beard_attr = DeenAttribute(
            value="sunnah_beard_stated",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Profile explicitly states maintaining a beard"
        )
    elif re.search(r"\b(?:clean\s*shaven|দাড়ি\s*নেই)\b", lowered):
        beard_attr = DeenAttribute(
            value="clean_shaven_stated",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Profile states clean shaven"
        )

    # 4. Islamic Studies / Dawah
    studies_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:alim|fazil|kamil|dakhil|madrasa|qawmi|দাওয়া|islamic\s*studies)\b", lowered):
        studies_attr = DeenAttribute(
            value="formal_or_structured_studies",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Formal Islamic studies or madrasa background mentioned"
        )

    # 5. Halal Income
    income_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:halal\s*income|হালাল\s*উপার্জন|halal\s*earning|conscious\s*of\s*halal)\b", lowered):
        income_attr = DeenAttribute(
            value="halal_income_emphasized",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Halal income is explicitly prioritized in profile text"
        )

    # 6. Religious Environment
    env_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:practicing\s*family|deen\s*oriented\s*family|দ্বীনি\s*পরিবেশ|religious\s*family)\b", lowered):
        env_attr = DeenAttribute(
            value="practicing_family_environment",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Deen-oriented family environment stated"
        )

    # 7. Islamic Practice (General sunnah observance)
    practice_attr = DeenAttribute(status=StatedStatus.NOT_STATED, evidence_type=EvidenceType.SELF_REPORTED)
    if re.search(r"\b(?:sunnah|islamic\s*lifestyle|shar'iah|শরীয়ত|পর্দা|purdah)\b", lowered):
        practice_attr = DeenAttribute(
            value="sunnah_practice_mentioned",
            status=StatedStatus.STATED,
            evidence_type=EvidenceType.SELF_REPORTED,
            raw_text="Adherence to Sunnah / Shari'ah guidelines mentioned"
        )

    # 8. Self description
    self_desc = DeenAttribute(
        value=raw_text[:200] if raw_text else None,
        status=StatedStatus.STATED if raw_text else StatedStatus.NOT_STATED,
        evidence_type=EvidenceType.SELF_REPORTED,
        raw_text=raw_text[:300] if raw_text else None
    )

    return DeenProfile(
        salah=salah_attr,
        quran=quran_attr,
        beard=beard_attr,
        islamic_studies=studies_attr,
        halal_income=income_attr,
        religious_environment=env_attr,
        islamic_practice=practice_attr,
        self_description=self_desc
    )

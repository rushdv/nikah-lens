"""
Profession and Career Normalization Utility.
Normalizes occupation titles and industries without making unverified assumptions
about financial stability or salary.
"""

import re
from typing import Optional
from packages.schemas.career import CareerInformation, CareerStatus


PROFESSION_CATEGORIES = [
    # Software & Technology
    (
        r"\b(?:software\s*engineer|software\s*dev|developer|s/w\s*engineer|web\s*developer|programmer|full\s*stack|backend|frontend|data\s*engineer|devops)\b",
        "Software Engineer",
        "Software & Technology",
        CareerStatus.EMPLOYED
    ),
    # Education & Academia
    (
        r"\b(?:teacher|lecturer|professor|instructor|madrasa\s*teacher|assistant\s*professor)\b",
        "Teacher / Academic",
        "Education & Academia",
        CareerStatus.EMPLOYED
    ),
    # Healthcare & Medicine
    (
        r"\b(?:doctor|physician|surgeon|medical\s*officer|pharmacist|dentist)\b",
        "Doctor / Healthcare Professional",
        "Healthcare & Medicine",
        CareerStatus.PROFESSIONAL
    ),
    # Business & Commerce
    (
        r"\b(?:business|businessman|business\s*owner|entrepreneur|trader|merchant|shop\s*owner|proprietor|export\s*import)\b",
        "Business Owner / Entrepreneur",
        "Business & Commerce",
        CareerStatus.BUSINESS_OWNER
    ),
    # Freelance & Digital
    (
        r"\b(?:freelancer|freelance|graphic\s*designer|ui/ux|content\s*creator)\b",
        "Freelancer / Digital Creator",
        "Freelance & Creative",
        CareerStatus.FREELANCER
    ),
    # Finance & Banking
    (
        r"\b(?:banker|bank\s*officer|accountant|financial\s*analyst|audit)\b",
        "Banking & Finance Professional",
        "Banking & Finance",
        CareerStatus.EMPLOYED
    ),
    # Government & Public Service
    (
        r"\b(?:bcs|govt\s*officer|government\s*service|civil\s*service|public\s*servant)\b",
        "Government Service / Officer",
        "Public Service",
        CareerStatus.EMPLOYED
    ),
    # Engineering
    (
        r"\b(?:civil\s*engineer|electrical\s*engineer|mechanical\s*engineer|site\s*engineer)\b",
        "Engineer",
        "Engineering",
        CareerStatus.EMPLOYED
    ),
    # Islamic Scholar / Imam
    (
        r"\b(?:imam|khatib|mufti|islamic\s*scholar|madrasa\s*principal)\b",
        "Islamic Scholar / Imam",
        "Religious & Islamic Affairs",
        CareerStatus.EMPLOYED
    ),
    # Student
    (
        r"\b(?:student|studying|undergraduate|postgraduate|candidate)\b",
        "Student",
        "Academics / Student",
        CareerStatus.STUDENT
    ),
    # Job Seeker / Unemployed
    (
        r"\b(?:job\s*seeker|seeking\s*job|unemployed|looking\s*for\s*job)\b",
        "Job Seeker",
        "Unspecified",
        CareerStatus.JOB_SEEKER
    ),
]


def normalize_profession(raw_text: Optional[str]) -> CareerInformation:
    """
    Normalizes raw profession title into structured CareerInformation.
    Always maintains original raw title and flags occupation_stated.
    Never asserts financial stability.

    Examples:
        - "S/W Engineer at Tech Corp" -> occupation="Software Engineer", role_category="Software & Technology", employment_status=EMPLOYED
        - "Businessman (Textile Trading)" -> occupation="Business Owner / Entrepreneur", role_category="Business & Commerce", employment_status=BUSINESS_OWNER
        - None / "" -> unspecified
    """
    if not raw_text or not raw_text.strip():
        return CareerInformation(
            occupation=None,
            role_category=None,
            industry=None,
            employment_status=CareerStatus.UNSPECIFIED,
            raw_title=None,
            occupation_stated=False,
            career_stability_stated=False,
            income_stated=False,
            financial_stability_verified=False
        )

    cleaned = raw_text.strip()
    lowered = cleaned.lower()

    detected_role = None
    detected_category = None
    detected_status = CareerStatus.EMPLOYED

    for pattern, role, cat, status in PROFESSION_CATEGORIES:
        if re.search(pattern, lowered, re.IGNORECASE):
            detected_role = role
            detected_category = cat
            detected_status = status
            break

    if not detected_role:
        detected_role = cleaned.title()
        detected_category = "General Employment"
        detected_status = CareerStatus.EMPLOYED

    # Check if candidate explicitly mentioned stability or income in the raw text
    stability_stated = bool(re.search(r"\b(?:permanent|stable|established|সরকারি|স্থায়ী)\b", lowered))
    income_stated = bool(re.search(r"\b(?:salary|income|tk|bdt|মাসিক|বেতন|লাখ)\b", lowered))

    return CareerInformation(
        occupation=detected_role,
        role_category=detected_category,
        industry=detected_category,
        employment_status=detected_status,
        raw_title=cleaned,
        occupation_stated=True,
        career_stability_stated=stability_stated,
        income_stated=income_stated,
        financial_stability_verified=False  # Strictly False unless independently verified
    )

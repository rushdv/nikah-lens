"""
Location Normalization Utility.
Maps English and Bengali place names to canonical Bangladesh districts and divisions.
Special focus on Rangpur Division and surrounding northern districts.
"""

from typing import Optional, Dict, Tuple, List

# Canonical district to division mapping
DISTRICT_TO_DIVISION = {
    # Rangpur Division
    "Rangpur": "Rangpur Division",
    "Dinajpur": "Rangpur Division",
    "Kurigram": "Rangpur Division",
    "Lalmonirhat": "Rangpur Division",
    "Nilphamari": "Rangpur Division",
    "Gaibandha": "Rangpur Division",
    "Thakurgaon": "Rangpur Division",
    "Panchagarh": "Rangpur Division",

    # Rajshahi Division
    "Rajshahi": "Rajshahi Division",
    "Bogura": "Rajshahi Division",
    "Pabna": "Rajshahi Division",
    "Sirajganj": "Rajshahi Division",
    "Naogaon": "Rajshahi Division",
    "Natore": "Rajshahi Division",
    "Chapai Nawabganj": "Rajshahi Division",
    "Joypurhat": "Rajshahi Division",

    # Dhaka Division
    "Dhaka": "Dhaka Division",
    "Gazipur": "Dhaka Division",
    "Narayanganj": "Dhaka Division",
    "Tangail": "Dhaka Division",
    "Faridpur": "Dhaka Division",
    "Manikganj": "Dhaka Division",
    "Munshiganj": "Dhaka Division",
    "Narsingdi": "Dhaka Division",
    "Kishoreganj": "Dhaka Division",
    "Gopalganj": "Dhaka Division",

    # Chattogram Division
    "Chattogram": "Chattogram Division",
    "Cox's Bazar": "Chattogram Division",
    "Cumilla": "Chattogram Division",
    "Feni": "Chattogram Division",
    "Noakhali": "Chattogram Division",
    "Brahmanbaria": "Chattogram Division",
    "Chandpur": "Chattogram Division",

    # Sylhet Division
    "Sylhet": "Sylhet Division",
    "Moulvibazar": "Sylhet Division",
    "Habiganj": "Sylhet Division",
    "Sunamganj": "Sylhet Division",

    # Khulna Division
    "Khulna": "Khulna Division",
    "Jashore": "Khulna Division",
    "Kushtia": "Khulna Division",
    "Satkhira": "Khulna Division",

    # Barishal Division
    "Barishal": "Barishal Division",
    "Bhola": "Barishal Division",
    "Patuakhali": "Barishal Division",

    # Mymensingh Division
    "Mymensingh": "Mymensingh Division",
    "Jamalpur": "Mymensingh Division",
    "Netrokona": "Mymensingh Division",
    "Sherpur": "Mymensingh Division",
}

# Aliases and spelling variations (case-insensitive)
LOCATION_ALIASES: Dict[str, str] = {
    # Rangpur Division
    "rangpur": "Rangpur",
    "রংপুর": "Rangpur",
    "rangpur district": "Rangpur",
    "rangpur sadar": "Rangpur",

    "dinajpur": "Dinajpur",
    "দিনাজপুর": "Dinajpur",
    "dinajpur district": "Dinajpur",

    "kurigram": "Kurigram",
    "কুড়িগ্রাম": "Kurigram",
    "kurigram district": "Kurigram",

    "lalmonirhat": "Lalmonirhat",
    "লালমনিরহাট": "Lalmonirhat",

    "nilphamari": "Nilphamari",
    "নীলফামারী": "Nilphamari",
    "saidpur": "Nilphamari",
    "সৈয়দপুর": "Nilphamari",

    "gaibandha": "Gaibandha",
    "গাইবান্ধা": "Gaibandha",

    "thakurgaon": "Thakurgaon",
    "ঠাকুরগাঁও": "Thakurgaon",

    "panchagarh": "Panchagarh",
    "পঞ্চগড়": "Panchagarh",

    # Dhaka
    "dhaka": "Dhaka",
    "ঢাকা": "Dhaka",
    "dhaka city": "Dhaka",
    "dhaka district": "Dhaka",
    "dhaka north": "Dhaka",
    "dhaka south": "Dhaka",
    "mirpur": "Dhaka",
    "uttara": "Dhaka",
    "dhanmondi": "Dhaka",
    "gulshan": "Dhaka",

    # Chattogram
    "chattogram": "Chattogram",
    "chittagong": "Chattogram",
    "চট্টগ্রাম": "Chattogram",
    "cumilla": "Cumilla",
    "comilla": "Cumilla",
    "কুমিল্লা": "Cumilla",

    # Sylhet
    "sylhet": "Sylhet",
    "সিলেট": "Sylhet",

    # Rajshahi & Bogura
    "rajshahi": "Rajshahi",
    "রাজশাহী": "Rajshahi",
    "bogura": "Bogura",
    "bogra": "Bogura",
    "বগুড়া": "Bogura",

    # Khulna & Jashore
    "khulna": "Khulna",
    "খুলনা": "Khulna",
    "jashore": "Jashore",
    "jessore": "Jashore",
    "যশোর": "Jashore",

    # Barishal
    "barishal": "Barishal",
    "barisal": "Barishal",
    "বরিশাল": "Barishal",

    # Mymensingh
    "mymensingh": "Mymensingh",
    "ময়মনসিংহ": "Mymensingh",
}

RANGPUR_DIVISION_DISTRICTS = [
    "Rangpur", "Dinajpur", "Kurigram", "Lalmonirhat",
    "Nilphamari", "Gaibandha", "Thakurgaon", "Panchagarh"
]


def normalize_location(raw_location: Optional[str]) -> Optional[str]:
    """
    Normalizes raw location string into a canonical district name.

    Examples:
        - "Rangpur" -> "Rangpur"
        - "রংপুর" -> "Rangpur"
        - "RANGPUR" -> "Rangpur"
        - "Rangpur District" -> "Rangpur"
        - "Dhaka" -> "Dhaka"
        - "ঢাকা" -> "Dhaka"
    """
    if not raw_location:
        return None

    cleaned = str(raw_location).strip().lower()
    # Remove common punctuation or noise
    cleaned = cleaned.replace(",", " ").replace("-", " ")
    words = cleaned.split()

    # Direct match on full string
    if cleaned in LOCATION_ALIASES:
        return LOCATION_ALIASES[cleaned]

    # Check words for matching known aliases
    for word in words:
        if word in LOCATION_ALIASES:
            return LOCATION_ALIASES[word]

    # Partial substring check
    for alias, canonical in LOCATION_ALIASES.items():
        if alias in cleaned:
            return canonical

    # If no mapping matched, return title-cased clean string
    return raw_location.strip().title()


def get_location_division(canonical_district: Optional[str]) -> Optional[str]:
    if not canonical_district:
        return None
    return DISTRICT_TO_DIVISION.get(canonical_district)


def is_rangpur_division(canonical_district: Optional[str]) -> bool:
    return canonical_district in RANGPUR_DIVISION_DISTRICTS

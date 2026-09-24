"""
Tests for normalizers: height, age, location, education, profession, deen.
"""

import pytest
from services.normalizer.height import normalize_height, format_height_display
from services.normalizer.age import normalize_age
from services.normalizer.location import normalize_location, is_rangpur_division
from services.normalizer.education import normalize_education
from services.normalizer.profession import normalize_profession
from services.normalizer.deen import extract_deen_profile
from packages.schemas.deen import StatedStatus


def test_height_normalization_feet_inches():
    assert normalize_height("5'5\"") == 165.1
    assert normalize_height("5'6\"") == 167.6
    assert normalize_height("5'7\"") == 170.2
    assert normalize_height("5 feet 7 inches") == 170.2
    assert normalize_height("5 ft 5 in") == 165.1


def test_height_normalization_centimeters():
    assert normalize_height("165 cm") == 165.0
    assert normalize_height("165cm") == 165.0
    assert normalize_height("170.2") == 170.2
    assert normalize_height(170.2) == 170.2


def test_height_normalization_bengali():
    assert normalize_height("৫ ফুট ৫ ইঞ্চি") == 165.1
    assert normalize_height("৫'৭\"") == 170.2
    assert normalize_height("১৬৫ সেমি") == 165.0


def test_format_height_display():
    assert format_height_display(165.1) == "5'5\""
    assert format_height_display(170.2) == "5'7\""
    assert format_height_display(None) is None


def test_age_normalization():
    assert normalize_age(27) == 27
    assert normalize_age("27") == 27
    assert normalize_age("27 years") == 27
    assert normalize_age("২৭ বছর") == 27
    assert normalize_age("Age: 25") == 25
    assert normalize_age("invalid") is None


def test_location_normalization_english_and_bengali():
    # Rangpur
    assert normalize_location("Rangpur") == "Rangpur"
    assert normalize_location("rangpur") == "Rangpur"
    assert normalize_location("RANGPUR") == "Rangpur"
    assert normalize_location("Rangpur District") == "Rangpur"
    assert normalize_location("Rangpur Sadar") == "Rangpur"
    assert normalize_location("রংপুর") == "Rangpur"

    # Dinajpur
    assert normalize_location("Dinajpur") == "Dinajpur"
    assert normalize_location("দিনাজপুর") == "Dinajpur"

    # Kurigram
    assert normalize_location("Kurigram") == "Kurigram"
    assert normalize_location("কুড়িগ্রাম") == "Kurigram"

    # Dhaka
    assert normalize_location("Dhaka") == "Dhaka"
    assert normalize_location("ঢাকা") == "Dhaka"
    assert normalize_location("Dhaka City") == "Dhaka"


def test_is_rangpur_division():
    assert is_rangpur_division("Rangpur") is True
    assert is_rangpur_division("Dinajpur") is True
    assert is_rangpur_division("Kurigram") is True
    assert is_rangpur_division("Panchagarh") is True
    assert is_rangpur_division("Dhaka") is False
    assert is_rangpur_division("Sylhet") is False


def test_education_normalization():
    res1 = normalize_education("B.Sc. in Computer Science & Engineering")
    assert res1.degree == "BSc"
    assert res1.field == "Computer Science & Engineering"

    res2 = normalize_education("CSE")
    assert res2.degree == "BSc"
    assert res2.field == "Computer Science & Engineering"

    res3 = normalize_education("Alim from Madrasa")
    assert res3.degree == "Alim"
    assert res3.field == "Islamic Studies"


def test_profession_normalization_and_no_inferred_wealth():
    res1 = normalize_profession("Software Engineer at Tech Corp")
    assert res1.occupation == "Software Engineer"
    assert res1.role_category == "Software & Technology"
    assert res1.occupation_stated is True
    # Financial stability must NEVER be inferred
    assert res1.financial_stability_verified is False

    res2 = normalize_profession("Businessman (Textile Trading)")
    assert res2.occupation == "Business Owner / Entrepreneur"
    assert res2.employment_status.value == "business_owner"
    assert res2.financial_stability_verified is False


def test_deen_extraction_factual_and_non_judgmental():
    text = "Performs regular 5 times prayer in masjid. Maintains sunnah beard. Conscious of halal income."
    res = extract_deen_profile(text)

    assert res.salah.status == StatedStatus.STATED
    assert res.salah.value == "regular_5_times"
    assert res.beard.status == StatedStatus.STATED
    assert res.beard.value == "sunnah_beard_stated"
    assert res.halal_income.status == StatedStatus.STATED

    # Verify no unstated claims
    assert res.islamic_studies.status == StatedStatus.NOT_STATED

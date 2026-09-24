"""
Tests for deterministic MatchEngine.
Verifies hard filtering, preferred preferences, unknown handling, and why explanations.
"""

from datetime import datetime, timezone
from packages.schemas.profile import ProfileResponse
from packages.schemas.deen import DeenProfile, DeenAttribute, StatedStatus, EvidenceType
from packages.schemas.career import CareerInformation, CareerStatus
from packages.schemas.education import EducationInformation
from packages.schemas.search import (
    SearchCriteria, AgeCriteria, HeightCriteria, LocationItem,
    MaritalStatusCriteria, DeenCriteria, CareerCriteria, RequirementPriority, MatchStatus
)
from services.matcher.engine import MatchEngine


def make_profile(
    pid="test-1", age=27, height_cm=170.2, location="Rangpur",
    marital="never_married", occupation="Software Engineer",
    salah="regular_5_times", beard="sunnah_beard_stated"
):
    now = datetime.now(timezone.utc)
    return ProfileResponse(
        id=pid,
        source="mock",
        source_profile_id=pid,
        candidate_code=f"Candidate #{pid}",
        gender="male",
        age=age,
        height_cm=height_cm,
        height_display="5'7\"",
        marital_status=marital,
        current_location=location,
        permanent_location=location,
        education=EducationInformation(degree="BSc", field="Computer Science"),
        career=CareerInformation(
            occupation=occupation,
            role_category="Software & Technology",
            employment_status=CareerStatus.EMPLOYED if occupation else CareerStatus.UNSPECIFIED,
            occupation_stated=bool(occupation)
        ),
        deen=DeenProfile(
            salah=DeenAttribute(
                value=salah,
                status=StatedStatus.STATED if salah else StatedStatus.NOT_STATED,
                evidence_type=EvidenceType.SELF_REPORTED
            ),
            beard=DeenAttribute(
                value=beard,
                status=StatedStatus.STATED if beard else StatedStatus.NOT_STATED,
                evidence_type=EvidenceType.SELF_REPORTED
            )
        ),
        synthetic=True,
        first_seen=now,
        last_seen=now
    )


def test_strong_match_evaluation():
    profile = make_profile()
    criteria = SearchCriteria(
        gender="male",
        age=AgeCriteria(min=22, max=29, priority=RequirementPriority.REQUIRED),
        height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.REQUIRED),
        locations=[LocationItem(name="Rangpur", priority=RequirementPriority.PREFERRED)],
        marital_status=MaritalStatusCriteria(values=["never_married"], priority=RequirementPriority.REQUIRED),
        deen=DeenCriteria(require_salah=True, prefer_beard=True),
        career=CareerCriteria(require_occupation_stated=True)
    )

    result = MatchEngine.evaluate(profile, criteria)
    assert result.match_status == MatchStatus.STRONG_MATCH
    assert len(result.hard_failures) == 0
    assert any("Age" in r for r in result.why_matched)
    assert any("Height" in r for r in result.why_matched)
    assert any("Location" in r for r in result.why_matched)
    assert any("Salah" in r for r in result.why_matched)


def test_hard_requirement_age_failure():
    profile = make_profile(age=35)
    criteria = SearchCriteria(
        age=AgeCriteria(min=22, max=29, priority=RequirementPriority.REQUIRED)
    )
    result = MatchEngine.evaluate(profile, criteria)
    assert result.match_status == MatchStatus.HARD_REQUIREMENT_NOT_MET
    assert any("outside preferred range" in f for f in result.hard_failures)


def test_hard_requirement_height_failure():
    profile = make_profile(height_cm=160.0)  # ~5'3"
    criteria = SearchCriteria(
        height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.REQUIRED)
    )
    result = MatchEngine.evaluate(profile, criteria)
    assert result.match_status == MatchStatus.HARD_REQUIREMENT_NOT_MET
    assert any("below minimum requirement" in f for f in result.hard_failures)


def test_unknown_does_not_fail_by_default():
    # If height is missing, unknown != fail (unless missing_data_disqualifies is set)
    profile = make_profile(height_cm=None)
    criteria = SearchCriteria(
        height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.REQUIRED),
        missing_data_disqualifies=False
    )
    result = MatchEngine.evaluate(profile, criteria)
    # Should NOT be hard failure; should appear under needs_review
    assert len(result.hard_failures) == 0
    assert any("Height is not stated in profile" in r for r in result.needs_review)


def test_missing_data_disqualifies_flag():
    profile = make_profile(height_cm=None)
    criteria = SearchCriteria(
        height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.REQUIRED),
        missing_data_disqualifies=True
    )
    result = MatchEngine.evaluate(profile, criteria)
    assert result.match_status == MatchStatus.HARD_REQUIREMENT_NOT_MET
    assert any("Height is not stated" in f for f in result.hard_failures)

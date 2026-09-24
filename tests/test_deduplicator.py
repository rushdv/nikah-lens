"""
Tests for DuplicateDetector.
Verifies multi-attribute comparison, duplicate candidate scoring, and reasons.
"""

from services.deduplicator.detector import DuplicateDetector
from tests.test_matcher import make_profile


def test_identical_attributes_high_confidence():
    p1 = make_profile(pid="p1", age=27, height_cm=170.2, location="Rangpur", occupation="Software Engineer")
    p2 = make_profile(pid="p2", age=27, height_cm=170.2, location="Rangpur", occupation="Software Engineer")

    summary = DuplicateDetector.compare_pair(p1, p2)
    assert summary.is_duplicate is True
    assert summary.confidence == "High"
    assert any("Identical age" in r for r in summary.reasons)
    assert any("Matching height" in r for r in summary.reasons)
    assert any("Same district" in r for r in summary.reasons)
    assert any("Identical occupation" in r for r in summary.reasons)


def test_different_people_not_duplicate():
    p1 = make_profile(pid="p1", age=24, height_cm=165.1, location="Rangpur", occupation="Teacher")
    p2 = make_profile(pid="p2", age=32, height_cm=178.0, location="Dhaka", occupation="Doctor")

    summary = DuplicateDetector.compare_pair(p1, p2)
    assert summary.is_duplicate is False

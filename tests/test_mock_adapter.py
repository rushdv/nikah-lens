"""
Tests for MockSourceAdapter.
Verifies synthetic dataset count (at least 30), Rangpur focus, and schema adherence.
"""

from services.collectors.mock.adapter import MockSourceAdapter


def test_mock_adapter_profile_count():
    adapter = MockSourceAdapter()
    profiles = adapter.get_all_profiles()
    # Must have at least 30 synthetic profiles per Section 24
    assert len(profiles) >= 30


def test_mock_adapter_synthetic_flag():
    adapter = MockSourceAdapter()
    profiles = adapter.get_all_profiles()
    for p in profiles:
        assert p.synthetic is True
        assert p.source == "mock"
        assert p.gender in ["male", "female"]
        assert p.education is not None
        assert p.career is not None
        assert p.deen is not None


def test_mock_adapter_rangpur_profiles_present():
    adapter = MockSourceAdapter()
    profiles = adapter.get_all_profiles()
    rangpur_profiles = [p for p in profiles if p.current_location == "Rangpur" or p.permanent_location == "Rangpur"]
    assert len(rangpur_profiles) >= 5

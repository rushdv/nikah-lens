"""
Database Seeding Script.
Populates initial synthetic profiles, saved search profiles, source adapters, and sample shortlist.
Strictly generates synthetic fictitious profiles.
"""

from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session

from database.session import SessionLocal, init_db
from database.models import (
    ProfileModel, ProfileVersionModel, SearchProfileModel,
    ShortlistModel, NoteModel, SourceModel
)
from services.collectors.mock.adapter import MockSourceAdapter, MOCK_RAW_PROFILES
from services.collectors import registry
from packages.schemas.search import (
    SearchCriteria, AgeCriteria, HeightCriteria, LocationItem,
    MaritalStatusCriteria, DeenCriteria, CareerCriteria, RequirementPriority
)


def seed_sources(db: Session):
    """Register source adapters."""
    for adapter in registry.list_adapters():
        existing = db.query(SourceModel).filter(SourceModel.name == adapter.name).first()
        if not existing:
            source_entry = SourceModel(
                name=adapter.name,
                display_name=adapter.display_name,
                enabled=adapter.is_enabled,
                mode=adapter.mode,
                terms_compliance_notes=adapter.terms_compliance_notes,
                permits_automated_collection=adapter.permits_automated_collection,
                last_synced_at=datetime.now(timezone.utc) if adapter.name == "mock" else None
            )
            db.add(source_entry)
        else:
            existing.display_name = adapter.display_name
            existing.mode = adapter.mode
            existing.terms_compliance_notes = adapter.terms_compliance_notes
            existing.permits_automated_collection = adapter.permits_automated_collection
    db.commit()


def seed_search_profiles(db: Session):
    """Seed initial search profiles."""
    default_searches = [
        {
            "name": "Primary Search",
            "description": "Initial personal search profile: Male, 22-29, 5'5\"+ min, Rangpur & nearby, Never married, High Deen priority.",
            "is_active": True,
            "criteria": SearchCriteria(
                gender="male",
                age=AgeCriteria(min=22, max=29, priority=RequirementPriority.REQUIRED),
                height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.REQUIRED),
                locations=[
                    LocationItem(name="Rangpur", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Dinajpur", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Kurigram", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Lalmonirhat", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Nilphamari", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Gaibandha", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Thakurgaon", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Panchagarh", priority=RequirementPriority.PREFERRED),
                ],
                marital_status=MaritalStatusCriteria(values=["never_married"], priority=RequirementPriority.REQUIRED),
                deen=DeenCriteria(priority="very_high", require_salah=True, prefer_beard=True),
                career=CareerCriteria(priority="high", require_occupation_stated=True)
            ).model_dump()
        },
        {
            "name": "Rangpur Only",
            "description": "Restricted strictly to Rangpur district.",
            "is_active": False,
            "criteria": SearchCriteria(
                gender="male",
                age=AgeCriteria(min=22, max=29, priority=RequirementPriority.REQUIRED),
                height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.REQUIRED),
                locations=[
                    LocationItem(name="Rangpur", priority=RequirementPriority.REQUIRED),
                ],
                marital_status=MaritalStatusCriteria(values=["never_married"], priority=RequirementPriority.REQUIRED),
                deen=DeenCriteria(priority="very_high", require_salah=True),
                career=CareerCriteria(priority="high", require_occupation_stated=True)
            ).model_dump()
        },
        {
            "name": "Northern Bangladesh",
            "description": "Broad search across all 8 districts of Rangpur Division plus Bogura.",
            "is_active": False,
            "criteria": SearchCriteria(
                gender="male",
                age=AgeCriteria(min=22, max=30, priority=RequirementPriority.REQUIRED),
                height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.PREFERRED),
                locations=[
                    LocationItem(name="Rangpur", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Dinajpur", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Kurigram", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Lalmonirhat", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Nilphamari", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Gaibandha", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Thakurgaon", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Panchagarh", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Bogura", priority=RequirementPriority.PREFERRED),
                ],
                marital_status=MaritalStatusCriteria(values=["never_married"], priority=RequirementPriority.REQUIRED),
                deen=DeenCriteria(priority="very_high", require_salah=True),
                career=CareerCriteria(priority="high", require_occupation_stated=True)
            ).model_dump()
        },
        {
            "name": "Flexible Age & Height",
            "description": "Broader age bracket (20-33) with relaxed height requirements.",
            "is_active": False,
            "criteria": SearchCriteria(
                gender="male",
                age=AgeCriteria(min=20, max=33, priority=RequirementPriority.PREFERRED),
                height=HeightCriteria(min_cm=160.0, priority=RequirementPriority.PREFERRED),
                locations=[
                    LocationItem(name="Rangpur", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Dhaka", priority=RequirementPriority.PREFERRED),
                ],
                marital_status=MaritalStatusCriteria(values=["never_married"], priority=RequirementPriority.REQUIRED),
                deen=DeenCriteria(priority="high", require_salah=True),
                career=CareerCriteria(priority="flexible", require_occupation_stated=False)
            ).model_dump()
        },
        {
            "name": "Strict Deen & Quran",
            "description": "Requires regular Salah, Quran recitation/memorization, and Sunnah beard.",
            "is_active": False,
            "criteria": SearchCriteria(
                gender="male",
                age=AgeCriteria(min=22, max=30, priority=RequirementPriority.REQUIRED),
                height=HeightCriteria(min_cm=165.1, priority=RequirementPriority.PREFERRED),
                locations=[
                    LocationItem(name="Rangpur", priority=RequirementPriority.PREFERRED),
                    LocationItem(name="Dinajpur", priority=RequirementPriority.PREFERRED),
                ],
                marital_status=MaritalStatusCriteria(values=["never_married"], priority=RequirementPriority.REQUIRED),
                deen=DeenCriteria(priority="very_high", require_salah=True, require_quran=True, prefer_beard=True),
                career=CareerCriteria(priority="high", require_occupation_stated=True)
            ).model_dump()
        }
    ]

    for p in default_searches:
        existing = db.query(SearchProfileModel).filter(SearchProfileModel.name == p["name"]).first()
        if not existing:
            search_profile = SearchProfileModel(
                name=p["name"],
                description=p["description"],
                is_active=p["is_active"],
                criteria=p["criteria"]
            )
            db.add(search_profile)
    db.commit()


def seed_synthetic_profiles(db: Session):
    """Seed synthetic profiles from mock adapter."""
    adapter = MockSourceAdapter()
    profiles = adapter.get_all_profiles()

    for p in profiles:
        existing = db.query(ProfileModel).filter(ProfileModel.id == p.id).first()
        if not existing:
            model = ProfileModel(
                id=p.id,
                source=p.source,
                source_profile_id=p.source_profile_id,
                candidate_code=p.candidate_code,
                profile_url=p.profile_url,
                gender=p.gender,
                age=p.age,
                height_cm=p.height_cm,
                height_display=p.height_display,
                marital_status=p.marital_status,
                current_location=p.current_location,
                permanent_location=p.permanent_location,
                education=p.education.model_dump(),
                career=p.career.model_dump(),
                deen=p.deen.model_dump(),
                synthetic=True,
                raw_data=p.raw_data,
                first_seen=p.first_seen,
                last_seen=p.last_seen,
                last_updated=p.last_updated
            )
            db.add(model)

            # Record version history
            v = ProfileVersionModel(
                profile_id=p.id,
                change_type="created",
                field_name="profile",
                old_value=None,
                new_value=f"Initial synthetic ingestion for {p.candidate_code or p.id}"
            )
            db.add(v)

    db.commit()


def seed_sample_shortlists_and_notes(db: Session):
    """Seed initial sample shortlisted profiles and private notes for testing UI."""
    sample_shortlists = [
        {"profile_id": "mock-001", "stage": "Shortlisted", "notes": "Strong candidate matching all primary preferences."},
        {"profile_id": "mock-002", "stage": "Interesting", "notes": "Hafiz and Hadith lecturer in Rangpur."},
        {"profile_id": "mock-004", "stage": "Need Review", "notes": "Check duplicate cross-listing with Candidate #31."}
    ]

    for item in sample_shortlists:
        existing = db.query(ShortlistModel).filter(ShortlistModel.profile_id == item["profile_id"]).first()
        if not existing:
            sl = ShortlistModel(
                profile_id=item["profile_id"],
                stage=item["stage"],
                notes=item["notes"]
            )
            db.add(sl)

    sample_notes = [
        {"profile_id": "mock-001", "content": "Family lives in Rangpur Sadar. Verified masjid attendance through local contact."},
        {"profile_id": "mock-004", "content": "Remote software job; check if planning to relocate or stay in Rangpur."}
    ]

    for item in sample_notes:
        existing = db.query(NoteModel).filter(
            NoteModel.profile_id == item["profile_id"],
            NoteModel.content == item["content"]
        ).first()
        if not existing:
            note = NoteModel(
                profile_id=item["profile_id"],
                content=item["content"]
            )
            db.add(note)

    db.commit()


def run_seed():
    """Main seed entrypoint."""
    init_db()
    db = SessionLocal()
    try:
        seed_sources(db)
        seed_search_profiles(db)
        seed_synthetic_profiles(db)
        seed_sample_shortlists_and_notes(db)
        print("Successfully seeded NikahLens database with synthetic profiles, searches, and sources.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

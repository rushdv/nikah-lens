"""
SQLAlchemy Database Models for NikahLens.
Includes core searchable attributes in structured columns and flexible fields in JSON.
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from database.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    source = Column(String(64), nullable=False, index=True)
    source_profile_id = Column(String(128), nullable=False, index=True)
    candidate_code = Column(String(64), nullable=True)
    profile_url = Column(String(512), nullable=True)

    gender = Column(String(16), nullable=False, default="male", index=True)
    age = Column(Integer, nullable=True, index=True)
    height_cm = Column(Float, nullable=True, index=True)
    height_display = Column(String(32), nullable=True)

    marital_status = Column(String(64), nullable=False, default="never_married", index=True)
    current_location = Column(String(128), nullable=True, index=True)
    permanent_location = Column(String(128), nullable=True, index=True)

    # Structured JSON fields
    education = Column(JSON, nullable=False, default=dict)
    career = Column(JSON, nullable=False, default=dict)
    deen = Column(JSON, nullable=False, default=dict)

    synthetic = Column(Boolean, default=False, nullable=False)
    raw_data = Column(JSON, nullable=True)

    first_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True)

    # Relationships
    versions = relationship("ProfileVersionModel", back_populates="profile", cascade="all, delete-orphan")
    shortlist_item = relationship("ShortlistModel", back_populates="profile", uselist=False, cascade="all, delete-orphan")
    notes = relationship("NoteModel", back_populates="profile", cascade="all, delete-orphan")


class ProfileVersionModel(Base):
    __tablename__ = "profile_versions"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    profile_id = Column(String(64), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    change_type = Column(String(64), nullable=False)  # 'created', 'updated', 'location_change', 'career_change'
    field_name = Column(String(64), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    profile = relationship("ProfileModel", back_populates="versions")


class SearchProfileModel(Base):
    __tablename__ = "search_profiles"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    criteria = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True)


class ShortlistModel(Base):
    __tablename__ = "shortlists"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    profile_id = Column(String(64), ForeignKey("profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    stage = Column(String(64), nullable=False, default="Shortlisted")  # New, Interesting, Shortlisted, Need Review, Contact Later, Archived
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True)

    profile = relationship("ProfileModel", back_populates="shortlist_item")


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    profile_id = Column(String(64), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True)

    profile = relationship("ProfileModel", back_populates="notes")


class SourceModel(Base):
    __tablename__ = "sources"

    name = Column(String(64), primary_key=True)
    display_name = Column(String(128), nullable=False)
    enabled = Column(Boolean, default=False, nullable=False)
    mode = Column(String(64), nullable=False, default="disabled")
    terms_compliance_notes = Column(Text, nullable=True)
    permits_automated_collection = Column(Boolean, default=False, nullable=False)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)

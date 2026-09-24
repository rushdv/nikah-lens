"""
Shortlist schema.
Tracks candidate review stages:
New, Interesting, Shortlisted, Need Review, Contact Later, Archived.
"""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from packages.schemas.profile import ProfileResponse


class ShortlistStage(str, Enum):
    NEW = "New"
    INTERESTING = "Interesting"
    SHORTLISTED = "Shortlisted"
    NEED_REVIEW = "Need Review"
    CONTACT_LATER = "Contact Later"
    ARCHIVED = "Archived"


class ShortlistCreate(BaseModel):
    profile_id: str
    stage: ShortlistStage = ShortlistStage.SHORTLISTED
    notes: Optional[str] = None


class ShortlistUpdate(BaseModel):
    stage: Optional[ShortlistStage] = None
    notes: Optional[str] = None


class ShortlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_id: str
    stage: ShortlistStage
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    profile: Optional[ProfileResponse] = None

"""
Search and Matching Schemas.
Supports deterministic filtering with transparent match explanations.
NO misleading single compatibility percentages.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from packages.schemas.profile import ProfileResponse


class RequirementPriority(str, Enum):
    REQUIRED = "REQUIRED"
    PREFERRED = "PREFERRED"
    OPTIONAL = "OPTIONAL"
    EXCLUDED = "EXCLUDED"


class MatchStatus(str, Enum):
    STRONG_MATCH = "Strong Match"
    POTENTIAL_MATCH = "Potential Match"
    NEEDS_REVIEW = "Needs Review"
    HARD_REQUIREMENT_NOT_MET = "Hard Requirement Not Met"


class AgeCriteria(BaseModel):
    min: Optional[int] = 22
    max: Optional[int] = 29
    priority: RequirementPriority = RequirementPriority.REQUIRED


class HeightCriteria(BaseModel):
    min_cm: Optional[float] = 165.1  # 5'5"
    priority: RequirementPriority = RequirementPriority.REQUIRED


class LocationItem(BaseModel):
    name: str
    priority: RequirementPriority = RequirementPriority.PREFERRED


class MaritalStatusCriteria(BaseModel):
    values: List[str] = Field(default_factory=lambda: ["never_married"])
    priority: RequirementPriority = RequirementPriority.REQUIRED


class DeenCriteria(BaseModel):
    priority: str = "very_high"  # "very_high", "high", "medium", "flexible"
    require_salah: bool = True
    require_quran: bool = False
    prefer_beard: bool = True
    prefer_islamic_studies: bool = False


class CareerCriteria(BaseModel):
    priority: str = "high"  # "high", "medium", "flexible"
    require_occupation_stated: bool = True
    preferred_statuses: List[str] = Field(
        default_factory=lambda: ["employed", "business_owner", "professional", "entrepreneur", "freelancer"]
    )


class SearchCriteria(BaseModel):
    gender: str = "male"
    age: AgeCriteria = Field(default_factory=AgeCriteria)
    height: HeightCriteria = Field(default_factory=HeightCriteria)
    locations: List[LocationItem] = Field(default_factory=lambda: [
        LocationItem(name="Rangpur", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Dinajpur", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Kurigram", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Lalmonirhat", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Nilphamari", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Gaibandha", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Thakurgaon", priority=RequirementPriority.PREFERRED),
        LocationItem(name="Panchagarh", priority=RequirementPriority.PREFERRED),
    ])
    marital_status: MaritalStatusCriteria = Field(default_factory=MaritalStatusCriteria)
    deen: DeenCriteria = Field(default_factory=DeenCriteria)
    career: CareerCriteria = Field(default_factory=CareerCriteria)
    missing_data_disqualifies: bool = False  # By default unknown != fail


# Saved search profile models
class SearchProfileBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = False
    criteria: SearchCriteria = Field(default_factory=SearchCriteria)


class SearchProfileCreate(SearchProfileBase):
    pass


class SearchProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    criteria: Optional[SearchCriteria] = None


class SearchProfileResponse(SearchProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


# Duplicate candidate summary for result cards
class DuplicateSummary(BaseModel):
    is_duplicate: bool = False
    confidence: Optional[str] = None  # High, Medium, Low
    matched_profile_id: Optional[str] = None
    matched_source: Optional[str] = None
    reasons: List[str] = Field(default_factory=list)


# Search Result Item
class SearchResultItem(BaseModel):
    profile: ProfileResponse
    match_status: MatchStatus
    why_matched: List[str] = Field(default_factory=list)
    needs_review: List[str] = Field(default_factory=list)
    hard_failures: List[str] = Field(default_factory=list)
    duplicate_info: Optional[DuplicateSummary] = None


class SearchFilterRequest(BaseModel):
    criteria: Optional[SearchCriteria] = None
    search_profile_id: Optional[str] = None
    query: Optional[str] = None
    source_filter: Optional[str] = None
    limit: int = 50
    offset: int = 0
    sort_by: str = "match_status"  # match_status, age, height, last_seen


class SearchResponse(BaseModel):
    total: int
    results: List[SearchResultItem]
    summary_counts: Dict[str, int]

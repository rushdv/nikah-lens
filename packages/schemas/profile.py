"""
Unified Profile Schema.
Normalized representation of matrimonial profiles across all sources.
Retains source tracking while omitting unnecessary sensitive personal details.
"""

from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

from packages.schemas.deen import DeenProfile
from packages.schemas.career import CareerInformation
from packages.schemas.education import EducationInformation


class ProfileBase(BaseModel):
    source: str = Field(description="Origin source name, e.g. 'mock', 'ahlia'")
    source_profile_id: str = Field(description="Unique identifier at original source")
    candidate_code: Optional[str] = Field(default=None, description="Display candidate tag, e.g. 'Candidate #18'")
    profile_url: Optional[str] = Field(default=None, description="Original source profile URL if public")
    gender: str = Field(default="male", description="'male' or 'female'")
    age: Optional[int] = Field(default=None, description="Age in years")
    height_cm: Optional[float] = Field(default=None, description="Height normalized to centimeters")
    height_display: Optional[str] = Field(default=None, description="Human friendly height, e.g. 5'7\"")
    marital_status: str = Field(default="never_married", description="Marital status canonical code")
    current_location: Optional[str] = Field(default=None, description="Canonical current district/area")
    permanent_location: Optional[str] = Field(default=None, description="Canonical permanent district/area")
    education: EducationInformation = Field(default_factory=EducationInformation)
    career: CareerInformation = Field(default_factory=CareerInformation)
    deen: DeenProfile = Field(default_factory=DeenProfile)
    synthetic: bool = Field(default=False, description="True if generated mock data")
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Preserved relevant source fragments")


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    height_cm: Optional[float] = None
    height_display: Optional[str] = None
    marital_status: Optional[str] = None
    current_location: Optional[str] = None
    permanent_location: Optional[str] = None
    education: Optional[EducationInformation] = None
    career: Optional[CareerInformation] = None
    deen: Optional[DeenProfile] = None
    raw_data: Optional[Dict[str, Any]] = None


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    first_seen: datetime
    last_seen: datetime
    last_updated: Optional[datetime] = None


class ProfileVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_id: str
    change_type: str
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    recorded_at: datetime

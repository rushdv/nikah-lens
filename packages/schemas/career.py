"""
Career and Financial Information Schema.
Models factual employment and career status without making unverified
assumptions about wealth, income, or financial stability.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CareerStatus(str, Enum):
    STUDENT = "student"
    EMPLOYED = "employed"
    BUSINESS_OWNER = "business_owner"
    PROFESSIONAL = "professional"
    FREELANCER = "freelancer"
    ENTREPRENEUR = "entrepreneur"
    JOB_SEEKER = "job_seeker"
    UNEMPLOYED = "unemployed"
    UNSPECIFIED = "unspecified"


class CareerInformation(BaseModel):
    occupation: Optional[str] = Field(
        default=None,
        description="Current normalized profession or role title"
    )
    role_category: Optional[str] = Field(
        default=None,
        description="Standardized role category (e.g., Software Engineering, Teaching, Healthcare)"
    )
    industry: Optional[str] = Field(
        default=None,
        description="Industry or field of work"
    )
    employment_status: CareerStatus = Field(
        default=CareerStatus.UNSPECIFIED,
        description="Employment category"
    )
    career_stage: Optional[str] = Field(
        default=None,
        description="Career stage if stated (e.g. 'Entry-level', 'Mid-level', 'Established')"
    )
    raw_title: Optional[str] = Field(
        default=None,
        description="Original unedited text from source"
    )

    # Transparency flags: explicitly distinguish what is stated vs verified
    occupation_stated: bool = Field(
        default=False,
        description="True if occupation is explicitly stated"
    )
    career_stability_stated: bool = Field(
        default=False,
        description="True if candidate explicitly described stability"
    )
    income_stated: bool = Field(
        default=False,
        description="True if income or salary was explicitly mentioned in source"
    )
    financial_stability_verified: bool = Field(
        default=False,
        description="Never inferred; true only if independently verified by official means"
    )

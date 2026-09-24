"""
Deen Information Schema.
Strictly distinguishes self-reported vs verified information.
Never reduces religious practice to a single boolean and never claims
objective piety or subjective judgements.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EvidenceType(str, Enum):
    SELF_REPORTED = "self_reported"
    VERIFIED = "verified"
    UNKNOWN = "unknown"


class StatedStatus(str, Enum):
    STATED = "stated"
    NOT_STATED = "not_stated"
    UNKNOWN = "unknown"


class DeenAttribute(BaseModel):
    value: Optional[str] = Field(
        default=None,
        description="Factual representation of stated practice (e.g. 'regular', 'occasional', 'memorized')"
    )
    status: StatedStatus = Field(
        default=StatedStatus.UNKNOWN,
        description="Whether this attribute is explicitly stated, omitted, or unknown"
    )
    evidence_type: EvidenceType = Field(
        default=EvidenceType.SELF_REPORTED,
        description="Source of verification (e.g., self-reported vs verified)"
    )
    raw_text: Optional[str] = Field(
        default=None,
        description="Direct quote or snippet from original profile where stated"
    )

    def is_present(self) -> bool:
        return self.status == StatedStatus.STATED and bool(self.value)


class DeenProfile(BaseModel):
    salah: DeenAttribute = Field(default_factory=DeenAttribute)
    quran: DeenAttribute = Field(default_factory=DeenAttribute)
    islamic_studies: DeenAttribute = Field(default_factory=DeenAttribute)
    islamic_practice: DeenAttribute = Field(default_factory=DeenAttribute)
    halal_income: DeenAttribute = Field(default_factory=DeenAttribute)
    beard: DeenAttribute = Field(default_factory=DeenAttribute)
    religious_environment: DeenAttribute = Field(default_factory=DeenAttribute)
    self_description: DeenAttribute = Field(default_factory=DeenAttribute)
    other_notes: Optional[str] = None

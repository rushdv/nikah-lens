"""
Source Adapter and Configuration Schemas.
Every adapter is independently enable/disable-able and explicitly tracks legal/terms compliance.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SourceStatus(BaseModel):
    name: str
    display_name: str
    enabled: bool
    mode: str = Field(description="'mock', 'public_api', 'manual_import', 'disabled'")
    description: str
    terms_compliance_notes: str
    permits_automated_collection: bool = False
    profile_count: int = 0
    last_synced_at: Optional[datetime] = None


class SourceToggleRequest(BaseModel):
    enabled: bool

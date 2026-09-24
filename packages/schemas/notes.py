"""
Private Notes Schema.
Strictly private, local-only notes. Never exported or communicated to source websites.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NoteCreate(BaseModel):
    profile_id: str
    content: str = Field(min_length=1, max_length=5000)


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

"""
Education Information Schema.
"""

from typing import Optional
from pydantic import BaseModel, Field


class EducationInformation(BaseModel):
    degree: Optional[str] = Field(
        default=None,
        description="Normalized degree level (e.g. 'BSc', 'MSc', 'Alim', 'Fazil', 'MBA', 'Diploma')"
    )
    field: Optional[str] = Field(
        default=None,
        description="Field or major of study (e.g. 'Computer Science & Engineering', 'Islamic Studies')"
    )
    institution: Optional[str] = Field(
        default=None,
        description="Name of college, university, or madrasa if publicly stated"
    )
    raw_text: Optional[str] = Field(
        default=None,
        description="Exact raw text as reported in the source profile"
    )

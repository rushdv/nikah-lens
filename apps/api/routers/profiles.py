"""
Profiles Router.
Provides endpoints for retrieving unified profiles and version history.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.session import get_db
from database.models import ProfileModel, ProfileVersionModel
from packages.schemas.profile import ProfileResponse, ProfileVersionResponse
from packages.schemas.deen import DeenProfile
from packages.schemas.career import CareerInformation
from packages.schemas.education import EducationInformation

router = APIRouter(prefix="/profiles", tags=["Profiles"])


def model_to_response(m: ProfileModel) -> ProfileResponse:
    edu_dict = m.education if isinstance(m.education, dict) else {}
    career_dict = m.career if isinstance(m.career, dict) else {}
    deen_dict = m.deen if isinstance(m.deen, dict) else {}

    return ProfileResponse(
        id=m.id,
        source=m.source,
        source_profile_id=m.source_profile_id,
        candidate_code=m.candidate_code,
        profile_url=m.profile_url,
        gender=m.gender,
        age=m.age,
        height_cm=m.height_cm,
        height_display=m.height_display,
        marital_status=m.marital_status,
        current_location=m.current_location,
        permanent_location=m.permanent_location,
        education=EducationInformation(**edu_dict),
        career=CareerInformation(**career_dict),
        deen=DeenProfile(**deen_dict),
        synthetic=m.synthetic,
        raw_data=m.raw_data,
        first_seen=m.first_seen,
        last_seen=m.last_seen,
        last_updated=m.last_updated
    )


@router.get("", response_model=List[ProfileResponse])
def list_profiles(
    gender: Optional[str] = None,
    location: Optional[str] = None,
    source: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    q = db.query(ProfileModel)

    if gender:
        q = q.filter(ProfileModel.gender == gender.lower())

    if source:
        q = q.filter(ProfileModel.source == source.lower())

    if location:
        loc_pattern = f"%{location}%"
        q = q.filter(
            or_(
                ProfileModel.current_location.ilike(loc_pattern),
                ProfileModel.permanent_location.ilike(loc_pattern)
            )
        )

    if query:
        pattern = f"%{query}%"
        q = q.filter(
            or_(
                ProfileModel.candidate_code.ilike(pattern),
                ProfileModel.current_location.ilike(pattern),
                ProfileModel.permanent_location.ilike(pattern)
            )
        )

    profiles = q.order_by(ProfileModel.first_seen.desc()).offset(offset).limit(limit).all()
    return [model_to_response(p) for p in profiles]


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return model_to_response(profile)


@router.get("/{profile_id}/versions", response_model=List[ProfileVersionResponse])
def get_profile_versions(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    versions = db.query(ProfileVersionModel).filter(
        ProfileVersionModel.profile_id == profile_id
    ).order_by(ProfileVersionModel.recorded_at.desc()).all()

    return versions

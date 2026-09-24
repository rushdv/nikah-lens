"""
Saved Search Profiles Router.
Allows creating, viewing, activating, and managing user search criteria profiles.
"""

from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import SearchProfileModel
from packages.schemas.search import (
    SearchProfileCreate, SearchProfileUpdate, SearchProfileResponse, SearchCriteria
)

router = APIRouter(prefix="/search-profiles", tags=["Search Profiles"])


@router.get("", response_model=List[SearchProfileResponse])
def list_search_profiles(db: Session = Depends(get_db)):
    profiles = db.query(SearchProfileModel).order_by(SearchProfileModel.created_at.desc()).all()
    results = []
    for sp in profiles:
        criteria_obj = SearchCriteria(**sp.criteria) if isinstance(sp.criteria, dict) else SearchCriteria()
        results.append(
            SearchProfileResponse(
                id=sp.id,
                name=sp.name,
                description=sp.description,
                is_active=sp.is_active,
                criteria=criteria_obj,
                created_at=sp.created_at,
                updated_at=sp.updated_at
            )
        )
    return results


@router.post("", response_model=SearchProfileResponse, status_code=201)
def create_search_profile(payload: SearchProfileCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    if payload.is_active:
        db.query(SearchProfileModel).update({"is_active": False})

    new_profile = SearchProfileModel(
        name=payload.name,
        description=payload.description,
        is_active=payload.is_active,
        criteria=payload.criteria.model_dump(),
        created_at=now,
        updated_at=now
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return SearchProfileResponse(
        id=new_profile.id,
        name=new_profile.name,
        description=new_profile.description,
        is_active=new_profile.is_active,
        criteria=SearchCriteria(**new_profile.criteria),
        created_at=new_profile.created_at,
        updated_at=new_profile.updated_at
    )


@router.get("/{profile_id}", response_model=SearchProfileResponse)
def get_search_profile(profile_id: str, db: Session = Depends(get_db)):
    sp = db.query(SearchProfileModel).filter(SearchProfileModel.id == profile_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Search profile not found")
    return SearchProfileResponse(
        id=sp.id,
        name=sp.name,
        description=sp.description,
        is_active=sp.is_active,
        criteria=SearchCriteria(**sp.criteria),
        created_at=sp.created_at,
        updated_at=sp.updated_at
    )


@router.patch("/{profile_id}", response_model=SearchProfileResponse)
def update_search_profile(profile_id: str, payload: SearchProfileUpdate, db: Session = Depends(get_db)):
    sp = db.query(SearchProfileModel).filter(SearchProfileModel.id == profile_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Search profile not found")

    if payload.name is not None:
        sp.name = payload.name
    if payload.description is not None:
        sp.description = payload.description
    if payload.is_active is not None:
        if payload.is_active:
            db.query(SearchProfileModel).filter(SearchProfileModel.id != profile_id).update({"is_active": False})
        sp.is_active = payload.is_active
    if payload.criteria is not None:
        sp.criteria = payload.criteria.model_dump()

    sp.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(sp)

    return SearchProfileResponse(
        id=sp.id,
        name=sp.name,
        description=sp.description,
        is_active=sp.is_active,
        criteria=SearchCriteria(**sp.criteria),
        created_at=sp.created_at,
        updated_at=sp.updated_at
    )


@router.delete("/{profile_id}")
def delete_search_profile(profile_id: str, db: Session = Depends(get_db)):
    sp = db.query(SearchProfileModel).filter(SearchProfileModel.id == profile_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Search profile not found")
    db.delete(sp)
    db.commit()
    return {"message": "Search profile deleted successfully"}

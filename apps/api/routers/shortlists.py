"""
Shortlist Router.
Manages candidate review stages: New, Interesting, Shortlisted, Need Review, Contact Later, Archived.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import ShortlistModel, ProfileModel
from packages.schemas.shortlist import (
    ShortlistCreate, ShortlistUpdate, ShortlistResponse, ShortlistStage
)
from apps.api.routers.profiles import model_to_response

router = APIRouter(prefix="/shortlists", tags=["Shortlist"])


@router.get("", response_model=List[ShortlistResponse])
def list_shortlists(stage: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(ShortlistModel)
    if stage:
        q = q.filter(ShortlistModel.stage == stage)

    items = q.order_by(ShortlistModel.updated_at.desc()).all()
    results = []
    for item in items:
        prof_resp = model_to_response(item.profile) if item.profile else None
        results.append(
            ShortlistResponse(
                id=item.id,
                profile_id=item.profile_id,
                stage=ShortlistStage(item.stage),
                notes=item.notes,
                created_at=item.created_at,
                updated_at=item.updated_at,
                profile=prof_resp
            )
        )
    return results


@router.post("", response_model=ShortlistResponse)
def add_to_shortlist(payload: ShortlistCreate, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.id == payload.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    existing = db.query(ShortlistModel).filter(ShortlistModel.profile_id == payload.profile_id).first()
    now = datetime.now(timezone.utc)

    if existing:
        existing.stage = payload.stage.value
        if payload.notes is not None:
            existing.notes = payload.notes
        existing.updated_at = now
        db.commit()
        db.refresh(existing)
        return ShortlistResponse(
            id=existing.id,
            profile_id=existing.profile_id,
            stage=ShortlistStage(existing.stage),
            notes=existing.notes,
            created_at=existing.created_at,
            updated_at=existing.updated_at,
            profile=model_to_response(profile)
        )

    new_item = ShortlistModel(
        profile_id=payload.profile_id,
        stage=payload.stage.value,
        notes=payload.notes,
        created_at=now,
        updated_at=now
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return ShortlistResponse(
        id=new_item.id,
        profile_id=new_item.profile_id,
        stage=ShortlistStage(new_item.stage),
        notes=new_item.notes,
        created_at=new_item.created_at,
        updated_at=new_item.updated_at,
        profile=model_to_response(profile)
    )


@router.patch("/{shortlist_id}", response_model=ShortlistResponse)
def update_shortlist(shortlist_id: str, payload: ShortlistUpdate, db: Session = Depends(get_db)):
    item = db.query(ShortlistModel).filter(ShortlistModel.id == shortlist_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Shortlist item not found")

    if payload.stage is not None:
        item.stage = payload.stage.value
    if payload.notes is not None:
        item.notes = payload.notes

    item.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)

    return ShortlistResponse(
        id=item.id,
        profile_id=item.profile_id,
        stage=ShortlistStage(item.stage),
        notes=item.notes,
        created_at=item.created_at,
        updated_at=item.updated_at,
        profile=model_to_response(item.profile) if item.profile else None
    )


@router.delete("/{shortlist_id}")
def delete_shortlist(shortlist_id: str, db: Session = Depends(get_db)):
    item = db.query(ShortlistModel).filter(ShortlistModel.id == shortlist_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Shortlist item not found")
    db.delete(item)
    db.commit()
    return {"message": "Shortlist item deleted successfully"}

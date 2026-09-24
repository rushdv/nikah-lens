"""
Private Notes Router.
Manages private personal notes attached to candidates.
Strictly local and never transmitted to external sources.
"""

from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import NoteModel, ProfileModel
from packages.schemas.notes import NoteCreate, NoteResponse

router = APIRouter(tags=["Notes"])


@router.get("/profiles/{profile_id}/notes", response_model=List[NoteResponse])
def get_profile_notes(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    notes = db.query(NoteModel).filter(
        NoteModel.profile_id == profile_id
    ).order_by(NoteModel.created_at.desc()).all()

    return notes


@router.post("/notes", response_model=NoteResponse, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.id == payload.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    now = datetime.now(timezone.utc)
    new_note = NoteModel(
        profile_id=payload.profile_id,
        content=payload.content,
        created_at=now,
        updated_at=now
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.delete("/notes/{note_id}")
def delete_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}

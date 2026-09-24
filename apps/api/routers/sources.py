"""
Sources Router.
Exposes source adapter states, terms compliance policies, and toggle controls.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import SourceModel, ProfileModel
from packages.schemas.source import SourceStatus, SourceToggleRequest
from services.collectors import registry

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.get("", response_model=List[SourceStatus])
def list_sources(db: Session = Depends(get_db)):
    sources_in_db = {s.name: s for s in db.query(SourceModel).all()}
    results = []

    for adapter in registry.list_adapters():
        db_s = sources_in_db.get(adapter.name)
        enabled = db_s.enabled if db_s else adapter.is_enabled
        count = db.query(ProfileModel).filter(ProfileModel.source == adapter.name).count()

        results.append(
            SourceStatus(
                name=adapter.name,
                display_name=adapter.display_name,
                enabled=enabled,
                mode=adapter.mode,
                description=adapter.display_name,
                terms_compliance_notes=adapter.terms_compliance_notes,
                permits_automated_collection=adapter.permits_automated_collection,
                profile_count=count,
                last_synced_at=db_s.last_synced_at if db_s else None
            )
        )
    return results


@router.patch("/{source_name}/toggle", response_model=SourceStatus)
def toggle_source(source_name: str, payload: SourceToggleRequest, db: Session = Depends(get_db)):
    source_name = source_name.lower()
    adapter = registry.get_adapter(source_name)
    if not adapter:
        raise HTTPException(status_code=404, detail="Source adapter not found")

    registry.toggle_adapter(source_name, payload.enabled)

    db_s = db.query(SourceModel).filter(SourceModel.name == source_name).first()
    if db_s:
        db_s.enabled = payload.enabled
        db.commit()
        db.refresh(db_s)

    count = db.query(ProfileModel).filter(ProfileModel.source == source_name).count()

    return SourceStatus(
        name=adapter.name,
        display_name=adapter.display_name,
        enabled=payload.enabled,
        mode=adapter.mode,
        description=adapter.display_name,
        terms_compliance_notes=adapter.terms_compliance_notes,
        permits_automated_collection=adapter.permits_automated_collection,
        profile_count=count,
        last_synced_at=db_s.last_synced_at if db_s else None
    )

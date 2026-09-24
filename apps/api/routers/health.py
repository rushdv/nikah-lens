"""
Health and Status Router.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.session import get_db
from services.collectors import registry

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health(db: Session = Depends(get_db)):
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    adapters = [
        {"name": a.name, "enabled": a.is_enabled, "mode": a.mode}
        for a in registry.list_adapters()
    ]

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "unreachable",
        "version": "0.1.0",
        "adapters": adapters
    }

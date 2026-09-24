"""
Duplicates and System Operations Router.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db, SessionLocal
from database.models import ProfileModel
from database.seed.seed_data import run_seed
from services.deduplicator.detector import DuplicateDetector
from apps.api.routers.profiles import model_to_response

router = APIRouter(tags=["Duplicates & System"])


@router.get("/duplicates")
def get_duplicates(db: Session = Depends(get_db)):
    all_profiles = [model_to_response(p) for p in db.query(ProfileModel).all()]
    dup_map = DuplicateDetector.find_duplicates_in_dataset(all_profiles)

    results = []
    # Deduplicate pair representations
    seen_pairs = set()
    profile_dict = {p.id: p for p in all_profiles}

    for p_id, summary in dup_map.items():
        matched_id = summary.matched_profile_id
        pair_key = tuple(sorted([p_id, matched_id]))
        if pair_key not in seen_pairs:
            seen_pairs.add(pair_key)
            results.append({
                "profile_a": profile_dict.get(p_id),
                "profile_b": profile_dict.get(matched_id),
                "confidence": summary.confidence,
                "reasons": summary.reasons
            })

    return {
        "total_duplicate_pairs": len(results),
        "pairs": results
    }


@router.post("/system/reset-seed")
def reset_seed():
    """Resets and re-seeds database with initial synthetic mock profiles."""
    run_seed()
    return {"status": "success", "message": "Synthetic profiles and sources re-seeded successfully."}

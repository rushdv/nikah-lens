"""
Deterministic Search Router.
Implements multi-attribute filtering and transparent match explanations.
"""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import ProfileModel, SearchProfileModel
from packages.schemas.search import (
    SearchFilterRequest, SearchResponse, SearchResultItem, SearchCriteria, MatchStatus
)
from services.matcher.engine import MatchEngine
from services.deduplicator.detector import DuplicateDetector
from apps.api.routers.profiles import model_to_response

router = APIRouter(prefix="/search", tags=["Search"])

STATUS_ORDER = {
    MatchStatus.STRONG_MATCH: 1,
    MatchStatus.POTENTIAL_MATCH: 2,
    MatchStatus.NEEDS_REVIEW: 3,
    MatchStatus.HARD_REQUIREMENT_NOT_MET: 4,
}


@router.post("", response_model=SearchResponse)
def execute_search(request: SearchFilterRequest, db: Session = Depends(get_db)):
    # Determine criteria to apply
    criteria: SearchCriteria
    if request.criteria:
        criteria = request.criteria
    elif request.search_profile_id:
        sp = db.query(SearchProfileModel).filter(SearchProfileModel.id == request.search_profile_id).first()
        if not sp:
            raise HTTPException(status_code=404, detail="Search profile not found")
        criteria = SearchCriteria(**sp.criteria)
    else:
        # Default criteria
        criteria = SearchCriteria()

    # Query profiles
    q = db.query(ProfileModel)
    if request.source_filter:
        q = q.filter(ProfileModel.source == request.source_filter.lower())
    if criteria.gender:
        q = q.filter(ProfileModel.gender == criteria.gender.lower())

    all_db_profiles = q.all()
    profile_responses = [model_to_response(p) for p in all_db_profiles]

    # Run duplicate detection across candidate pool
    dup_map = DuplicateDetector.find_duplicates_in_dataset(profile_responses)

    # Evaluate each candidate deterministically
    evaluated_items: List[SearchResultItem] = []
    summary_counts: Dict[str, int] = {
        MatchStatus.STRONG_MATCH.value: 0,
        MatchStatus.POTENTIAL_MATCH.value: 0,
        MatchStatus.NEEDS_REVIEW.value: 0,
        MatchStatus.HARD_REQUIREMENT_NOT_MET.value: 0,
    }

    for p in profile_responses:
        item = MatchEngine.evaluate(p, criteria)
        # Attach duplicate info if detected
        if p.id in dup_map:
            item.duplicate_info = dup_map[p.id]

        summary_counts[item.match_status.value] += 1
        evaluated_items.append(item)

    # Sort results
    if request.sort_by == "match_status":
        evaluated_items.sort(key=lambda x: STATUS_ORDER.get(x.match_status, 99))
    elif request.sort_by == "age":
        evaluated_items.sort(key=lambda x: x.profile.age or 999)
    elif request.sort_by == "height":
        evaluated_items.sort(key=lambda x: -(x.profile.height_cm or 0))

    # Paginate
    paged_items = evaluated_items[request.offset : request.offset + request.limit]

    return SearchResponse(
        total=len(evaluated_items),
        results=paged_items,
        summary_counts=summary_counts
    )

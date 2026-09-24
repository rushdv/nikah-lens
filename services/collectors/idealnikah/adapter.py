"""
Ideal Nikah Source Adapter Interface.
Complies with source terms of service and robots directives.
"""

from typing import List, Optional, Dict, Any
from packages.schemas.profile import ProfileResponse
from packages.schemas.search import SearchCriteria
from services.collectors.base.adapter import BaseSourceAdapter


class IdealNikahSourceAdapter(BaseSourceAdapter):
    name: str = "idealnikah"
    display_name: str = "Ideal Nikah"
    is_enabled: bool = False
    permits_automated_collection: bool = False
    mode: str = "manual_import"
    terms_compliance_notes: str = (
        "Operates in manual import mode. Unauthenticated scraping or bypass of security measures is not permitted."
    )

    def search(self, criteria: SearchCriteria) -> List[ProfileResponse]:
        return []

    def fetch_profile(self, profile_id_or_url: str) -> Optional[ProfileResponse]:
        return None

    def normalize(self, raw_data: Dict[str, Any]) -> ProfileResponse:
        raise NotImplementedError("Ideal Nikah normalization available for manual import records.")

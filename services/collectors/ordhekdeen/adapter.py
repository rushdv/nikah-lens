"""
Ordhek Deen Source Adapter Interface.
Complies with source terms of service and robots directives.
Automated collection without written permission is prohibited.
"""

from typing import List, Optional, Dict, Any
from packages.schemas.profile import ProfileResponse
from packages.schemas.search import SearchCriteria
from services.collectors.base.adapter import BaseSourceAdapter


class OrdhekDeenSourceAdapter(BaseSourceAdapter):
    name: str = "ordhekdeen"
    display_name: str = "Ordhek Deen"
    is_enabled: bool = False
    permits_automated_collection: bool = False
    mode: str = "manual_import"
    terms_compliance_notes: str = (
        "Strict adherence to Ordhek Deen privacy policies and terms. Unauthenticated automated collection "
        "is disabled. Adapter provides structured manual export/import interfaces."
    )

    def search(self, criteria: SearchCriteria) -> List[ProfileResponse]:
        return []

    def fetch_profile(self, profile_id_or_url: str) -> Optional[ProfileResponse]:
        return None

    def normalize(self, raw_data: Dict[str, Any]) -> ProfileResponse:
        raise NotImplementedError("Ordhek Deen normalization available for manual import records.")

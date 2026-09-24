"""
Ahlia Matrimony Source Adapter Interface.
Complies with source terms of service and robots directives.
Automated unauthenticated scraping is strictly prohibited. Operates in manual-import
or authenticated-API mode only.
"""

from typing import List, Optional, Dict, Any
from packages.schemas.profile import ProfileResponse
from packages.schemas.search import SearchCriteria
from services.collectors.base.adapter import BaseSourceAdapter


class AhliaSourceAdapter(BaseSourceAdapter):
    name: str = "ahlia"
    display_name: str = "Ahlia Matrimony"
    is_enabled: bool = False
    permits_automated_collection: bool = False
    mode: str = "manual_import"
    terms_compliance_notes: str = (
        "Automated scraping is disabled in compliance with Ahlia Terms of Service and robots.txt. "
        "Supports manual JSON/CSV profile imports provided directly by the user."
    )

    def search(self, criteria: SearchCriteria) -> List[ProfileResponse]:
        if not self.is_enabled:
            return []
        # In manual import mode, searches against locally imported Ahlia profiles
        return []

    def fetch_profile(self, profile_id_or_url: str) -> Optional[ProfileResponse]:
        return None

    def normalize(self, raw_data: Dict[str, Any]) -> ProfileResponse:
        raise NotImplementedError("Ahlia normalization available for manual import records.")

"""
Base Source Adapter Interface.
Defines standard contract for all matrimonial data sources.
Every adapter is independently toggleable and strictly honors data/terms policies.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from packages.schemas.profile import ProfileResponse
from packages.schemas.search import SearchCriteria
from packages.schemas.source import SourceStatus


class BaseSourceAdapter(ABC):
    """
    Abstract contract for source adapters.
    """
    name: str = "base"
    display_name: str = "Base Adapter"
    is_enabled: bool = False
    permits_automated_collection: bool = False
    mode: str = "disabled"
    terms_compliance_notes: str = ""

    @abstractmethod
    def search(self, criteria: SearchCriteria) -> List[ProfileResponse]:
        """Search profiles from this source matching the criteria."""
        pass

    @abstractmethod
    def fetch_profile(self, profile_id_or_url: str) -> Optional[ProfileResponse]:
        """Fetch a specific profile by ID or canonical URL."""
        pass

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> ProfileResponse:
        """Convert source-specific raw data into unified ProfileResponse."""
        pass

    def get_metadata(self, profile_count: int = 0) -> SourceStatus:
        """Returns source health, capability, and compliance metadata."""
        return SourceStatus(
            name=self.name,
            display_name=self.display_name,
            enabled=self.is_enabled,
            mode=self.mode,
            description=self.__doc__ or self.display_name,
            terms_compliance_notes=self.terms_compliance_notes,
            permits_automated_collection=self.permits_automated_collection,
            profile_count=profile_count
        )

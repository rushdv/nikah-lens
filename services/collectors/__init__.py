from typing import Dict, List
from services.collectors.base.adapter import BaseSourceAdapter
from services.collectors.mock.adapter import MockSourceAdapter
from services.collectors.ahlia.adapter import AhliaSourceAdapter
from services.collectors.ordhekdeen.adapter import OrdhekDeenSourceAdapter
from services.collectors.idealnikah.adapter import IdealNikahSourceAdapter


class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, BaseSourceAdapter] = {
            "mock": MockSourceAdapter(),
            "ahlia": AhliaSourceAdapter(),
            "ordhekdeen": OrdhekDeenSourceAdapter(),
            "idealnikah": IdealNikahSourceAdapter(),
        }

    def get_adapter(self, name: str) -> BaseSourceAdapter:
        return self._adapters.get(name.lower())

    def list_adapters(self) -> List[BaseSourceAdapter]:
        return list(self._adapters.values())

    def toggle_adapter(self, name: str, enabled: bool) -> bool:
        adapter = self._adapters.get(name.lower())
        if adapter:
            adapter.is_enabled = enabled
            return True
        return False


registry = AdapterRegistry()

__all__ = [
    "BaseSourceAdapter",
    "MockSourceAdapter",
    "AhliaSourceAdapter",
    "OrdhekDeenSourceAdapter",
    "IdealNikahSourceAdapter",
    "AdapterRegistry",
    "registry"
]

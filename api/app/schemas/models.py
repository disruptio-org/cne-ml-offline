"""Schema objects describing model registry payloads."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Mapping, Optional


@dataclass
class ModelInfo:
    """Metadata describing a single model version."""

    version: str
    created_at: datetime
    metrics: Optional[Mapping[str, float]] = None

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "version": self.version,
            "created_at": self.created_at.isoformat(),
        }
        if self.metrics is not None:
            payload["metrics"] = dict(self.metrics)
        return payload


@dataclass
class ModelHistory:
    """Paginated listing of models stored in the registry."""

    page: int
    size: int
    total: int
    items: List[ModelInfo] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "page": self.page,
            "size": self.size,
            "total": self.total,
            "items": [item.to_dict() for item in self.items],
        }

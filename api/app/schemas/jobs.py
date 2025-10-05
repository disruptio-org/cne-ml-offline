"""Schema objects describing job payloads."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class JobState(str, Enum):
    queued = "queued"
    processing = "processing"
    ready = "ready"
    approved = "approved"
    failed = "failed"


@dataclass
class JobStats:
    rows_total: Optional[int] = None
    rows_ok: Optional[int] = None
    rows_warn: Optional[int] = None
    rows_err: Optional[int] = None
    ocr_conf_mean: Optional[float] = None

    def to_dict(self) -> Dict[str, Optional[float]]:
        payload: Dict[str, Optional[float]] = asdict(self)
        return {key: value for key, value in payload.items() if value is not None}


@dataclass
class JobStatus:
    job_id: str
    state: JobState
    created_at: datetime
    updated_at: datetime
    input_files: List[str] = field(default_factory=list)
    pages: Optional[int] = None
    stats: Optional[JobStats] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "job_id": self.job_id,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "input_files": list(self.input_files),
            "pages": self.pages,
            "error": self.error,
        }
        if self.stats is not None:
            payload["stats"] = self.stats.to_dict()
        return payload


@dataclass
class JobCreated:
    job_id: str
    status: JobState

    def to_dict(self) -> Dict[str, str]:
        return {"job_id": self.job_id, "status": self.status.value}

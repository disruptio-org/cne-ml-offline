"""Persistent metadata helpers for worker job execution."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union


class JobState(str, Enum):
    queued = "queued"
    processing = "processing"
    ready = "ready"
    approved = "approved"
    failed = "failed"


@dataclass
class JobMetadata:
    job_id: str
    state: JobState
    created_at: datetime
    updated_at: datetime
    input_files: List[str] = field(default_factory=list)
    csv_path: Optional[str] = None
    pages: Optional[int] = None
    stats: Dict[str, Union[int, float, None]] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        payload = asdict(self)
        payload["state"] = self.state.value
        payload["created_at"] = self.created_at.isoformat()
        payload["updated_at"] = self.updated_at.isoformat()
        return payload

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "JobMetadata":
        return cls(
            job_id=str(data["job_id"]),
            state=JobState(str(data["state"])),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            updated_at=datetime.fromisoformat(str(data["updated_at"])),
            input_files=[str(item) for item in data.get("input_files", [])],
            csv_path=data.get("csv_path"),
            pages=data.get("pages"),
            stats=_coerce_stats(dict(data.get("stats", {}))),
            error=data.get("error"),
        )


def _coerce_stats(raw: Dict[str, object]) -> Dict[str, Union[int, float, None]]:
    stats: Dict[str, Union[int, float, None]] = {}
    for key, value in raw.items():
        if value is None:
            stats[key] = None
            continue
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            numeric = float(value)
        else:
            try:
                numeric = float(str(value))
            except (TypeError, ValueError):
                continue
        if numeric.is_integer():
            stats[key] = int(numeric)
        else:
            stats[key] = numeric
    return stats


class JobStorage:
    """Stores job metadata under ``data/jobs/<job_id>``."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        root = Path(base_dir or Path("data"))
        self.base_dir = root.resolve()
        self.jobs_dir = self.base_dir / "jobs"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.jobs_dir.mkdir(parents=True, exist_ok=True)

    def _job_dir(self, job_id: str) -> Path:
        return self.jobs_dir / job_id

    def _job_meta_path(self, job_id: str) -> Path:
        return self._job_dir(job_id) / "job.json"

    def ensure(self, job_id: str, input_files: List[Path]) -> JobMetadata:
        try:
            return self.load(job_id)
        except FileNotFoundError:
            pass
        now = datetime.now(timezone.utc)
        meta = JobMetadata(
            job_id=job_id,
            state=JobState.queued,
            created_at=now,
            updated_at=now,
            input_files=[str(path) for path in input_files],
        )
        self._persist(meta)
        return meta

    def load(self, job_id: str) -> JobMetadata:
        meta_path = self._job_meta_path(job_id)
        if not meta_path.exists():
            raise FileNotFoundError(f"Job '{job_id}' metadata not found")
        payload = json.loads(meta_path.read_text(encoding="utf-8"))
        return JobMetadata.from_dict(payload)

    def update(self, job_id: str, **changes: object) -> JobMetadata:
        meta = self.load(job_id)
        for key, value in changes.items():
            if hasattr(meta, key):
                setattr(meta, key, value)
        meta.updated_at = datetime.now(timezone.utc)
        self._persist(meta)
        return meta

    def mark_state(self, job_id: str, state: JobState, **changes: object) -> JobMetadata:
        meta = self.load(job_id)
        meta.state = state
        for key, value in changes.items():
            if hasattr(meta, key):
                setattr(meta, key, value)
        meta.updated_at = datetime.now(timezone.utc)
        self._persist(meta)
        return meta

    def _persist(self, meta: JobMetadata) -> None:
        job_dir = self._job_dir(meta.job_id)
        job_dir.mkdir(parents=True, exist_ok=True)
        meta_path = self._job_meta_path(meta.job_id)
        meta_path.write_text(json.dumps(meta.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

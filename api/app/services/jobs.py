"""Job service helpers for preparing API responses."""
from __future__ import annotations

from typing import Optional

from worker.src.storage import JobMetadata

from ..schemas.jobs import JobStats


def build_job_stats(metadata: JobMetadata) -> Optional[JobStats]:
    """Convert persisted statistics into the API schema representation."""

    stats = metadata.stats or {}
    if not stats:
        return None
    return JobStats(
        rows_total=stats.get("rows_total"),
        rows_ok=stats.get("rows_ok"),
        rows_warn=stats.get("rows_warn"),
        rows_err=stats.get("rows_err"),
        ocr_conf_mean=stats.get("ocr_conf_mean"),
    )

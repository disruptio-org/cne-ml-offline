"""FastAPI application exposing job metadata endpoints."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from worker.src.storage import JobStorage

from .routes import models as models_routes
from .schemas.jobs import JobState, JobStatus
from .services import build_job_stats

try:  # pragma: no cover - optional dependency for runtime API usage
    from fastapi import Depends, FastAPI, HTTPException
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without FastAPI
    FastAPI = None

    class HTTPException(RuntimeError):
        def __init__(self, status_code: int, detail: str) -> None:
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)

    def Depends(factory: Callable) -> Callable:
        return factory


def get_storage() -> JobStorage:
    base_dir = Path(os.environ.get("CNE_DATA_DIR", "data"))
    return JobStorage(base_dir)


if FastAPI is not None:
    app = FastAPI(title="CNE Offline API")

    if models_routes.router is not None:
        app.include_router(models_routes.router)

    @app.get("/api/jobs/{job_id}", response_model=JobStatus)
    async def read_job(job_id: str, storage: JobStorage = Depends(get_storage)) -> JobStatus:
        try:
            metadata = storage.load(job_id)
        except FileNotFoundError as exc:  # pragma: no cover - FastAPI handles HTTPException
            raise HTTPException(status_code=404, detail="Job not found") from exc

        stats = build_job_stats(metadata)
        return JobStatus(
            job_id=metadata.job_id,
            state=JobState(metadata.state.value),
            created_at=metadata.created_at,
            updated_at=metadata.updated_at,
            input_files=metadata.input_files,
            pages=metadata.pages,
            stats=stats,
            error=metadata.error,
        )
else:  # pragma: no cover - runtime fallback
    app = None

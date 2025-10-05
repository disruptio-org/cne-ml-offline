"""FastAPI routes exposing model registry information."""
from __future__ import annotations

from typing import Sequence

from ..services.models import RegistryRecord, get_history as get_model_history, load_registry

try:  # pragma: no cover - FastAPI optional dependency
    from fastapi import APIRouter, Depends, Query
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without FastAPI
    APIRouter = None  # type: ignore

    def Depends(factory):  # type: ignore
        return factory

    def Query(default, **_kwargs):  # type: ignore
        return default


def get_registry() -> Sequence[RegistryRecord]:
    """Return raw model registry records from persistent storage."""

    return load_registry()


if APIRouter is not None:  # pragma: no branch - runtime guard
    router = APIRouter(prefix="/api/models", tags=["models"])

    @router.get("/history", response_model=None)
    async def get_history(
        page: int = Query(1, ge=1, le=100, description="Requested page number"),
        size: int = Query(20, ge=1, le=100, description="Items per page"),
        registry: Sequence[RegistryRecord] = Depends(get_registry),
    ) -> dict:
        """Return a paginated slice of the model registry history."""

        history = get_model_history(registry, page=page, size=size)
        return history.to_dict()
else:  # pragma: no cover - runtime fallback when FastAPI missing
    router = None

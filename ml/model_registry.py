"""Helpers for reading and paginating the simulated model registry."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class RegistryPage(Generic[T]):
    """A single page of registry results with pagination metadata."""

    items: List[T]
    total: int
    page: int
    size: int


class ModelRegistry(Generic[T]):
    """In-memory view of registry records with pagination helpers."""

    def __init__(self, records: Sequence[T] | None = None) -> None:
        self._records: List[T] = list(records or [])

    def paginate(self, *, page: int = 1, size: int = 20) -> RegistryPage[T]:
        """Return a paginated slice of the registry."""

        if page < 1:
            raise ValueError("page must be greater than or equal to 1")
        if size < 1:
            raise ValueError("size must be greater than or equal to 1")

        total = len(self._records)
        start = (page - 1) * size
        end = start + size
        items = self._records[start:end]
        return RegistryPage(items=items, total=total, page=page, size=size)

    def __len__(self) -> int:  # pragma: no cover - convenience helper
        return len(self._records)

    def __iter__(self):  # pragma: no cover - convenience helper
        return iter(self._records)

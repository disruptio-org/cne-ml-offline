"""Model service helpers for registry pagination."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Mapping, Sequence, Union

from ..schemas.models import ModelHistory, ModelInfo

RegistryRecord = Union[ModelInfo, Mapping[str, object]]

_DEFAULT_REGISTRY_PATH = Path(os.environ.get("CNE_MODEL_REGISTRY", "data/models/registry.json"))


def load_registry(path: Union[str, os.PathLike[str], None] = None) -> Sequence[RegistryRecord]:
    """Load registry records from disk.

    The registry is expected to be stored as a JSON list. Missing files yield an empty
    list to make the API resilient in development environments.
    """

    registry_path = Path(path) if path is not None else _DEFAULT_REGISTRY_PATH
    if not registry_path.exists():
        return []

    with registry_path.open("r", encoding="utf-8") as stream:
        payload = json.load(stream)

    if not isinstance(payload, list):
        raise ValueError("Model registry must contain a list of records")
    return payload


def _coerce_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        normalised = value.replace("Z", "+00:00") if value.endswith("Z") else value
        try:
            return datetime.fromisoformat(normalised)
        except ValueError as exc:  # pragma: no cover - invalid persisted data
            raise ValueError(f"Invalid ISO datetime string: {value}") from exc
    raise TypeError("Model registry record is missing a valid 'created_at' value")


def _coerce_metrics(value: object) -> Mapping[str, float] | None:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError("Model registry metrics must be a mapping if provided")


def _normalise_record(record: RegistryRecord) -> ModelInfo:
    if isinstance(record, ModelInfo):
        return record
    version = record.get("version") if isinstance(record, Mapping) else None
    created_at = record.get("created_at") if isinstance(record, Mapping) else None
    metrics = record.get("metrics") if isinstance(record, Mapping) else None
    if version is None:
        raise KeyError("Model registry record missing 'version'")
    if created_at is None:
        raise KeyError("Model registry record missing 'created_at'")
    return ModelInfo(
        version=str(version),
        created_at=_coerce_datetime(created_at),
        metrics=_coerce_metrics(metrics),
    )


def get_history(
    registry: Sequence[RegistryRecord],
    *,
    page: int = 1,
    size: int = 20,
) -> ModelHistory:
    """Return paginated history information for models in the registry."""

    if page < 1:
        raise ValueError("page must be greater than or equal to 1")
    if size < 1:
        raise ValueError("size must be greater than or equal to 1")

    normalised: List[ModelInfo] = [_normalise_record(record) for record in registry]
    total = len(normalised)
    start = (page - 1) * size
    end = start + size
    items = normalised[start:end]
    return ModelHistory(page=page, size=size, total=total, items=items)

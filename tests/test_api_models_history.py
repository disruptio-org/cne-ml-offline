from __future__ import annotations

from datetime import datetime, timezone
from typing import List

import pytest

from api.app.schemas.models import ModelInfo
from api.app.services.models import get_history


def _build_records(count: int) -> List[ModelInfo]:
    base = datetime(2024, 1, 1, tzinfo=timezone.utc)
    records: List[ModelInfo] = []
    for index in range(count):
        records.append(
            ModelInfo(
                version=f"model-{index}",
                created_at=base.replace(day=min(base.day + index, 28)),
                metrics={"acc": 0.9 + index * 0.01},
            )
        )
    return records


def test_get_history_paginates_records():
    records = _build_records(5)

    history = get_history(records, page=2, size=2)

    assert history.page == 2
    assert history.size == 2
    assert history.total == 5
    assert [item.version for item in history.items] == ["model-2", "model-3"]


def test_history_route_uses_pagination():
    pytest.importorskip("fastapi", reason="FastAPI not installed")
    from fastapi.testclient import TestClient

    from api.app.main import app
    from api.app.routes import models as models_routes

    records = [
        {
            "version": "parser-v1",
            "created_at": datetime(2024, 1, 1, tzinfo=timezone.utc).isoformat(),
            "metrics": {"f1": 0.9},
        },
        {
            "version": "parser-v2",
            "created_at": datetime(2024, 1, 2, tzinfo=timezone.utc).isoformat(),
            "metrics": {"f1": 0.91},
        },
        {
            "version": "parser-v3",
            "created_at": datetime(2024, 1, 3, tzinfo=timezone.utc).isoformat(),
            "metrics": {"f1": 0.92},
        },
    ]

    def override_registry():
        return records

    app.dependency_overrides[models_routes.get_registry] = override_registry
    client = TestClient(app)
    response = client.get("/api/models/history", params={"page": 2, "size": 1})
    app.dependency_overrides.pop(models_routes.get_registry, None)

    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 2
    assert payload["size"] == 1
    assert payload["total"] == len(records)
    assert [item["version"] for item in payload["items"]] == ["parser-v2"]

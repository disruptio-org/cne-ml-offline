import pytest

from api.app.schemas.jobs import JobState as ApiJobState, JobStatus
from api.app.services.jobs import build_job_stats
from worker.src.storage import JobState, JobStorage

try:  # pragma: no cover - optional FastAPI dependency
    from fastapi.testclient import TestClient
except ModuleNotFoundError:  # pragma: no cover - used for skipping API-only tests
    TestClient = None  # type: ignore[assignment]


def test_job_status_payload_includes_ocr_conf_mean(tmp_path):
    storage = JobStorage(tmp_path)
    job_id = "job-test"
    input_file = tmp_path / "sample.pdf"
    input_file.write_bytes(b"pdf")

    storage.ensure(job_id, [input_file])

    stats = {
        "rows_total": 2,
        "rows_ok": 1,
        "rows_warn": 1,
        "rows_err": 0,
        "ocr_conf_mean": 0.85,
    }

    metadata = storage.mark_state(
        job_id,
        JobState.ready,
        csv_path=str(tmp_path / "processed" / job_id / "listas_job-test.csv"),
        pages=1,
        stats=stats,
    )

    reloaded = storage.load(job_id)
    assert reloaded.stats["ocr_conf_mean"] == stats["ocr_conf_mean"]
    assert isinstance(reloaded.stats["ocr_conf_mean"], float)

    job_stats = build_job_stats(metadata)
    payload = JobStatus(
        job_id=metadata.job_id,
        state=ApiJobState(metadata.state.value),
        created_at=metadata.created_at,
        updated_at=metadata.updated_at,
        input_files=metadata.input_files,
        pages=metadata.pages,
        stats=job_stats,
        error=metadata.error,
    ).to_dict()

    assert payload["stats"]["ocr_conf_mean"] == stats["ocr_conf_mean"]


@pytest.mark.skipif(TestClient is None, reason="FastAPI is not available")
def test_api_job_endpoint_includes_ocr_conf_mean(tmp_path, monkeypatch):
    monkeypatch.setenv("CNE_DATA_DIR", str(tmp_path))
    storage = JobStorage(tmp_path)
    job_id = "job-endpoint"
    input_file = tmp_path / "input.pdf"
    input_file.write_bytes(b"pdf")

    storage.ensure(job_id, [input_file])
    stats = {
        "rows_total": 5,
        "rows_ok": 3,
        "rows_warn": 2,
        "rows_err": 0,
        "ocr_conf_mean": 0.73,
    }
    storage.mark_state(
        job_id,
        JobState.ready,
        csv_path=str(tmp_path / "processed" / job_id / f"listas_{job_id}.csv"),
        pages=2,
        stats=stats,
    )

    from api.app.main import app

    client = TestClient(app)
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["stats"]["ocr_conf_mean"] == pytest.approx(stats["ocr_conf_mean"])

"""High-level orchestration of the candidate list processing pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

from . import extractor, normalizer, ocr_stub, renderer, segmenter, validator, writer
from .storage import JobState, JobStorage
from .types import PipelineResult


def process_job(
    job_id: str,
    files: Sequence[Path],
    *,
    base_dir: Optional[Path] = None,
    storage: Optional[JobStorage] = None,
) -> PipelineResult:
    """Run the full pipeline for ``job_id`` and persist artefacts."""

    base = Path(base_dir or Path("data")).resolve()
    store = storage or JobStorage(base)
    input_paths = [Path(path).resolve() for path in files]

    store.ensure(job_id, input_paths)
    store.mark_state(job_id, JobState.processing, error=None)

    try:
        artifacts = renderer.render_documents(job_id, input_paths)
        pages = ocr_stub.run_ocr(job_id, artifacts)
        ocr_conf_mean = None
        if pages:
            ocr_conf_mean = round(
                sum(page.confidence for page in pages) / len(pages),
                4,
            )
        segments = segmenter.segment_pages(pages)
        raw_rows = extractor.extract_candidates(segments)
        normalized_rows = normalizer.normalize_rows(raw_rows)
        validated_rows = validator.validate_rows(normalized_rows)
        summary = validator.summarise_validation(
            validated_rows, ocr_conf_mean=ocr_conf_mean
        )

        csv_path, _meta_path = writer.write_outputs(job_id, validated_rows, summary, base)

        store.mark_state(
            job_id,
            JobState.ready,
            csv_path=str(csv_path),
            pages=len(pages),
            stats=summary,
        )
    except Exception as exc:  # pragma: no cover - defensive safeguard
        store.mark_state(job_id, JobState.failed, error=str(exc))
        raise

    return PipelineResult(
        job_id=job_id,
        csv_path=csv_path,
        rows_total=summary["rows_total"],
        rows_ok=summary["rows_ok"],
        rows_warn=summary["rows_warn"],
        rows_err=summary["rows_err"],
        pages_processed=len(pages),
        ocr_conf_mean=summary.get("ocr_conf_mean"),
    )

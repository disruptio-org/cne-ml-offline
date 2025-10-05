"""Input rendering stage (detect file types and produce artifacts)."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .types import DocumentArtifact

_SUPPORTED_MEDIA = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".md": "text/markdown",
}

_DEFAULT_MEDIA = "application/octet-stream"


def render_documents(job_id: str, files: Iterable[Path]) -> List[DocumentArtifact]:
    """Return lightweight artifacts with detected media types."""

    artifacts: List[DocumentArtifact] = []
    for path in files:
        suffix = path.suffix.lower()
        media_type = _SUPPORTED_MEDIA.get(suffix, _DEFAULT_MEDIA)
        artifacts.append(DocumentArtifact(job_id=job_id, source_path=Path(path), media_type=media_type))
    return artifacts

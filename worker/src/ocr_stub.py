"""Stub OCR implementation to keep the pipeline offline friendly."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .types import DocumentArtifact, OCRPage

_TEXTUAL_SUFFIXES = {".txt", ".csv", ".md", ".json"}


def _confidence_for_suffix(suffix: str) -> float:
    if suffix in _TEXTUAL_SUFFIXES:
        return 0.99
    if suffix == ".pdf":
        return 0.93
    if suffix in {".docx", ".xlsx"}:
        return 0.9
    return 0.75


def _read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")
    except OSError:
        return ""


def _stub_text(job_id: str, artifact: DocumentArtifact) -> str:
    base = artifact.source_path.stem.upper() or job_id[:6].upper()
    return (
        f"DTMNFR=150800;ORGAO=AM;SIGLA=PS;TIPO=2;NUM_ORDEM=1;NOME_LISTA=Lista {base};"
        "NOME_CANDIDATO=Candidato Efetivo;PARTIDO_PROPONENTE=PS;INDEPENDENTE=0\n"
        f"DTMNFR=150800;ORGAO=AM;SIGLA=PS;TIPO=3;NUM_ORDEM=1;NOME_LISTA=Lista {base};"
        "NOME_CANDIDATO=Candidato Suplente;PARTIDO_PROPONENTE=PS;INDEPENDENTE=0"
    )


def run_ocr(job_id: str, artifacts: Iterable[DocumentArtifact]) -> List[OCRPage]:
    pages: List[OCRPage] = []
    for artifact in artifacts:
        suffix = artifact.source_path.suffix.lower()
        if suffix in _TEXTUAL_SUFFIXES:
            text = _read_text_file(artifact.source_path)
        elif suffix == ".pdf":
            text = _stub_text(job_id, artifact)
        elif suffix in {".docx", ".xlsx"}:
            text = _stub_text(job_id, artifact)
        else:
            text = _read_text_file(artifact.source_path)
        confidence = _confidence_for_suffix(suffix)
        pages.append(
            OCRPage(
                document_id=str(artifact.source_path),
                page_number=1,
                text=text.strip(),
                confidence=confidence,
            )
        )
    return pages

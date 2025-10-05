"""Shared dataclasses used across the processing pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional


@dataclass
class DocumentArtifact:
    """Represents an input document to be processed."""

    job_id: str
    source_path: Path
    media_type: str


@dataclass
class OCRPage:
    """Result of OCR or text extraction for a single page."""

    document_id: str
    page_number: int
    text: str


@dataclass
class CandidateRow:
    """Structured representation of a candidate list entry."""

    DTMNFR: str
    ORGAO: str
    TIPO: str
    SIGLA: str
    SIMBOLO: Optional[str]
    NOME_LISTA: Optional[str]
    NUM_ORDEM: int
    NOME_CANDIDATO: str
    PARTIDO_PROPONENTE: Optional[str]
    INDEPENDENTE: Optional[str]
    validation: Dict[str, str] = field(default_factory=dict)


@dataclass
class PipelineResult:
    """High-level summary returned after processing a job."""

    job_id: str
    csv_path: Path
    rows_total: int
    rows_ok: int
    rows_warn: int
    rows_err: int
    pages_processed: int
    ocr_conf_mean: Optional[float] = None

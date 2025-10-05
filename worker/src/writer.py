"""CSV writer helpers for the pipeline."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, Tuple

from .types import CandidateRow

CSV_COLUMNS = [
    "DTMNFR",
    "ORGAO",
    "TIPO",
    "SIGLA",
    "SIMBOLO",
    "NOME_LISTA",
    "NUM_ORDEM",
    "NOME_CANDIDATO",
    "PARTIDO_PROPONENTE",
    "INDEPENDENTE",
]


def write_outputs(
    job_id: str,
    rows: Iterable[CandidateRow],
    summary: Dict[str, int],
    base_dir: Path,
) -> Tuple[Path, Path]:
    processed_dir = (base_dir / "processed" / job_id).resolve()
    processed_dir.mkdir(parents=True, exist_ok=True)
    csv_path = processed_dir / f"listas_{job_id}.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(CSV_COLUMNS)
        for row in rows:
            writer.writerow([
                row.DTMNFR,
                row.ORGAO,
                row.TIPO,
                row.SIGLA,
                row.SIMBOLO or "",
                row.NOME_LISTA or "",
                row.NUM_ORDEM,
                row.NOME_CANDIDATO,
                row.PARTIDO_PROPONENTE or "",
                row.INDEPENDENTE or "",
            ])
    meta_path = processed_dir / "meta.json"
    payload = {
        "job_id": job_id,
        "rows_total": summary.get("rows_total", 0),
        "rows_ok": summary.get("rows_ok", 0),
        "rows_warn": summary.get("rows_warn", 0),
        "rows_err": summary.get("rows_err", 0),
    }
    meta_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return csv_path, meta_path

"""CSV writer helpers for the pipeline."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, Tuple, Union

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
    summary: Dict[str, Union[int, float, None]],
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
    payload: Dict[str, Union[int, float, None]] = {
        "job_id": job_id,
        "rows_total": summary.get("rows_total", 0),
        "rows_ok": summary.get("rows_ok", 0),
        "rows_warn": summary.get("rows_warn", 0),
        "rows_err": summary.get("rows_err", 0),
    }
    if "ocr_conf_mean" in summary:
        payload["ocr_conf_mean"] = summary.get("ocr_conf_mean")
    meta_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    preview_path = processed_dir / "preview.json"
    preview_payload: Dict[str, object]
    if preview_path.exists():
        try:
            preview_payload = json.loads(preview_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            preview_payload = {}
    else:
        preview_payload = {}
    stats_section = dict(preview_payload.get("stats", {}))  # type: ignore[arg-type]
    for key in ("rows_total", "rows_ok", "rows_warn", "rows_err", "ocr_conf_mean"):
        if key in summary:
            stats_section[key] = summary.get(key)
    preview_payload["stats"] = stats_section
    preview_path.write_text(
        json.dumps(preview_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return csv_path, meta_path

"""Validation logic for candidate rows."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple, Union

from .types import CandidateRow

_ALLOWED_ORGAOS = {"AM", "CM", "AF"}
_ALLOWED_TIPOS = {"2", "3"}
_ALLOWED_SIGLAS = {
    "PS",
    "PSD",
    "PSD/CDS",
    "CDS",
    "CDU",
    "BE",
    "IL",
    "LIVRE",
    "PAN",
    "CHEGA",
    "IND",
}
_ALLOWED_INDEPENDENTE = {"0", "1", "S", "N", "SIM", "NAO"}

_VALIDATION_OK = "OK"
_VALIDATION_WARN = "AVISO"
_VALIDATION_ERR = "ERRO"

_SORT_KEY_ORDER = ("DTMNFR", "ORGAO", "SIGLA", "NOME_LISTA", "TIPO", "NUM_ORDEM")


def _row_sort_key(row: CandidateRow) -> Tuple:
    return tuple(
        getattr(row, field)
        if field != "NUM_ORDEM"
        else int(getattr(row, field))
        for field in _SORT_KEY_ORDER
    )


def validate_rows(rows: Iterable[CandidateRow]) -> List[CandidateRow]:
    validated: List[CandidateRow] = []
    for row in rows:
        row.validation.setdefault("DTMNFR", _VALIDATION_OK)
        row.validation.setdefault("ORGAO", _VALIDATION_OK)
        row.validation.setdefault("TIPO", _VALIDATION_OK)
        row.validation.setdefault("SIGLA", _VALIDATION_OK)
        row.validation.setdefault("NOME_LISTA", _VALIDATION_OK)
        row.validation.setdefault("NUM_ORDEM", _VALIDATION_OK)
        row.validation.setdefault("NOME_CANDIDATO", _VALIDATION_OK)
        row.validation.setdefault("PARTIDO_PROPONENTE", _VALIDATION_OK)
        row.validation.setdefault("INDEPENDENTE", _VALIDATION_OK)

        if row.DTMNFR and (len(row.DTMNFR) != 6 or not row.DTMNFR.isdigit()):
            row.validation["DTMNFR"] = _VALIDATION_WARN
            row.DTMNFR = row.DTMNFR.zfill(6)[:6]

        if row.ORGAO not in _ALLOWED_ORGAOS:
            row.validation["ORGAO"] = _VALIDATION_WARN
            row.ORGAO = "AM"

        if row.TIPO not in _ALLOWED_TIPOS:
            row.validation["TIPO"] = _VALIDATION_WARN
            row.TIPO = "2"

        if row.SIGLA not in _ALLOWED_SIGLAS:
            row.validation["SIGLA"] = _VALIDATION_ERR

        if not row.NOME_LISTA:
            row.validation["NOME_LISTA"] = _VALIDATION_WARN
            row.NOME_LISTA = f"LISTA {row.SIGLA or 'IND'}"

        if row.INDEPENDENTE.upper() not in _ALLOWED_INDEPENDENTE:
            row.validation["INDEPENDENTE"] = _VALIDATION_WARN
            row.INDEPENDENTE = "0"

        validated.append(row)

    validated.sort(key=_row_sort_key)

    grouped: Dict[Tuple[str, str, str, str, str], List[CandidateRow]] = defaultdict(list)
    for row in validated:
        key = (row.DTMNFR, row.ORGAO, row.SIGLA, row.NOME_LISTA or "", row.TIPO)
        grouped[key].append(row)

    for rows_group in grouped.values():
        for index, row in enumerate(rows_group, start=1):
            if row.NUM_ORDEM != index:
                row.validation["NUM_ORDEM"] = _VALIDATION_WARN
                row.NUM_ORDEM = index
            else:
                row.validation.setdefault("NUM_ORDEM", _VALIDATION_OK)

    validated.sort(key=_row_sort_key)
    return validated


def summarise_validation(rows: Iterable[CandidateRow]) -> Dict[str, Union[int, float, None]]:
    summary: Dict[str, Union[int, float, None]] = {
        "rows_total": 0,
        "rows_ok": 0,
        "rows_warn": 0,
        "rows_err": 0,
        "ocr_conf_mean": None,
    }
    severity = {_VALIDATION_OK: 0, _VALIDATION_WARN: 1, _VALIDATION_ERR: 2}
    confidence_scale = {0: 1.0, 1: 0.7, 2: 0.3}
    confidence_total = 0.0
    confidence_count = 0
    for row in rows:
        summary["rows_total"] += 1
        worst = 0
        for flag in row.validation.values():
            worst = max(worst, severity.get(flag, 0))
        if worst == 0:
            summary["rows_ok"] += 1
        elif worst == 1:
            summary["rows_warn"] += 1
        else:
            summary["rows_err"] += 1
        confidence_total += confidence_scale.get(worst, 0.0)
        confidence_count += 1
    if confidence_count:
        summary["ocr_conf_mean"] = round(confidence_total / confidence_count, 4)
    return summary

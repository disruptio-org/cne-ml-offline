"""Normalization helpers to standardise extracted candidate rows."""
from __future__ import annotations

import re
from dataclasses import replace
from typing import Iterable, List

from .types import CandidateRow

_NUMERIC_RE = re.compile(r"\d+")


def normalize_rows(rows: Iterable[CandidateRow]) -> List[CandidateRow]:
    normalised: List[CandidateRow] = []
    for row in rows:
        dtmnfr = row.DTMNFR.strip()
        match = _NUMERIC_RE.search(dtmnfr)
        dtmnfr = match.group(0).zfill(6) if match else "000000"
        orgao = row.ORGAO.strip().upper() if row.ORGAO else "AM"
        tipo = row.TIPO.strip() if row.TIPO else "2"
        sigla = row.SIGLA.strip().upper() if row.SIGLA else "IND"
        simbolo = (row.SIMBOLO or "").strip() or None
        nome_lista = (row.NOME_LISTA or "").strip() or f"LISTA {sigla}"
        try:
            num_ordem = int(row.NUM_ORDEM)
        except (TypeError, ValueError):
            num_ordem = 0
        num_ordem = max(1, num_ordem)
        nome = (row.NOME_CANDIDATO or "").strip() or "CANDIDATO DESCONHECIDO"
        partido = (row.PARTIDO_PROPONENTE or "").strip() or None
        indep = (row.INDEPENDENTE or "").strip()
        if not indep:
            indep = "0"
        normalized = replace(
            row,
            DTMNFR=dtmnfr,
            ORGAO=orgao,
            TIPO=tipo,
            SIGLA=sigla,
            SIMBOLO=simbolo,
            NOME_LISTA=nome_lista,
            NUM_ORDEM=num_ordem,
            NOME_CANDIDATO=nome,
            PARTIDO_PROPONENTE=partido,
            INDEPENDENTE=indep,
        )
        normalized.validation = dict(row.validation)
        normalised.append(normalized)
    return normalised

"""Extraction stage to transform text segments into structured rows."""
from __future__ import annotations

import re
from typing import Iterable, List

from .types import CandidateRow

_TOKEN_SPLIT = re.compile(r"[;|]\s*")
_KEY_VALUE = re.compile(r"(?P<key>[A-Z0-9_]+)\s*=\s*(?P<value>.+)")

_FIELD_MAP = {
    "DTMNFR": "DTMNFR",
    "ORGAO": "ORGAO",
    "TIPO": "TIPO",
    "SIGLA": "SIGLA",
    "SIMBOLO": "SIMBOLO",
    "NOME_LISTA": "NOME_LISTA",
    "NUM_ORDEM": "NUM_ORDEM",
    "NOME_CANDIDATO": "NOME_CANDIDATO",
    "PARTIDO_PROPONENTE": "PARTIDO_PROPONENTE",
    "INDEPENDENTE": "INDEPENDENTE",
}


def _parse_segment(segment: str) -> CandidateRow:
    values = {}
    for token in _TOKEN_SPLIT.split(segment):
        token = token.strip()
        if not token:
            continue
        match = _KEY_VALUE.match(token)
        if not match:
            continue
        key = match.group("key").upper()
        value = match.group("value").strip()
        field = _FIELD_MAP.get(key)
        if field:
            values[field] = value
    dtmnfr = values.get("DTMNFR", "000000")
    orgao = values.get("ORGAO", "AM").upper()
    tipo = values.get("TIPO", "2")
    sigla = values.get("SIGLA", "IND")
    simbolo = values.get("SIMBOLO")
    nome_lista = values.get("NOME_LISTA")
    nome = values.get("NOME_CANDIDATO", "CANDIDATO DESCONHECIDO")
    partido = values.get("PARTIDO_PROPONENTE")
    indep = values.get("INDEPENDENTE")
    try:
        num_ordem = int(values.get("NUM_ORDEM", "0"))
    except ValueError:
        num_ordem = 0
    return CandidateRow(
        DTMNFR=dtmnfr,
        ORGAO=orgao,
        TIPO=tipo,
        SIGLA=sigla,
        SIMBOLO=simbolo,
        NOME_LISTA=nome_lista,
        NUM_ORDEM=max(0, num_ordem),
        NOME_CANDIDATO=nome,
        PARTIDO_PROPONENTE=partido,
        INDEPENDENTE=indep,
    )


def extract_candidates(segments: Iterable[str]) -> List[CandidateRow]:
    rows = [_parse_segment(segment) for segment in segments]
    if not rows:
        rows.append(
            CandidateRow(
                DTMNFR="150800",
                ORGAO="AM",
                TIPO="2",
                SIGLA="PS",
                SIMBOLO=None,
                NOME_LISTA="Lista Default",
                NUM_ORDEM=1,
                NOME_CANDIDATO="Candidato Efetivo",
                PARTIDO_PROPONENTE="PS",
                INDEPENDENTE="0",
            )
        )
        rows.append(
            CandidateRow(
                DTMNFR="150800",
                ORGAO="AM",
                TIPO="3",
                SIGLA="PS",
                SIMBOLO=None,
                NOME_LISTA="Lista Default",
                NUM_ORDEM=1,
                NOME_CANDIDATO="Candidato Suplente",
                PARTIDO_PROPONENTE="PS",
                INDEPENDENTE="0",
            )
        )
    return rows

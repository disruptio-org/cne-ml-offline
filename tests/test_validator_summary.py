from worker.src.types import CandidateRow
from worker.src.validator import validate_rows, summarise_validation


def make_row(**overrides):
    defaults = dict(
        DTMNFR="150800",
        ORGAO="AM",
        TIPO="2",
        SIGLA="PS",
        SIMBOLO="",
        NOME_LISTA="Lista",
        NUM_ORDEM=1,
        NOME_CANDIDATO="Nome",
        PARTIDO_PROPONENTE="PS",
        INDEPENDENTE="0",
    )
    defaults.update(overrides)
    return CandidateRow(**defaults)


def test_summary_includes_ocr_conf_mean():
    rows = [
        make_row(),
        make_row(DTMNFR="1508", NUM_ORDEM=2),  # triggers warning fixes
        make_row(SIGLA="XXX"),  # triggers error
    ]

    validated = validate_rows(rows)
    summary = summarise_validation(validated, ocr_conf_mean=0.88)

    assert summary["rows_total"] == 3
    assert summary["rows_ok"] == 1
    assert summary["rows_warn"] == 1
    assert summary["rows_err"] == 1
    assert "ocr_conf_mean" in summary
    assert summary["ocr_conf_mean"] == 0.88


def test_summary_fallback_computes_confidence_when_missing():
    rows = [make_row(), make_row(SIGLA="XXX")]
    validated = validate_rows(rows)

    summary = summarise_validation(validated)

    assert summary["ocr_conf_mean"] is not None
    assert 0 < summary["ocr_conf_mean"] < 1

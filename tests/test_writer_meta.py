import json

from worker.src.types import CandidateRow
from worker.src.validator import summarise_validation, validate_rows
from worker.src.writer import write_outputs


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


def test_meta_file_includes_ocr_conf_mean(tmp_path):
    rows = validate_rows([make_row(), make_row(SIGLA="XXX")])
    summary = summarise_validation(rows)

    csv_path, meta_path = write_outputs("job1", rows, summary, tmp_path)

    assert csv_path.exists()
    data = json.loads(meta_path.read_text(encoding="utf-8"))
    assert "ocr_conf_mean" in data
    assert data["ocr_conf_mean"] == summary["ocr_conf_mean"]

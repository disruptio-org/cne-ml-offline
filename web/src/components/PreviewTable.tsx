import ValidationIcon from "./ValidationIcon";
import { PreviewRow } from "../types";

interface Props {
  rows: PreviewRow[];
}

const HEADERS = [
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
];

function PreviewTable({ rows }: Props) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            {HEADERS.map((header) => (
              <th key={header}>{header}</th>
            ))}
            <th>Validações</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.DTMNFR}-${row.ORGAO}-${row.TIPO}-${row.NUM_ORDEM}-${index}`}>
              <td>{row.DTMNFR}</td>
              <td>{row.ORGAO}</td>
              <td>{row.TIPO}</td>
              <td>{row.SIGLA}</td>
              <td>{row.SIMBOLO ?? ""}</td>
              <td>{row.NOME_LISTA ?? ""}</td>
              <td>{row.NUM_ORDEM}</td>
              <td>{row.NOME_CANDIDATO}</td>
              <td>{row.PARTIDO_PROPONENTE ?? ""}</td>
              <td>{row.INDEPENDENTE ?? ""}</td>
              <td>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                  {Object.entries(row.__validation__).map(([key, value]) => (
                    <ValidationIcon key={key} value={value} />
                  ))}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PreviewTable;

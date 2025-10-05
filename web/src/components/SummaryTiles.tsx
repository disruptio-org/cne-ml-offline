import { PreviewRow } from "../types";
import { formatTipo } from "../utils/format";

interface Props {
  rows: PreviewRow[];
}

function buildSummary(rows: PreviewRow[]) {
  const totals: Record<string, number> = {};
  const byLista: Record<string, number> = {};

  rows.forEach((row) => {
    const tipoLabel = formatTipo(row.TIPO);
    totals[tipoLabel] = (totals[tipoLabel] ?? 0) + 1;

    const key = `${row.NOME_LISTA ?? "Sem nome"} (${formatTipo(row.TIPO)})`;
    byLista[key] = (byLista[key] ?? 0) + 1;
  });

  return { totals, byLista };
}

function SummaryTiles({ rows }: Props) {
  const summary = buildSummary(rows);
  if (rows.length === 0) {
    return <p>Sem dados disponíveis.</p>;
  }
  return (
    <div className="summary-grid">
      {Object.entries(summary.totals).map(([label, value]) => (
        <div key={label} className="summary-tile">
          <h4>{label}</h4>
          <span>{value}</span>
        </div>
      ))}
      {Object.entries(summary.byLista).map(([label, value]) => (
        <div key={label} className="summary-tile">
          <h4>{label}</h4>
          <span>{value}</span>
        </div>
      ))}
    </div>
  );
}

export default SummaryTiles;

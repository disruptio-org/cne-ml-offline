import { JobState } from "../types";

export function formatDate(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("pt-PT");
}

export function formatState(state: JobState): string {
  switch (state) {
    case "queued":
      return "Em fila";
    case "processing":
      return "A processar";
    case "ready":
      return "Pronto";
    case "approved":
      return "Aprovado";
    case "failed":
      return "Falhou";
    default:
      return state;
  }
}

export function formatTipo(tipo: string): string {
  if (tipo === "2") return "Efetivos";
  if (tipo === "3") return "Suplentes";
  return tipo;
}

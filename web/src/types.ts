export type JobState = "queued" | "processing" | "ready" | "approved" | "failed";

export interface JobStats {
  rows_total?: number;
  rows_ok?: number;
  rows_warn?: number;
  rows_err?: number;
  ocr_conf_mean?: number;
}

export interface JobStatus {
  job_id: string;
  state: JobState;
  created_at: string;
  updated_at: string;
  input_files: string[];
  pages?: number;
  stats?: JobStats;
}

export interface JobCreated {
  job_id: string;
  status: JobState;
}

export type ValidationFlag = "OK" | "AVISO" | "ERRO";

export interface PreviewRow {
  DTMNFR: string;
  ORGAO: "AM" | "CM" | "AF";
  TIPO: "2" | "3";
  SIGLA: string;
  SIMBOLO?: string | null;
  NOME_LISTA?: string | null;
  NUM_ORDEM: number;
  NOME_CANDIDATO: string;
  PARTIDO_PROPONENTE?: string | null;
  INDEPENDENTE?: string | null;
  __validation__: Record<string, ValidationFlag>;
}

export interface PreviewResponse {
  job_id: string;
  page: number;
  size: number;
  total: number;
  rows: PreviewRow[];
}

export interface ApproveResponse {
  job_id: string;
  status: string;
  dataset_path?: string;
}

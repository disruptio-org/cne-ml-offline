import { API_ROUTES } from "../config";
import { ApproveResponse, JobCreated, JobState, JobStatus, PreviewResponse } from "../types";

function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    return response.json().catch(() => ({})).then((payload) => {
      const error = payload?.error ?? response.statusText;
      const detail = payload?.detail;
      throw new Error(detail ? `${error}: ${detail}` : error);
    });
  }
  return response.json() as Promise<T>;
}

export async function createJob(file: File, inferOnly = false): Promise<JobCreated> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("infer_only", String(inferOnly));

  const response = await fetch(API_ROUTES.jobs, {
    method: "POST",
    body: formData,
  });

  return handleResponse<JobCreated>(response);
}

export async function getJob(jobId: string): Promise<JobStatus> {
  const response = await fetch(`${API_ROUTES.jobs}/${jobId}`);
  return handleResponse<JobStatus>(response);
}

export async function getJobPreview(jobId: string, page = 1, size = 200): Promise<PreviewResponse> {
  const response = await fetch(`${API_ROUTES.jobs}/${jobId}/preview?page=${page}&size=${size}`);
  return handleResponse<PreviewResponse>(response);
}

export async function downloadCsv(jobId: string): Promise<void> {
  const response = await fetch(`${API_ROUTES.jobs}/${jobId}/csv`);
  if (!response.ok) {
    await handleResponse(response);
    return;
  }
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  const filename = response.headers.get("Content-Disposition")?.match(/filename="?(.+?)"?$/i)?.[1] ?? `listas_${jobId}.csv`;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export async function approveJob(jobId: string, notes?: string): Promise<ApproveResponse> {
  const payload = notes ? { notes } : undefined;
  const response = await fetch(`${API_ROUTES.jobs}/${jobId}/approve`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  return handleResponse<ApproveResponse>(response);
}

export async function pollJobUntil(jobId: string, targetStates: JobState[], timeoutMs = 60000): Promise<JobStatus> {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const job = await getJob(jobId);
    if (targetStates.includes(job.state)) {
      return job;
    }
    await new Promise((resolve) => setTimeout(resolve, 1500));
  }
  throw new Error("Tempo limite atingido a aguardar processamento");
}

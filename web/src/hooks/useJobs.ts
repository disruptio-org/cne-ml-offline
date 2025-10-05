import { useCallback, useEffect, useMemo, useState } from "react";
import { getJob } from "../api/jobs";
import { JobState, JobStatus } from "../types";

const STORAGE_KEY = "cne-jobs";

function readStoredJobIds(): string[] {
  if (typeof window === "undefined") {
    return [];
  }
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return parsed.filter((value) => typeof value === "string");
    }
    return [];
  } catch (error) {
    console.warn("Erro ao ler jobs do storage", error);
    return [];
  }
}

function writeStoredJobIds(jobIds: string[]): void {
  if (typeof window === "undefined") {
    return;
  }
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(jobIds));
  } catch (error) {
    console.warn("Erro ao persistir jobs", error);
  }
}

export interface JobRecord extends JobStatus {
  lastChecked: number;
  isLoading: boolean;
  error?: string;
}

export function useJobs() {
  const [jobIds, setJobIds] = useState<string[]>(() => readStoredJobIds());
  const [jobs, setJobs] = useState<Record<string, JobRecord>>({});

  useEffect(() => {
    writeStoredJobIds(jobIds);
  }, [jobIds]);

  useEffect(() => {
    if (jobIds.length === 0) {
      setJobs({});
      return;
    }
    let cancelled = false;
    async function refreshStatus(jobId: string) {
      setJobs((prev) => ({
        ...prev,
        [jobId]: {
          ...(prev[jobId] ?? ({
            job_id: jobId,
            state: "queued" as JobState,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            input_files: [],
            lastChecked: Date.now(),
            isLoading: true,
          } as JobRecord)),
          isLoading: true,
          error: undefined,
        },
      }));
      try {
        const status = await getJob(jobId);
        if (cancelled) return;
        setJobs((prev) => ({
          ...prev,
          [jobId]: {
            ...status,
            lastChecked: Date.now(),
            isLoading: false,
          },
        }));
      } catch (error) {
        if (cancelled) return;
        setJobs((prev) => ({
          ...prev,
          [jobId]: {
            ...(prev[jobId] ?? ({
              job_id: jobId,
              state: "failed" as JobState,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              input_files: [],
              lastChecked: Date.now(),
              isLoading: false,
            } as JobRecord)),
            isLoading: false,
            lastChecked: Date.now(),
            error: error instanceof Error ? error.message : String(error),
          },
        }));
      }
    }

    jobIds.forEach((jobId) => {
      refreshStatus(jobId);
    });

    const interval = setInterval(() => {
      jobIds.forEach((jobId) => refreshStatus(jobId));
    }, 5000);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [jobIds]);

  const addJobId = useCallback((jobId: string) => {
    setJobIds((prev) => {
      if (prev.includes(jobId)) return prev;
      return [jobId, ...prev];
    });
  }, []);

  const removeJobId = useCallback((jobId: string) => {
    setJobIds((prev) => prev.filter((value) => value !== jobId));
    setJobs((prev) => {
      const copy = { ...prev };
      delete copy[jobId];
      return copy;
    });
  }, []);

  const sortedJobs = useMemo(() => {
    return jobIds
      .map((id) => jobs[id])
      .filter(Boolean)
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
  }, [jobIds, jobs]);

  return { jobIds, jobs, sortedJobs, addJobId, removeJobId };
}

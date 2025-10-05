import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { approveJob, downloadCsv, getJob, getJobPreview } from "../api/jobs";
import JobStatusBadge from "../components/JobStatusBadge";
import PdfPreviewPlaceholder from "../components/PdfPreviewPlaceholder";
import PreviewTable from "../components/PreviewTable";
import SummaryTiles from "../components/SummaryTiles";
import { useJobs } from "../hooks/useJobs";
import { PreviewRow } from "../types";
import { formatDate } from "../utils/format";

const REQUEST_SIZE = 500;
const PAGE_SIZE = 50;

function ResultPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const { jobs, addJobId } = useJobs();
  const [jobError, setJobError] = useState<string | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [isApproving, setApproving] = useState(false);
  const [allRows, setAllRows] = useState<PreviewRow[]>([]);
  const [page, setPage] = useState(1);
  const [isLoadingPreview, setLoadingPreview] = useState(false);
  const job = jobId ? jobs[jobId] : undefined;

  useEffect(() => {
    if (jobId) {
      addJobId(jobId);
      setPage(1);
    }
  }, [jobId, addJobId]);

  useEffect(() => {
    if (!jobId) return;
    let cancelled = false;
    async function loadJob() {
      try {
        await getJob(jobId);
        if (!cancelled) {
          setJobError(null);
        }
      } catch (error) {
        if (!cancelled) {
          setJobError(error instanceof Error ? error.message : String(error));
        }
      }
    }
    loadJob();
    return () => {
      cancelled = true;
    };
  }, [jobId]);

  useEffect(() => {
    if (!jobId) return;
    let cancelled = false;
    async function loadAllPreviewRows() {
      setLoadingPreview(true);
      try {
        const aggregated: PreviewRow[] = [];
        let currentPage = 1;
        let total = 0;
        while (true) {
          const preview = await getJobPreview(jobId, currentPage, REQUEST_SIZE);
          if (cancelled) return;
          aggregated.push(...preview.rows);
          total = preview.total;
          if (aggregated.length >= total || preview.rows.length === 0) {
            break;
          }
          currentPage += 1;
        }
        setAllRows(aggregated);
        setPreviewError(null);
      } catch (error) {
        if (!cancelled) {
          setPreviewError(error instanceof Error ? error.message : String(error));
        }
      } finally {
        if (!cancelled) {
          setLoadingPreview(false);
        }
      }
    }
    loadAllPreviewRows();
    return () => {
      cancelled = true;
    };
  }, [jobId]);

  const totalRows = allRows.length;
  const totalPages = useMemo(() => {
    return totalRows === 0 ? 1 : Math.max(1, Math.ceil(totalRows / PAGE_SIZE));
  }, [totalRows]);

  const pageRows = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return allRows.slice(start, start + PAGE_SIZE);
  }, [allRows, page]);

  useEffect(() => {
    if (page > totalPages) {
      setPage(totalPages);
    }
  }, [totalPages, page]);

  const handleDownload = useCallback(async () => {
    if (!jobId) return;
    try {
      await downloadCsv(jobId);
    } catch (error) {
      alert(error instanceof Error ? error.message : String(error));
    }
  }, [jobId]);

  const handleApprove = useCallback(async () => {
    if (!jobId) return;
    setApproving(true);
    try {
      const response = await approveJob(jobId);
      alert(`Job aprovado! Dados em ${response.dataset_path ?? "data/approved"}`);
      navigate("/jobs");
    } catch (error) {
      alert(error instanceof Error ? error.message : String(error));
    } finally {
      setApproving(false);
    }
  }, [jobId, navigate]);

  if (!jobId) {
    return <p>Job inválido.</p>;
  }

  return (
    <div>
      <div className="card">
        <button className="secondary" onClick={() => navigate(-1)} style={{ marginBottom: "16px" }}>
          ← Voltar
        </button>
        <h2>Job {jobId}</h2>
        {jobError && <p style={{ color: "#b91c1c" }}>{jobError}</p>}
        {job ? (
          <div className="status-grid">
            <div className="status-card">
              <h3>Estado</h3>
              <p>
                <JobStatusBadge state={job.state} />
              </p>
            </div>
            <div className="status-card">
              <h3>Criado</h3>
              <p>{formatDate(job.created_at)}</p>
            </div>
            <div className="status-card">
              <h3>Atualizado</h3>
              <p>{formatDate(job.updated_at)}</p>
            </div>
            <div className="status-card">
              <h3>Ficheiros</h3>
              <p>{job.input_files.join(", ") || "n/a"}</p>
            </div>
            {job.stats && (
              <div className="status-card">
                <h3>Resumo</h3>
                <p>
                  {job.stats.rows_total ?? 0} linhas | OK {job.stats.rows_ok ?? 0} · AVISO {job.stats.rows_warn ?? 0} · ERRO {job.stats.rows_err ?? 0}
                </p>
              </div>
            )}
          </div>
        ) : (
          <p>A carregar estado do job...</p>
        )}
      </div>

      <div className="card">
        <h2>Pré-visualização</h2>
        <PdfPreviewPlaceholder jobId={jobId} fileName={job?.input_files[0]} />
        <div className="controls">
          <button onClick={handleDownload}>Descarregar CSV</button>
          <button onClick={handleApprove} disabled={isApproving || (job && job.state === "approved")}>Aprovar</button>
        </div>
      </div>

      <div className="card">
        <h2>Tabela de candidatos</h2>
        {isLoadingPreview && <p>A carregar pré-visualização...</p>}
        {previewError && <p style={{ color: "#b91c1c" }}>{previewError}</p>}
        {!isLoadingPreview && !previewError && pageRows.length === 0 ? <p>Sem linhas para mostrar.</p> : <PreviewTable rows={pageRows} />}
        <div className="controls" style={{ justifyContent: "space-between" }}>
          <div>
            <button className="secondary" disabled={page <= 1} onClick={() => setPage((value) => Math.max(1, value - 1))}>
              Página anterior
            </button>
            <button
              className="secondary"
              disabled={page >= totalPages}
              onClick={() => setPage((value) => Math.min(totalPages, value + 1))}
            >
              Próxima página
            </button>
          </div>
          <span>
            Página {page} de {totalPages} ({totalRows} linhas)
          </span>
        </div>
      </div>

      <div className="card">
        <h2>Resumo por tipo e lista</h2>
        <SummaryTiles rows={allRows} />
      </div>
    </div>
  );
}

export default ResultPage;

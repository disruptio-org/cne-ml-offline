import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";

import { createJob } from "../api/jobs";
import JobStatusBadge from "../components/JobStatusBadge";
import UploadDropzone from "../components/UploadDropzone";
import { useJobs } from "../hooks/useJobs";
import { formatDate } from "../utils/format";

function UploadPage() {
  const navigate = useNavigate();
  const { sortedJobs, addJobId } = useJobs();
  const [isUploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = useCallback(
    async (files: FileList | File[]) => {
      setError(null);
      const fileArray = Array.isArray(files) ? files : Array.from(files ?? []);
      if (!fileArray.length) return;

      setUploading(true);
      try {
        for (const file of fileArray) {
          const result = await createJob(file);
          addJobId(result.job_id);
          navigate(`/jobs/${result.job_id}`);
        }
      } catch (uploadError) {
        setError(uploadError instanceof Error ? uploadError.message : String(uploadError));
      } finally {
        setUploading(false);
      }
    },
    [addJobId, navigate]
  );

  return (
    <div>
      <div className="card">
        <h2>Upload de documentos</h2>
        <p>Arraste e largue ficheiros PDF, Word ou Excel para iniciar um novo processamento offline.</p>
        <UploadDropzone onFiles={handleFiles}>
          <strong>{isUploading ? "A enviar ficheiro..." : "Clique ou largue ficheiros aqui"}</strong>
          <p style={{ marginTop: "12px" }}>Formatos suportados: PDF, DOCX, XLSX, ZIP</p>
        </UploadDropzone>
        {error && <p style={{ color: "#b91c1c", marginTop: "16px" }}>{error}</p>}
      </div>

      <div className="card">
        <h2>Jobs recentes</h2>
        {sortedJobs.length === 0 ? (
          <p>Ainda não existem jobs nesta sessão.</p>
        ) : (
          <div className="table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Job</th>
                  <th>Estado</th>
                  <th>Criado</th>
                  <th>Atualizado</th>
                </tr>
              </thead>
              <tbody>
                {sortedJobs.map((job) => (
                  <tr
                    key={job.job_id}
                    onClick={() => navigate(`/jobs/${job.job_id}`)}
                    style={{ cursor: "pointer" }}
                  >
                    <td>{job.job_id}</td>
                    <td>
                      <JobStatusBadge state={job.state} />
                    </td>
                    <td>{formatDate(job.created_at)}</td>
                    <td>{formatDate(job.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadPage;

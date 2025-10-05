import { useMemo } from "react";
import { useNavigate } from "react-router-dom";

import JobStatusBadge from "../components/JobStatusBadge";
import { useJobs } from "../hooks/useJobs";
import { JobState } from "../types";
import { formatDate, formatState } from "../utils/format";

const ORDER: JobState[] = ["processing", "ready", "approved", "queued", "failed"];

function HistoryPage() {
  const { sortedJobs } = useJobs();
  const navigate = useNavigate();

  const grouped = useMemo(() => {
    const buckets: Record<JobState, typeof sortedJobs> = {
      queued: [],
      processing: [],
      ready: [],
      approved: [],
      failed: [],
    };

    sortedJobs.forEach((job) => {
      buckets[job.state].push(job);
    });

    return buckets;
  }, [sortedJobs]);

  return (
    <div>
      <div className="card">
        <h2>Histórico de Jobs</h2>
        {sortedJobs.length === 0 ? (
          <p>Sem jobs registados localmente.</p>
        ) : (
          <div className="summary-grid">
            {ORDER.map((state) => (
              <div key={state} className="summary-tile">
                <h4>{formatState(state)}</h4>
                <span>{grouped[state].length}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
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
                <tr key={job.job_id} onClick={() => navigate(`/jobs/${job.job_id}`)} style={{ cursor: "pointer" }}>
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
      </div>
    </div>
  );
}

export default HistoryPage;

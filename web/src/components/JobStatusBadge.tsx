import { JobState } from "../types";
import { formatState } from "../utils/format";

interface Props {
  state: JobState;
}

const ICONS: Record<JobState, string> = {
  queued: "⏳",
  processing: "⚙️",
  ready: "✅",
  approved: "🏁",
  failed: "❌",
};

function JobStatusBadge({ state }: Props) {
  return <span className={`badge ${state}`}>{ICONS[state]} {formatState(state)}</span>;
}

export default JobStatusBadge;

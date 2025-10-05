export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const API_ROUTES = {
  jobs: `${API_BASE_URL}/api/jobs`,
  health: `${API_BASE_URL}/api/health`,
};

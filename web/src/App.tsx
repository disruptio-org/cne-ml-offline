import { NavLink, Route, Routes } from "react-router-dom";

import HistoryPage from "./pages/HistoryPage";
import ResultPage from "./pages/ResultPage";
import UploadPage from "./pages/UploadPage";

function App() {
  return (
    <div className="main-shell">
      <aside className="sidebar">
        <h1>CNE Offline</h1>
        <nav>
          <NavLink to="/" end>
            Upload
          </NavLink>
          <NavLink to="/jobs" end>
            Histórico
          </NavLink>
        </nav>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/jobs" element={<HistoryPage />} />
          <Route path="/jobs/:jobId" element={<ResultPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

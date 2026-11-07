import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Employees from "./pages/Employees";
import Resources from "./pages/Resources";
import Requests from "./pages/Requests";
import Grants from "./pages/Grants";
import Reviews from "./pages/Reviews";
import AuditLogs from "./pages/AuditLogs";

function App() {
  return (
    <BrowserRouter>
      <div
        style={{
          display: "flex",
          background: "#f8fafc",
        }}
      >
        <Sidebar />

        <div
          style={{
            flex: 1,
            padding: "30px",
          }}
        >
          <Routes>
            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/employees"
              element={<Employees />}
            />

            <Route
              path="/resources"
              element={<Resources />}
            />

            <Route
              path="/requests"
              element={<Requests />}
            />

            <Route
              path="/grants"
              element={<Grants />}
            />

            <Route
              path="/reviews"
              element={<Reviews />}
            />

            <Route
              path="/audit-logs"
              element={<AuditLogs />}
            />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
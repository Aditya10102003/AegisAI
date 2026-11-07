import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div
      style={{
        width: "220px",
        background: "#1e293b",
        color: "white",
        minHeight: "100vh",
        padding: "20px",
      }}
    >
      <h2>AegisAI</h2>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "15px",
          marginTop: "30px",
        }}
      >
        <Link to="/" style={{ color: "white" }}>Dashboard</Link>

        <Link to="/employees" style={{ color: "white" }}>
          Employees
        </Link>

        <Link to="/resources" style={{ color: "white" }}>
          Resources
        </Link>

        <Link to="/requests" style={{ color: "white" }}>
          Requests
        </Link>

        <Link to="/grants" style={{ color: "white" }}>
          Grants
        </Link>

        <Link to="/reviews" style={{ color: "white" }}>
          Reviews
        </Link>

        <Link to="/audit-logs" style={{ color: "white" }}>
          Audit Logs
        </Link>
      </div>
    </div>
  );
}
import { useEffect, useState } from "react";
import axios from "axios";

function Card({ title, value }) {
  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0px 2px 4px rgba(0,0,0,0.1)",
        textAlign: "center",
      }}
    >
      <h3>{title}</h3>
      <h1>{value}</h1>
    </div>
  );
}

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/dashboard")
      .then((res) => setDashboard(res.data));
  }, []);

  if (!dashboard) {
    return <h2>Loading...</h2>;
  }

  return (
    <>
      <h1>Dashboard</h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(5, 1fr)",
          gap: "20px",
        }}
      >
        <Card title="Employees" value={dashboard.employees} />
        <Card title="Resources" value={dashboard.resources} />
        <Card title="Requests" value={dashboard.pending_requests} />
        <Card title="Active Grants" value={dashboard.active_grants} />
        <Card title="Reviews" value={dashboard.pending_reviews} />
      </div>
    </>
  );
}
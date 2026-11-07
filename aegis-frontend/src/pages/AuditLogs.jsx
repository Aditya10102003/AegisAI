import { useEffect, useState } from "react";
import axios from "axios";

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/audit-logs")
      .then((response) => {
        setLogs(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Audit Logs</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead>
          <tr>
            <th>Action</th>
            <th>Requested Action</th>
            <th>Decision</th>
            <th>Reason</th>
            <th>Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.action}</td>

              <td>{log.requested_action}</td>

              <td>
                <span
                  style={{
                    padding: "6px 12px",
                    borderRadius: "6px",
                    backgroundColor:
                      log.decision === "Allowed"
                        ? "#d1fae5"
                        : "#fee2e2",
                    color:
                      log.decision === "Allowed"
                        ? "green"
                        : "red",
                  }}
                >
                  {log.decision}
                </span>
              </td>

              <td>{log.reason}</td>

              <td>
                {new Date(
                  log.timestamp
                ).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

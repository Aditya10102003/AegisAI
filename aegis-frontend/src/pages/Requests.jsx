import { useEffect, useState } from "react";
import axios from "axios";

export default function Requests() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/access-requests")
      .then((response) => {
        setRequests(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Access Requests</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {requests.map((request) => (
            <tr key={request.id}>
              <td>{request.id}</td>
              <td>
                <span
                  style={{
                    padding: "6px 12px",
                    borderRadius: "6px",
                    backgroundColor:
                      request.status === "Approved"
                        ? "#d1fae5"
                        : request.status === "Rejected"
                        ? "#fee2e2"
                        : "#fef3c7",
                    color:
                      request.status === "Approved"
                        ? "green"
                        : request.status === "Rejected"
                        ? "red"
                        : "#92400e",
                  }}
                >
                  {request.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
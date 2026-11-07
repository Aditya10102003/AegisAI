import { useEffect, useState } from "react";
import axios from "axios";

export default function Grants() {
  const [grants, setGrants] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/access-grants")
      .then((response) => {
        setGrants(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Access Grants</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead>
          <tr>
            <th>Employee</th>
            <th>Resource</th>
            <th>Action</th>
            <th>Status</th>
            <th>Grant Type</th>
          </tr>
        </thead>

        <tbody>
          {grants.map((grant) => (
            <tr key={grant.grant_id}>
              <td>{grant.employee_id}</td>
              <td>{grant.resource}</td>
              <td>{grant.action}</td>
              <td>
                <span
                  style={{
                    padding: "6px 12px",
                    borderRadius: "6px",
                    backgroundColor:
                      grant.status === "Active"
                        ? "#d1fae5"
                        : "#fee2e2",
                    color:
                      grant.status === "Active"
                        ? "green"
                        : "red",
                  }}
                >
                  {grant.status}
                </span>
              </td>
              <td>{grant.grant_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

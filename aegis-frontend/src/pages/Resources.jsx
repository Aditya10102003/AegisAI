import { useEffect, useState } from "react";
import axios from "axios";

export default function Resources() {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/resources")
      .then((response) => {
        setResources(response.data);
      });
  }, []);

  return (
    <div>
      <h1>Resources</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Sensitivity</th>
            <th>Environment</th>
            <th>Active</th>
          </tr>
        </thead>

        <tbody>
          {resources.map((resource) => (
            <tr key={resource.id}>
              <td>{resource.name}</td>
              <td>{resource.resource_type}</td>
              <td>{resource.sensitivity_level}</td>
              <td>{resource.environment}</td>
              <td>
                {resource.active ? "Yes" : "No"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
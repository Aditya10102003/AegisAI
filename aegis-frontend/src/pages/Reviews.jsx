import { useEffect, useState } from "react";
import axios from "axios";

export default function Reviews() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/access-reviews")
      .then((response) => {
        setReviews(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Access Reviews</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead>
          <tr>
            <th>Review ID</th>
            <th>Status</th>
            <th>Decision</th>
            <th>Due Date</th>
          </tr>
        </thead>

        <tbody>
          {reviews.map((review) => (
            <tr key={review.id}>
              <td>{review.id}</td>

              <td>
                <span
                  style={{
                    padding: "6px 12px",
                    borderRadius: "6px",
                    backgroundColor:
                      review.status === "Completed"
                        ? "#d1fae5"
                        : "#fef3c7",
                    color:
                      review.status === "Completed"
                        ? "green"
                        : "#92400e",
                  }}
                >
                  {review.status}
                </span>
              </td>

              <td>
                {review.decision || "Pending"}
              </td>

              <td>
                {new Date(
                  review.due_date
                ).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
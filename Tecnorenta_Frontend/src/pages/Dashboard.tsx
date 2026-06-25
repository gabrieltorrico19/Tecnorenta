import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Dashboard() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    api
      .get("/health")
      .then((res) => setStatus(res.data.status))
      .catch(() => setStatus("offline"));
  }, []);

  return (
    <div>
      <h2>Panel Principal</h2>
      <p>
        Backend:{" "}
        <strong style={{ color: status === "ok" ? "green" : "red" }}>
          {status}
        </strong>
      </p>
    </div>
  );
}

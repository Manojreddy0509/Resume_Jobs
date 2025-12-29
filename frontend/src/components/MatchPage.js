import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { matchSingle } from "../api/api";
import NavBar from "./NavBar";
import "../Futuristic.css";

export default function MatchPage() {
  const [params] = useSearchParams();
  const resume_id = params.get("resume_id");
  const job_id = params.get("job_id");
  const [res, setRes] = useState(null);

  useEffect(() => {
    (async () => {
      if (resume_id && job_id) {
        const data = await matchSingle(resume_id, job_id);
        setRes(data);
      }
    })();
  }, [resume_id, job_id]);

  return (
    <div className="futuristic-body">
      <NavBar />
      <div className="futuristic-container">
        <div className="neon-card">
          <h3 className="neon-title">Analysis Detail</h3>
          {res ? (
            <div className="match-result-box">
              <div className="score-display">{(res.score * 100).toFixed(1)}%</div>
              <div style={{ color: '#00ff66', fontSize: '1.5rem', marginBottom: '20px' }}>
                {res.label}
              </div>
              <div style={{ marginBottom: '15px', color: '#ccc' }}>
                <strong style={{ color: '#00f3ff' }}>Match Reasoning:</strong>
                <ul style={{ marginTop: '10px' }}>
                  {res.reasons?.map((r, i) => (
                    <li key={i} style={{ marginBottom: '5px' }}>{r}</li>
                  ))}
                </ul>
              </div>
              <div style={{ color: '#ff4b4b' }}>
                <strong style={{ color: '#ff4b4b' }}>Missing Skills:</strong> {res.missing_skills?.join(", ") || "None"}
              </div>
            </div>
          ) : (
            <p style={{ color: '#888' }}>Initializing neural link... (Loading)</p>
          )}
        </div>
      </div>
    </div>
  );
}

// src/components/recruiter/RankedResumes.js
import React, { useState } from "react";
import { rankJob } from "../../api/api";

export default function RankedResumes({ jobId }) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const data = await rankJob(jobId, 50);
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      alert("Failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button className="cyber-btn" onClick={load} disabled={loading} style={{ marginBottom: '20px' }}>
        {loading ? "SCANNING DATABASE..." : "RETRIEVE TOP CANDIDATES"}
      </button>
      <ul className="neon-list">
        {results.map((r) => (
          <li key={r.resume_id} className="neon-list-item">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ fontSize: '1.1rem', color: '#fff' }}>{r.filename}</strong>
                <span style={{ color: '#00ff66', fontSize: '1.2rem', fontFamily: 'Orbitron' }}>{(r.score * 100).toFixed(1)}%</span>
            </div>
            <div style={{ color: '#aaa', fontSize: '0.9rem', marginTop: '5px' }}>Label: {r.label}</div>
            <div style={{ marginTop: '8px', color: '#ccc' }}>
                <span style={{ color: '#888' }}>Key Match:</span> {r.reasons?.slice(0,3).join(" | ")}
            </div>
            <div style={{ marginTop: '5px', color: '#ff4b4b', fontSize: '0.9rem' }}>
                <span style={{ color: '#888' }}>Missing:</span> {r.missing_skills?.join(", ") || "None"}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
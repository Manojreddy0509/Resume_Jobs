// src/components/student/StudentDashboard.js
import React, { useEffect, useState, useContext } from "react";
import ResumeUpload from "./ResumeUpload";
import { listJobs, listResumes, matchSingle } from "../../api/api";
import NavBar from "../NavBar";
import { AuthContext } from "../../context/AuthContext";
import "../../Futuristic.css";

export default function StudentDashboard() {
  const [jobs, setJobs] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [matchResult, setMatchResult] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    (async () => {
      try {
        const j = await listJobs();
        setJobs(j || []);
        const r = await listResumes();
        setResumes(r || []);
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  const onUploaded = (data) => {
    setResumes((prev) => [data, ...prev]);
    setSelectedResume(data.resume_id);
  };

  const runMatch = async (jobId) => {
    if (!selectedResume) return alert("Select a resume or upload one");
    const res = await matchSingle(selectedResume, jobId);
    console.log("MATCH RESPONSE:", res);
    setMatchResult(res);
  };

  return (
    <div className="futuristic-body">
      <NavBar />
      <div className="futuristic-container">
        <div className="left-col">
          <div className="neon-card">
            <h3 className="neon-title">Upload Resume</h3>
            <ResumeUpload onUploaded={onUploaded} />
          </div>
          
          <div className="neon-card" style={{ marginTop: '30px' }}>
            <h3 className="neon-title">Your Resumes</h3>
            {resumes.length === 0 && <p style={{ color: '#888' }}>No resumes uploaded yet</p>}
            <ul className="neon-list">
              {resumes.map((r) => (
                <li 
                  key={r.resume_id || r.id} 
                  className={`neon-list-item ${selectedResume === (r.resume_id || r.id) ? 'active' : ''}`}
                  onClick={() => setSelectedResume(r.resume_id || r.id)}
                >
                  <label style={{ cursor: 'pointer', display: 'block' }}>
                    <input 
                      type="radio" 
                      name="resume" 
                      checked={selectedResume === (r.resume_id || r.id)}
                      onChange={() => setSelectedResume(r.resume_id || r.id)} 
                      style={{ marginRight: '10px' }}
                    />
                    {r.filename}
                  </label>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="right-col">
          <div className="neon-card">
            <h3 className="neon-title">Available Missions (Jobs)</h3>
            {jobs.map((job) => (
              <div key={job.job_id || job.id} className="job-row">
                <div>
                  <div className="job-title">{job.parsed?.title || job.title}</div>
                  <div className="job-skills">{job.parsed?.required_skills?.join(", ") || job.description}</div>
                </div>
                <button 
                  className="cyber-btn"
                  onClick={() => runMatch(job.job_id || job.id)}
                >
                  Analyze Match
                </button>
              </div>
            ))}
          </div>

          <div className="neon-card" style={{ marginTop: '30px' }}>
            <h3 className="neon-title">Analysis Result</h3>
            {matchResult ? (
              <div className="match-result-box">
                <div className="score-display">{(matchResult.score * 100).toFixed(1)}%</div>
                <div style={{ color: '#00ff66', fontSize: '1.2rem', marginBottom: '10px' }}>
                  {matchResult.label}
                </div>
                <div style={{ color: '#ccc' }}>
                  <strong>Key Factors:</strong> {matchResult.reasons.join(" | ")}
                </div>
              </div>
            ) : (
              <p style={{ color: '#888', fontStyle: 'italic' }}>Select a resume and a job to run analysis...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
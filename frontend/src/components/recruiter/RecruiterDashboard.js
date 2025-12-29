// src/components/recruiter/RecruiterDashboard.js
import React, { useEffect, useState } from "react";
import NavBar from "../NavBar";
import JobCreate from "./JobCreate";
import RankedResumes from "./RankedResumes";
import { listJobs } from "../../api/api";
import "../../Futuristic.css";

export default function RecruiterDashboard() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    (async () => {
      const j = await listJobs();
      setJobs(j || []);
    })();
  }, []);

  return (
    <div className="futuristic-body">
      <NavBar />
      <div className="futuristic-container">
        <div className="left-col">
          <div className="neon-card">
            <h3 className="neon-title">Post New Mission</h3>
            <JobCreate onCreated={(data) => setJobs((prev) => [data, ...prev])} />
          </div>
        </div>

        <div className="right-col">
          <div className="neon-card">
            <h3 className="neon-title">Active Missions (Jobs)</h3>
            {jobs.length === 0 && <p style={{ color: '#888' }}>No jobs posted yet</p>}
            {jobs.map((job) => (
              <div 
                key={job.job_id} 
                className="job-row" 
                onClick={() => setSelectedJob(job.job_id)}
                style={{ cursor: 'pointer' }}
              >
                <div>
                  <div className="job-title">{job.parsed?.title || job.title}</div>
                  <div className="job-skills">{job.parsed?.required_skills?.join(", ")}</div>
                  <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '5px' }}>
                    Click to view ranked candidates
                  </div>
                </div>
                <button className="cyber-btn">View Candidates</button>
              </div>
            ))}
          </div>

          {selectedJob && (
            <div className="neon-card" style={{ marginTop: '30px' }}>
               <h3 className="neon-title">Ranked Operatives (Candidates)</h3>
               <RankedResumes jobId={selectedJob} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

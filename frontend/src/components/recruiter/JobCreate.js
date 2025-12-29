// src/components/recruiter/JobCreate.js
import React, { useState } from "react";
import { createJob } from "../../api/api";

export default function JobCreate({ onCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [minExp, setMinExp] = useState(0);
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      const parsedSkills = description.match(/\b(python|fastapi|ml|machine learning|docker|aws|sql|postgres|mongodb|r)\b/gi) || [];
      const payload = {
        title,
        description,
        min_experience_years: Number(minExp),
        parsed_skills: parsedSkills, // backend will parse anyway
      };
      const data = await createJob(payload);
      setMsg("Job created: " + data.job_id);
      onCreated && onCreated(data);
    } catch (err) {
      setMsg(err?.response?.data?.detail || "Failed");
    }
  };

  return (
    <form onSubmit={submit}>
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', color: '#888', marginBottom: '5px', fontSize: '0.9rem' }}>MISSION TITLE</label>
        <input 
          className="cyber-input"
          value={title} 
          onChange={(e) => setTitle(e.target.value)} 
          required 
          placeholder="e.g. Senior Frontend Engineer"
        />
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', color: '#888', marginBottom: '5px', fontSize: '0.9rem' }}>MISSION BRIEF</label>
        <textarea 
          className="cyber-input"
          value={description} 
          onChange={(e) => setDescription(e.target.value)} 
          required 
          rows={5}
          placeholder="Paste job description here..."
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', color: '#888', marginBottom: '5px', fontSize: '0.9rem' }}>MIN EXPERIENCE (YEARS)</label>
        <input 
          className="cyber-input"
          type="number" 
          value={minExp} 
          onChange={(e) => setMinExp(e.target.value)} 
        />
      </div>

      <button type="submit" className="cyber-btn">INITIATE MISSION (POST JOB)</button>
      {msg && <p style={{ color: '#00ff66', marginTop: '10px' }}>{msg}</p>}
    </form>
  );
}
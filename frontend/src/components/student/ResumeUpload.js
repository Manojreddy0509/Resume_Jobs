// src/components/student/ResumeUpload.js
import React, { useState } from "react";
import { uploadResume } from "../../api/api";

export default function ResumeUpload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    if (!file) return setMsg("Select a PDF first");
    setLoading(true);
    try {
      const data = await uploadResume(file);
      setMsg("Uploaded: " + data.filename);
      onUploaded && onUploaded(data);
    } catch (err) {
      setMsg(err?.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit}>
      <div className="cyber-file-upload">
        <input 
          type="file" 
          accept="application/pdf" 
          onChange={(e) => setFile(e.target.files[0])} 
          style={{ color: '#fff' }}
        />
      </div>
      <button className="cyber-btn" type="submit" disabled={loading}>
        {loading ? "INITIALIZING UPLOAD..." : "UPLOAD RESUME DATA"}
      </button>
      {msg && <p style={{ color: '#00ff66', marginTop: '10px' }}>{msg}</p>}
    </form>
  );
}

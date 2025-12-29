// src/components/auth/Signup.js
import React, { useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../../LiquidGlass.css";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [name, setName] = useState("");
  const { signup } = useContext(AuthContext);
  const nav = useNavigate();
  const [err, setErr] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    setErr(null);
    try {
      await signup({ email, password, name, role });
      nav(role === "recruiter" ? "/recruiter" : "/student");
    } catch (err) {
      setErr(err?.response?.data?.detail || "Signup failed");
    }
  };

  return (
    <div className="liquid-container">
      <div className="glass-panel">
        <h2>Create Account</h2>
        <form onSubmit={submit} className="glass-form">
          <div className="glass-input-group">
            <label>Full Name</label>
            <input 
              className="glass-input"
              value={name} 
              onChange={(e) => setName(e.target.value)} 
              required 
              placeholder="John Doe"
            />
          </div>

          <div className="glass-input-group">
            <label>Email Address</label>
            <input 
              className="glass-input"
              type="email"
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              required 
              placeholder="name@example.com"
            />
          </div>

          <div className="glass-input-group">
            <label>Password</label>
            <input 
              className="glass-input"
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
              placeholder="••••••••"
            />
          </div>

          <div className="glass-input-group">
            <label>I am a</label>
            <select 
              className="glass-select"
              value={role} 
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="student">Student / Job Seeker</option>
              <option value="recruiter">Recruiter / Employer</option>
            </select>
          </div>

          {err && <div className="error-message">{err}</div>}

          <button type="submit" className="glass-button">Sign Up</button>
        </form>
      </div>
    </div>
  );
}

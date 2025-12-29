// src/components/auth/Login.js
import React, { useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import "../../LiquidGlass.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await login(email, password, role);
      // redirect based on role
      nav(role === "recruiter" ? "/recruiter" : "/student");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="liquid-container">
      <div className="glass-panel">
        <h2>Sign In</h2>
        <form onSubmit={submit} className="glass-form">
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

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="glass-button">Sign In</button>
          
          <div className="glass-link">
            Don't have an account? <Link to="/signup">Sign up now</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
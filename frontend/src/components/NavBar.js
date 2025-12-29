// src/components/NavBar.js
import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../Futuristic.css";

export default function NavBar() {
  const { user, logout } = useContext(AuthContext);
  const nav = useNavigate();
  const handleLogout = () => {
    logout();
    nav("/login");
  };

  return (
    <nav className="topbar">
      <div className="brand">YouMatch</div>
      <div className="links">
        {user && user.user && user.user.role === "recruiter" && <Link to="/recruiter">Dashboard</Link>}
        {user && user.user && user.user.role === "student" && <Link to="/student">Dashboard</Link>}
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}
// src/App.js
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, AuthContext } from "./context/AuthContext";

import Login from "./components/auth/Login";
import Signup from "./components/auth/Signup";
import StudentDashboard from "./components/student/StudentDashboard";
import RecruiterDashboard from "./components/recruiter/RecruiterDashboard";
import MatchPage from "./components/MatchPage";

function PrivateRoute({ children, roles }) {
  // roles: allowed role(s)
  const { user } = React.useContext(AuthContext);
  if (!user) return <Navigate to="/login" />;
  if (roles && !roles.includes(user.user.role)) return <Navigate to="/" />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          <Route path="/student" element={
            <PrivateRoute roles={["student"]}>
              <StudentDashboard />
            </PrivateRoute>
          } />

          <Route path="/recruiter" element={
            <PrivateRoute roles={["recruiter"]}>
              <RecruiterDashboard />
            </PrivateRoute>
          } />

          <Route path="/match" element={
            <PrivateRoute>
              <MatchPage />
            </PrivateRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
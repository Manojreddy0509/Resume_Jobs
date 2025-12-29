// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from "react";
import { loginUser, signupUser } from "../api/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("access_token", user.token || "");
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
    }
  }, [user]);

  const login = async (email, password, role) => {
  const fakeUser = {
    token: "dev-token",
    user: { email, role }};
  setUser(fakeUser);
  return fakeUser;};


  const signup = async (payload) => {
    const data = await signupUser(payload);
    setUser(data);
    return data;
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
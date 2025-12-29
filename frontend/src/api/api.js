// src/api/api.js
import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 30000,
  withCredentials: false, // IMPORTANT
});

// attach JWT if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function loginUser(email, password, role) {
  // role optional: "student" or "recruiter"
  const resp = await api.post("/auth/login", { email, password, role });
  return resp.data;
}

export async function signupUser(payload) {
  const resp = await api.post("/auth/signup", payload);
  return resp.data;
}

export async function uploadResume(file) {
  const form = new FormData();
  form.append("file", file);
  const resp = await api.post("/resumes/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return resp.data;
}

export async function createJob(jobPayload) {
  const resp = await api.post("/jobs/", jobPayload);
  return resp.data;
}

export async function matchSingle(resume_id, job_id) {
  const resp = await api.post("/match/", { resume_id, job_id });
  return resp.data;
}

export async function rankJob(job_id, limit = 50) {
  const resp = await api.post(`/match/job/${job_id}?limit=${limit}`);
  return resp.data;
}

export async function listJobs() {
  const resp = await api.get("/jobs/");
  return resp.data;
}

export async function listResumes() {
  const resp = await api.get("/resumes/all"); // implement this endpoint or fetch from DB
  return resp.data;
}

export default api;

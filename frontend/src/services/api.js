import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  timeout: 10000
});

export function setAuthToken(token) {
  if (token) {
    client.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete client.defaults.headers.common.Authorization;
  }
}

export async function login(email, password) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);
  const response = await client.post("/auth/login", body);
  return response.data;
}

export async function listUsers() {
  const response = await client.get("/users/");
  return response.data;
}

export async function getProfile() {
  const response = await client.get("/profile/me");
  return response.data;
}

export async function updateProfile(profile) {
  const response = await client.patch("/profile/me", profile);
  return response.data;
}

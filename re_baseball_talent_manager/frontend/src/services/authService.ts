import api from "./api";
import type { AxiosError } from "axios";
import type { AuthResponse } from "@/stores/auth"; 

export async function login(email: string, password: string): Promise<AuthResponse> {
  const res = await api.post("/api/auth/login", { email, password });
  return res.data;
}

export async function refreshAccessToken(): Promise<AuthResponse | null> {
  try {
    const res = await api.post("/api/auth/refresh");
    return res.data;
  } catch (error) {
    const err = error as AxiosError;

    if (err.response?.status === 401) {
      return null;
    }
    throw error;
  }
}

export async function logout(): Promise<void> {
  try {
    await api.post("/api/auth/logout");
  } catch (e) {
    // 無視
  }
}

import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// リクエストインターセプター：Access Tokenを自動付与
api.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`;
  }
  return config;
});

// レスポンスインターセプター：401エラー時にRefresh Tokenで自動更新
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // refreshエンドポイント自体が401の場合はループしない
    if (originalRequest.url === "/api/auth/refresh") {
      const authStore = useAuthStore();
      await authStore.logout();
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const authStore = useAuthStore();
      const refreshed = await authStore.refreshAccessToken();

      if (refreshed) {
        originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`;
        return api(originalRequest);
      } else {
        await authStore.logout();
      }
    }

    return Promise.reject(error);
  },
);

export default api;

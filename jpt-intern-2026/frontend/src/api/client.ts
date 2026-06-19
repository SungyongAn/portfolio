import { useAuthStore } from "@/stores/auth";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
}

interface ApiResponse<T> {
  data: T;
}

async function request<T>(
  path: string,
  options: RequestOptions = {},
): Promise<ApiResponse<T>> {
  const authStore = useAuthStore();
  const { method = "GET", body } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (authStore.accessToken) {
    headers["Authorization"] = `Bearer ${authStore.accessToken}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  // 401エラー時はログアウト
  if (response.status === 401) {
    await authStore.logout();
    throw new Error("認証エラー");
  }

  // 204 No Contentはbodyなし
  if (response.status === 204) {
    return { data: null as T };
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw { response: { status: response.status, data: errorData } };
  }

  const data = await response.json();
  return { data };
}

const apiClient = {
  get<T>(url: string) {
    return request<T>(url);
  },
  post<T>(url: string, body?: unknown) {
    return request<T>(url, { method: "POST", body });
  },
  put<T>(url: string, body?: unknown) {
    return request<T>(url, { method: "PUT", body });
  },
  patch<T>(url: string, body?: unknown) {
    return request<T>(url, { method: "PATCH", body });
  },
  delete<T = void>(url: string) {
    return request<T>(url, { method: "DELETE" });
  },
};

export default apiClient;

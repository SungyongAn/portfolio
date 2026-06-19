import apiClient from "./client";

export type LoginRequest = {
  email: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
};

export const authAPI = {
  login(data: LoginRequest) {
    return apiClient.post<TokenResponse>("/api/auth/login", data);
  },

  refresh(refresh_token: string) {
    return apiClient.post<TokenResponse>("/api/auth/refresh", {
      refresh_token,
    });
  },
};

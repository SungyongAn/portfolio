import { defineStore } from "pinia";
import router from "@/router";
import { authAPI } from "@/api/auth";
import { usersAPI } from "@/api/users";
import type { UserRole } from "@/api/models/UserRole";

export type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  tokenExpiry: number | null;
  userId: number | null;
  userName: string | null;
  role: UserRole | null;
  departmentId: number | null;
  isInitialized: boolean;
};

// Store
export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    accessToken: null,
    refreshToken: null,
    tokenExpiry: null,
    userId: null,
    userName: null,
    role: null,
    departmentId: null,
    isInitialized: false,
  }),

  // getters
  getters: {
    isAuthenticated(): boolean {
      return !!this.accessToken && !this.isTokenExpired;
    },

    isTokenExpired(state): boolean {
      if (!state.tokenExpiry) return true;
      return Date.now() > state.tokenExpiry;
    },

    isApplicant(): boolean {
      return this.role === "APPLICANT";
    },

    isTaskMember(): boolean {
      return this.role === "TASK_MEMBER";
    },

    isDeptManager(): boolean {
      return this.role === "DEPT_MANAGER";
    },

    isHqManager(): boolean {
      return this.role === "HQ_MANAGER";
    },

    displayRole(): string | null {
      const roleMap: Record<UserRole, string> = {
        APPLICANT: "申請者",
        TASK_MEMBER: "担当者",
        DEPT_MANAGER: "部門管理者",
        HQ_MANAGER: "本部管理者",
      };
      return this.role ? roleMap[this.role] : null;
    },

    canApprove(): boolean {
      return this.role === "DEPT_MANAGER" || this.role === "HQ_MANAGER";
    },
  },

  // actions
  actions: {
    async login(email: string, password: string): Promise<void> {
      // APIでログイン
      const response = await authAPI.login({ email, password });
      const { access_token, refresh_token, expires_in } = response.data;

      // トークンをセッションストレージに保存
      sessionStorage.setItem("accessToken", access_token);
      sessionStorage.setItem("refreshToken", refresh_token);
      sessionStorage.setItem(
        "tokenExpiry",
        String(Date.now() + expires_in * 1000),
      );

      this.accessToken = access_token;
      this.refreshToken = refresh_token;
      this.tokenExpiry = Date.now() + expires_in * 1000;

      // ユーザー情報を取得
      const userResponse = await usersAPI.getMe();
      const user = userResponse.data;
      this.userId = user.id;
      this.userName = user.name;
      this.role = user.role;
      this.departmentId = user.department_id ?? null;
    },

    async initAuth(): Promise<void> {
      const accessToken = sessionStorage.getItem("accessToken");
      const refreshToken = sessionStorage.getItem("refreshToken");
      const storedExpiry = sessionStorage.getItem("tokenExpiry");

      if (!accessToken || !storedExpiry) {
        this.isInitialized = true;
        return;
      }

      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
      this.tokenExpiry = parseInt(storedExpiry);

      if (this.isTokenExpired) {
        // リフレッシュトークンで再取得を試みる
        const refreshed = await this.refreshAccessToken();
        if (!refreshed) {
          this.clearAuth();
          this.isInitialized = true;
          return;
        }
      }

      // ユーザー情報を取得
      try {
        const userResponse = await usersAPI.getMe();
        const user = userResponse.data;
        this.userId = user.id;
        this.userName = user.name;
        this.role = user.role;
        this.departmentId = user.department_id ?? null;
      } catch {
        this.clearAuth();
      }

      this.isInitialized = true;
    },

    async logout(): Promise<void> {
      this.clearAuth();
      router.push("/login");
    },

    async refreshAccessToken(): Promise<boolean> {
      if (!this.refreshToken) return false;

      try {
        const response = await authAPI.refresh(this.refreshToken);
        const { access_token, refresh_token, expires_in } = response.data;

        this.accessToken = access_token;
        this.refreshToken = refresh_token;
        this.tokenExpiry = Date.now() + expires_in * 1000;

        sessionStorage.setItem("accessToken", access_token);
        sessionStorage.setItem("refreshToken", refresh_token);
        sessionStorage.setItem("tokenExpiry", String(this.tokenExpiry));

        return true;
      } catch {
        return false;
      }
    },

    clearAuth(): void {
      sessionStorage.removeItem("accessToken");
      sessionStorage.removeItem("refreshToken");
      sessionStorage.removeItem("tokenExpiry");

      this.accessToken = null;
      this.refreshToken = null;
      this.tokenExpiry = null;
      this.userId = null;
      this.userName = null;
      this.role = null;
      this.departmentId = null;
    },
  },
});

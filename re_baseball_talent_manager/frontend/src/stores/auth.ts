import { defineStore } from "pinia";
import * as authAPI from "@/services/authService";
import router from "@/router";
import { useNotificationStore } from "@/stores/notification";

// ==============================
// 型定義
// ==============================

export type Role = "manager" | "member" | "coach" | "director";

export type EventListenerItem = {
  eventName: string;
  handler: () => void;
};

export type AuthState = {
  accessToken: string | null;

  tokenExpiry: number | null;
  userName: string | null;
  userId: number | null;

  member_grade: number | null;

  isInitialized: boolean;
  lastActivity: number;

  role: Role | null;

  inactivityTimer: ReturnType<typeof setTimeout> | null;
  eventListeners: EventListenerItem[];

  roleMap: Record<Role, string>;
};

// APIレスポンス型
export type AuthResponse = {
  access_token: string;
  expires_in: number;
  role: Role;
  user_id: number;
  name: string;
  grade?: number;
};

// ==============================
// Store
// ==============================

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    accessToken: null,

    tokenExpiry: null,
    userName: null,
    userId: null,

    member_grade: null,

    isInitialized: false,
    lastActivity: Date.now(),

    role: null,

    inactivityTimer: null,
    eventListeners: [],

    roleMap: {
      manager: "マネージャー",
      member: "部員",
      coach: "コーチ",
      director: "監督",
    },
  }),

  // ==============================
  // getters
  // ==============================
  getters: {
    isAuthenticated(): boolean {
      return !!this.accessToken && !this.isTokenExpired;
    },

    isTokenExpired(state): boolean {
      if (!state.tokenExpiry) return true;
      return Date.now() > state.tokenExpiry;
    },

    maybeLoggedIn(state): boolean {
      return (
        !!state.accessToken ||
        !!state.tokenExpiry ||
        !!sessionStorage.getItem("tokenExpiry")
      );
    },

    memberGrade(): number | null {
      return this.member_grade ?? null;
    },

    displayRole(): string | null {
      return this.role ? this.roleMap[this.role] || this.role : null;
    },

    isManager(): boolean {
      return this.role === "manager";
    },

    isMember(): boolean {
      return this.role === "member";
    },

    isCoach(): boolean {
      return this.role === "coach";
    },

    isDirector(): boolean {
      return this.role === "director";
    },

    isStaff(): boolean {
      return this.role === "coach" || this.role === "director";
    },
  },

  // ==============================
  // actions
  // ==============================
  actions: {
    async login(email: string, password: string): Promise<boolean> {
      try {
        const data: AuthResponse = await authAPI.login(email, password);

        this.accessToken = data.access_token;
        this.tokenExpiry = Date.now() + data.expires_in * 1000;
        sessionStorage.setItem("tokenExpiry", String(this.tokenExpiry));

        this.role = data.role;
        this.userId = data.user_id;
        this.userName = data.name;
        this.member_grade = data.grade ?? null;

        const notificationStore = useNotificationStore();
        if (this.accessToken && !notificationStore.isConnected) {
          notificationStore.connect(this.accessToken);
        }

        this.updateActivity();
        this.startInactivityTimer();

        return true;
      } catch (error) {
        console.error("ログインエラー:", error);
        throw error;
      }
    },

    async refreshAccessToken(): Promise<boolean> {
      const data: AuthResponse | null = await authAPI.refreshAccessToken();

      if (!data) {
        return false;
      }

      this.accessToken = data.access_token;
      this.tokenExpiry = Date.now() + data.expires_in * 1000;
      sessionStorage.setItem("tokenExpiry", String(this.tokenExpiry));

      this.role = data.role;
      this.userId = data.user_id;
      this.userName = data.name;
      this.member_grade = data.grade ?? null;

      return true;
    },

    async initAuth(): Promise<void> {
      const storedExpiry = sessionStorage.getItem("tokenExpiry");
      if (storedExpiry) {
        this.tokenExpiry = parseInt(storedExpiry);
      }

      if (!this.maybeLoggedIn) {
        this.isInitialized = true;
        return;
      }

      const refreshed = await this.refreshAccessToken();

      if (refreshed) {
        this.startInactivityTimer();

        const notificationStore = useNotificationStore();
        if (this.accessToken && !notificationStore.isConnected) {
          notificationStore.connect(this.accessToken);
        }
      }

      this.isInitialized = true;
    },

    startInactivityTimer(): void {
      const INACTIVITY_TIMEOUT = 30 * 60 * 1000;

      this.clearInactivityTimer();

      const resetTimer = () => {
        this.updateActivity();

        if (this.inactivityTimer) {
          clearTimeout(this.inactivityTimer);
        }

        this.inactivityTimer = setTimeout(() => {
          this.logout();
        }, INACTIVITY_TIMEOUT);
      };

      const events = ["mousemove", "keypress", "click", "scroll", "touchstart"];

      events.forEach((eventName) => {
        window.addEventListener(eventName, resetTimer);
        this.eventListeners.push({ eventName, handler: resetTimer });
      });

      resetTimer();
    },

    clearInactivityTimer(): void {
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer);
        this.inactivityTimer = null;
      }

      this.eventListeners.forEach(({ eventName, handler }) => {
        window.removeEventListener(eventName, handler);
      });

      this.eventListeners = [];
    },

    updateActivity(): void {
      this.lastActivity = Date.now();
    },

    async logout(): Promise<void> {
      try {
        await authAPI.logout();
      } catch {
        // 無視
      }

      const notificationStore = useNotificationStore();
      notificationStore.disconnect();

      this.clearInactivityTimer();

      sessionStorage.removeItem("tokenExpiry");

      this.accessToken = null;
      this.tokenExpiry = null;
      this.role = null;
      this.userName = null;
      this.userId = null;
      this.member_grade = null;

      router.push("/login");
    },
  },
});
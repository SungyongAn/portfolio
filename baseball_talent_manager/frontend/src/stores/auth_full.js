import { defineStore } from "pinia";
import * as authAPI from "@/services/authService";
import router from "@/router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: null,
    tokenExpiry: null, // トークンの有効期限
    role: null,
    userName: null,
    userId: null,
    member_grade: null,
    isInitialized: false,
    lastActivity: Date.now(),
    inactivityTimer: null,
    eventListeners: [],

    roleMap: {
      manager: "マネージャー",
      member: "部員",
      coach: "コーチ",
      director: "監督",
    },
  }),

  getters: {
    isAuthenticated() {
      return !!this.accessToken && !this.isTokenExpired;
    },

    isTokenExpired(state) {
      if (!state.tokenExpiry) return true;
      return Date.now() > state.tokenExpiry;
    },

    maybeLoggedIn(state) {
      return !!state.accessToken || !!state.tokenExpiry;
    },

    memberGrade() {
      return this.member_grade ?? null;
    },

    displayRole() {
      return this.role ? this.roleMap[this.role] || this.role : null;
    },

    isManager() {
      return this.role === "manager";
    },

    isMember() {
      return this.role === "member";
    },

    isCoach() {
      return this.role === "coach";
    },

    isDirector() {
      return this.role === "director";
    },
  },

  actions: {
    async login(email, password) {
      try {
        const data = await authAPI.login(email, password);
        console.log("store login data:", data);
        this.accessToken = data.access_token;
        this.tokenExpiry = Date.now() + data.expires_in * 1000;
        this.role = data.role;
        this.userId = data.user_id;
        this.userName = data.name;
        this.member_grade = data.grade ?? null;

        this.updateActivity();
        this.startInactivityTimer();

        return true;
      } catch (error) {
        console.error("ログインエラー:", error);
        throw error;
      }
    },

    async refreshAccessToken() {
      const data = await authAPI.refreshAccessToken();

      if (!data) {
        return false;
      }

      // ← ここでstateを更新
      this.accessToken = data.access_token;
      this.tokenExpiry = Date.now() + data.expires_in * 1000;

      return true;
    },

    async initAuth() {
      if (!this.maybeLoggedIn) {
        this.isInitialized = true;
        return;
      }

      const refreshed = await this.refreshAccessToken();

      if (refreshed) {
        this.startInactivityTimer();
      }

      this.isInitialized = true;
    },

    startInactivityTimer() {
      const INACTIVITY_TIMEOUT = 30 * 60 * 1000; // 30分

      this.clearInactivityTimer();

      const resetTimer = () => {
        this.updateActivity();
        if (this.inactivityTimer) clearTimeout(this.inactivityTimer);

        this.inactivityTimer = setTimeout(() => {
          console.log("無操作によりログアウトします");
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

    clearInactivityTimer() {
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer);
        this.inactivityTimer = null;
      }

      this.eventListeners.forEach(({ eventName, handler }) => {
        window.removeEventListener(eventName, handler);
      });
      this.eventListeners = [];
    },

    updateActivity() {
      this.lastActivity = Date.now();
    },

    async logout() {
      try {
        await authAPI.logout();
      } catch (e) {
        // エラー無視
      }

      this.clearInactivityTimer();
      this.accessToken = null;
      this.tokenExpiry = null;
      this.role = null;
      this.userName = null;
      this.userId = null;
      this.member_grade = null;

      // ルーティング
      router.push("/login");
    },
  },
});

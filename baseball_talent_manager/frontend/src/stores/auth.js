/**
 * stores/auth.js
 *
 * モックUI用Piniaストア
 * バックエンド実装後はauth.full.jsに差し替える
 */
import { defineStore } from "pinia";
import * as authAPI from "@/services/authService";
import router from "@/router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: null,
    role: null,
    userName: null,
    userId: null,
    memberGrade: null,
    isInitialized: false,

    roleMap: {
      manager: "マネージャー",
      member: "部員",
      coach: "コーチ",
      director: "監督",
    },
  }),

  getters: {
    // ログイン状態
    isAuthenticated(state) {
      return !!state.accessToken;
    },

    // ロール表示名
    displayRole(state) {
      return state.role ? state.roleMap[state.role] || state.role : null;
    },

    // ロール別判定
    isManager(state) {
      return state.role === "manager";
    },

    isMember(state) {
      return state.role === "member";
    },

    isCoach(state) {
      return state.role === "coach";
    },

    isDirector(state) {
      return state.role === "director";
    },
  },

  actions: {
    /**
     * ログイン
     * authService.loginを呼び出してstateに格納する
     */
    async login(email, password) {
      try {
        const data = await authAPI.login(email, password);
        this.accessToken = data.access_token;
        this.role = data.role;
        this.userId = data.user_id;
        this.userName = data.name;
        this.memberGrade = data.grade ?? null;
        return true;
      } catch (error) {
        console.error("ログインエラー:", error);
        throw error;
      }
    },

    /**
     * アプリ起動時の認証状態初期化
     * モックUI段階ではリフレッシュ不要のためシンプルな実装
     */
    async initAuth() {
      // モックUI段階ではリフレッシュ不要
      this.isInitialized = true;
    },

    /**
     * ログアウト
     * stateをリセットしてログイン画面へ遷移する
     */
    async logout() {
      try {
        await authAPI.logout();
      } catch (e) {
        // エラー無視
      }

      this.accessToken = null;
      this.role = null;
      this.userName = null;
      this.userId = null;
      this.memberGrade = null;

      router.push("/login");
    },
  },
});

// ============================================================
// stores/auth.ts  —  認証状態管理（Pinia）
// モック段階：トークンは localStorage で保持
// 本番実装時：HttpOnly Cookie に切り替える
// ============================================================

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { AuthUser } from "@/types";
import { ACCESS_TOKEN_KEY } from "@/domains/auth/constants";
import { ROLE_DEFAULT_ROUTE } from "@/constants";

export const useAuthStore = defineStore("auth", () => {
  // ── state ──────────────────────────────────────────────────
  const user = ref<AuthUser | null>(null);
  const token = ref<string | null>(localStorage.getItem(ACCESS_TOKEN_KEY));

  // ── getters ────────────────────────────────────────────────
  const isLoggedIn = computed(
    () => token.value !== null && user.value !== null,
  );

  /** ログイン後のデフォルト遷移先 */
  const defaultRoute = computed(() => {
    if (!user.value) return "/login";
    return ROLE_DEFAULT_ROUTE[user.value.role];
  });

  // ── actions ────────────────────────────────────────────────

  /**
   * ログイン処理
   * モック段階：authService から受け取った AuthUser とトークンをセットする
   */
  function login(authUser: AuthUser, accessToken: string): void {
    user.value = authUser;
    token.value = accessToken;
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  }

  /**
   * ログアウト処理
   * state・localStorage を両方クリアする
   */
  function logout(): void {
    user.value = null;
    token.value = null;
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  }

  /**
   * ページリロード時の認証状態復元
   * モック段階：localStorage のトークンからダミーユーザーを復元する
   * 本番実装時：GET /api/auth/me を呼び出してユーザー情報を取得する
   */
  function restoreSession(authUser: AuthUser): void {
    user.value = authUser;
  }

  /**
   * ユーザー情報の更新（パスワード変更後などに使用）
   */
  function updateUser(partial: Partial<AuthUser>): void {
    if (!user.value) return;
    user.value = { ...user.value, ...partial };
  }

  return {
    // state
    user,
    token,
    // getters
    isLoggedIn,
    defaultRoute,
    // actions
    login,
    logout,
    restoreSession,
    updateUser,
  };
});

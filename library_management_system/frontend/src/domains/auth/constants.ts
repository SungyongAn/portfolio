// ============================================================
// モック段階ではアクセストークンを localStorage で保持し、
// ログイン済みユーザー情報は Pinia ストアで管理する。
// 本番実装時は HttpOnly Cookie に切り替える。
// ============================================================

/** localStorage に保存するアクセストークンのキー名 */
export const ACCESS_TOKEN_KEY = 'access_token'

/** Authorizationヘッダーのプレフィックス */
export const AUTH_HEADER_PREFIX = 'Bearer '
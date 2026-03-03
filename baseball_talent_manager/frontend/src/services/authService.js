/**
 * モックUI用仮実装
 * バックエンド実装後は実際のAPI通信に差し替える
 */
import { dummyUsers } from "@/dummyData";

/**
 * ログイン
 * バックエンド実装後は POST /api/auth/login に差し替える
 *
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>} ログインレスポンス
 */
export const login = async (email, password) => {
  // バックエンド未実装のため、dummyUsersからメールアドレスで検索
  const user = dummyUsers.find((u) => u.email === email);

  if (!user) {
    throw new Error("メールアドレスまたはパスワードが正しくありません");
  }

  // バックエンドから返ってくるJSONを模倣
  return {
    access_token: "dummy_token",
    expires_in: 900, // 15分（秒）
    role: user.role,
    user_id: user.user_id,
    name: user.name,
    grade: user.grade ?? null,
  };
};

/**
 * トークン再発行
 * バックエンド実装後は POST /api/auth/refresh に差し替える
 * モックUI段階ではnullを返してリフレッシュ不要とする
 *
 * @returns {Promise<null>}
 */
export const refreshAccessToken = async () => {
  // モックUI段階ではリフレッシュ不要
  return null;
};

/**
 * ログアウト
 * バックエンド実装後は POST /api/auth/logout に差し替える
 *
 * @returns {Promise<void>}
 */
export const logout = async () => {
  // モックUI段階ではAPI通信不要
};

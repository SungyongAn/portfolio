import api from "./api";

// ユーザーの作成
export function createUser(params) {
  return api.post("/api/users", params);
}

// ユーザー情報の取得
export function getUsers(role = null) {
  return api.get("/api/users", { params: { role } });
}

// ユーザーの引退・退部処理
export function updateUserStatus(userId, status) {
  return api.patch(`/api/users/${userId}/status`, { status });
}

import api from "./api";

// AIアドバイス取得
export function getAdvice(userId) {
  return api.post(`/api/advice/${userId}`);
}

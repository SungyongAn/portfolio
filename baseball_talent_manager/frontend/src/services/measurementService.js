import api from "./api";

// 測定結果の登録
export function createMeasurement(data) {
  return api.post("/api/measurements", data);
}

// 測定結果の取得
export function getMeasurements() {
  return api.get("/api/measurements");
}

// 測定結果の部員への承認依頼
export function submitMeasurement(measurementId) {
  return api.post(`/api/measurements/${measurementId}/submit`);
}

// 測定結果の承認（部員）
export function memberApprove(measurementId, action) {
  return api.patch(`/api/measurements/${measurementId}/member-approve`, {
    action,
  });
}

// 測定結果の承認（コーチ）
export function coachApprove(measurementId, action) {
  return api.patch(`/api/measurements/${measurementId}/coach-approve`, {
    action,
  });
}

// 測定結果の全件取得
export const getAllMeasurements = () => {
  return api.get("/api/measurements/all");
};

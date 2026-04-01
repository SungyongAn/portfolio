import api from "./api";
import type { AxiosResponse } from "axios";

// ==============================
// 型定義
// ==============================

// 測定データ（仮：必要に応じて拡張）
export type Measurement = {
  id: number;
  [key: string]: any;
};

export type ApproveAction = "approve" | "reject";

// ==============================
// API
// ==============================

// 測定結果の登録
export function createMeasurement(
  data: Partial<Measurement>
): Promise<AxiosResponse<Measurement>> {
  return api.post("/api/measurements", data);
}

// 測定結果の取得
export function getMeasurements(): Promise<AxiosResponse<Measurement[]>> {
  return api.get("/api/measurements");
}

// 測定結果の部員への承認依頼
export function submitMeasurement(
  measurementId: number
): Promise<AxiosResponse<void>> {
  return api.post(`/api/measurements/${measurementId}/submit`);
}

// 測定結果の承認（部員）
export function memberApprove(
  measurementId: number,
  action: ApproveAction
): Promise<AxiosResponse<void>> {
  return api.patch(`/api/measurements/${measurementId}/member-approve`, {
    action,
  });
}

// 測定結果の承認（コーチ）
export function coachApprove(
  measurementId: number,
  action: ApproveAction
): Promise<AxiosResponse<void>> {
  return api.patch(`/api/measurements/${measurementId}/coach-approve`, {
    action,
  });
}

// 測定結果の全件取得
export function getAllMeasurements(): Promise<
  AxiosResponse<Measurement[]>
> {
  return api.get("/api/measurements/all");
}

// 測定結果の確認済みマーク（マネージャー）
export function confirmMeasurement(
  measurementId: number
): Promise<AxiosResponse<void>> {
  return api.patch(`/api/measurements/${measurementId}/confirm`);
}
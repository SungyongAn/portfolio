import api from "./api";
import type { AxiosResponse } from "axios";
import type { Role } from "@/stores/auth";

// ==============================
// 型定義
// ==============================

// ユーザー
export type User = {
  user_id: number;
  name: string;
  email: string;
  role: Role;
  status: UserStatus;
  grade: number;
  status_changed_at: string | null;
};

// ユーザー作成用
export type CreateUserParams = {
  name: string;
  email: string;
  password: string;
  role: Role;
  grade: number;
};

// ステータス（引退・退部）
export type UserStatus = "active" | "retired" | "inactive";

type UsersResponse = {
  users: User[];
};

// ==============================
// API
// ==============================

// ユーザーの作成
export function createUser(
  params: CreateUserParams,
): Promise<AxiosResponse<User>> {
  return api.post("/api/users", params);
}

// ユーザー情報の取得
export function getUsers(
  role: Role | null = null,
): Promise<AxiosResponse<UsersResponse>> {
  return api.get("/api/users", { params: { role } });
}

// ユーザーの引退・退部処理
export function updateUserStatus(
  userId: number,
  status: UserStatus,
): Promise<AxiosResponse<User>> {
  return api.patch(`/api/users/${userId}/status`, { status });
}

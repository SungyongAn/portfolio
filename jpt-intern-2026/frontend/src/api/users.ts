import apiClient from "./client";
import type { UserResponse } from "@/api/models/UserResponse";

export const usersAPI = {
  getMe() {
    return apiClient.get<UserResponse>("/api/users/me");
  },
  getUsers() {
    return apiClient.get<UserResponse[]>("/api/users");
  },
  getDepartmentUsers(departmentId: number) {
    return apiClient.get<UserResponse[]>(`/api/users/department/${departmentId}`);
  },
};

import apiClient from "./client";
import type { TaskResponse } from "@/api/models/TaskResponse";
import type { TaskCreate } from "@/api/models/TaskCreate";
import type { TaskUpdate } from "@/api/models/TaskUpdate";

export const tasksAPI = {
  getTasks(projectId: number) {
    return apiClient.get<TaskResponse[]>(`/api/projects/${projectId}/tasks`);
  },

  createTask(projectId: number, data: TaskCreate) {
    return apiClient.post<TaskResponse>(
      `/api/projects/${projectId}/tasks`,
      data,
    );
  },

  updateTask(projectId: number, taskId: number, data: TaskUpdate) {
    return apiClient.put<TaskResponse>(
      `/api/projects/${projectId}/tasks/${taskId}`,
      data,
    );
  },

  deleteTask(projectId: number, taskId: number) {
    return apiClient.delete(`/api/projects/${projectId}/tasks/${taskId}`);
  },

  getDepartmentTasks(departmentId: number) {
    return apiClient.get<TaskResponse[]>(
      `/api/departments/${departmentId}/tasks`,
    );
  },

  getAllTasks() {
    return apiClient.get<TaskResponse[]>(`/api/tasks/all`);
  },
};

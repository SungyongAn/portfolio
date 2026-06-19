import apiClient from "./client";
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import type { ProjectCreate } from "@/api/models/ProjectCreate";
import type { ApprovalRequest } from "@/api/models/ApprovalRequest";
import type { ProjectListResponse } from "@/api/models/ProjectListResponse";
import type { BudgetSummaryResponse } from "@/api/models/BudgetSummaryResponse";

export type ProjectSortBy = "budget_amount";
export type SortOrder = "asc" | "desc";

export const projectsAPI = {
  getProjects(
    page = 1,
    limit = 10,
    status?: string[],
    keyword?: string,
    departmentId?: number,
    budgetMin?: number,
    budgetMax?: number,
    sortBy?: ProjectSortBy,
    sortOrder?: SortOrder,
    alertLevel?: string,
  ) {
    const params = new URLSearchParams();
    params.append("page", String(page));
    params.append("limit", String(limit));

    if (status?.length) status.forEach((s) => params.append("status", s));
    if (keyword) params.append("keyword", keyword);

    if (departmentId != null) {
      params.append("department_id", String(departmentId));
    }

    if (budgetMin != null) params.append("budget_min", String(budgetMin));
    if (budgetMax != null) params.append("budget_max", String(budgetMax));

    if (sortBy) params.append("sort_by", sortBy);
    if (sortOrder) params.append("sort_order", sortOrder);
    if (alertLevel) params.append("alert_level", alertLevel);

    return apiClient.get<ProjectListResponse>(
      `/api/projects?${params.toString()}`,
    );
  },

  getProject(projectId: number) {
    return apiClient.get<ProjectResponse>(`/api/projects/${projectId}`);
  },

  getBudgetSummary(
    status?: string[],
    keyword?: string,
    departmentId?: number | null,
    budgetMin?: number | null,
    budgetMax?: number | null,
  ) {
    const params = new URLSearchParams();

    if (status?.length) status.forEach((s) => params.append("status", s));
    if (keyword) params.append("keyword", keyword);

    if (departmentId != null) {
      params.append("department_id", String(departmentId));
    }

    if (budgetMin != null) params.append("budget_min", String(budgetMin));
    if (budgetMax != null) params.append("budget_max", String(budgetMax));

    return apiClient.get<BudgetSummaryResponse>(
      `/api/projects/budget-summary?${params.toString()}`,
    );
  },

  createProject(data: ProjectCreate) {
    return apiClient.post<ProjectResponse>("/api/projects", data);
  },

  updateProject(projectId: number, data: Partial<ProjectCreate>) {
    return apiClient.put<ProjectResponse>(`/api/projects/${projectId}`, data);
  },

  approveProject(projectId: number, data: ApprovalRequest) {
    return apiClient.post<ProjectResponse>(
      `/api/projects/${projectId}/approve`,
      data,
    );
  },

  startProject(projectId: number) {
    return apiClient.patch<ProjectResponse>(`/api/projects/${projectId}/start`);
  },

  completeProject(projectId: number) {
    return apiClient.patch<ProjectResponse>(
      `/api/projects/${projectId}/complete`,
    );
  },
};

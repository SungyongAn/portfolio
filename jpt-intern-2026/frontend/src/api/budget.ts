import apiClient from "./client";
import type { ProjectBudgetResponse } from "@/api/models/ProjectBudgetResponse";
import type { WorklogResponse } from "@/api/models/WorklogResponse";
import type { WorklogCreate } from "@/api/models/WorklogCreate";
import type { ExpenseResponse } from "@/api/models/ExpenseResponse";
import type { ExpenseCreate } from "@/api/models/ExpenseCreate";

export type BudgetCreate = {
  budget_amount: number;
  unit_price?: number;
  planned_months?: number;
};

export const budgetAPI = {
  getBudget(projectId: number) {
    return apiClient.get<ProjectBudgetResponse>(
      `/api/projects/${projectId}/budget`,
    );
  },

  createBudget(projectId: number, data: BudgetCreate) {
    return apiClient.post<ProjectBudgetResponse>(
      `/api/projects/${projectId}/budget`,
      data,
    );
  },

  getWorklogs(projectId: number) {
    return apiClient.get<WorklogResponse[]>(
      `/api/projects/${projectId}/worklogs`,
    );
  },

  createWorklog(projectId: number, data: WorklogCreate) {
    return apiClient.post<WorklogResponse>(
      `/api/projects/${projectId}/worklogs`,
      data,
    );
  },

  updateWorklog(
    projectId: number,
    worklogId: number,
    data: { actual_months: string },
  ) {
    return apiClient.put<WorklogResponse>(
      `/api/projects/${projectId}/worklogs/${worklogId}`,
      data,
    );
  },

  deleteWorklog(projectId: number, worklogId: number) {
    return apiClient.delete(`/api/projects/${projectId}/worklogs/${worklogId}`);
  },

  getExpenses(projectId: number) {
    return apiClient.get<ExpenseResponse[]>(
      `/api/projects/${projectId}/expenses`,
    );
  },

  createExpense(projectId: number, data: ExpenseCreate) {
    return apiClient.post<ExpenseResponse>(
      `/api/projects/${projectId}/expenses`,
      data,
    );
  },

  updateExpense(
    projectId: number,
    expenseId: number,
    data: Partial<ExpenseCreate>,
  ) {
    return apiClient.put<ExpenseResponse>(
      `/api/projects/${projectId}/expenses/${expenseId}`,
      data,
    );
  },

  deleteExpense(projectId: number, expenseId: number) {
    return apiClient.delete(`/api/projects/${projectId}/expenses/${expenseId}`);
  },
};
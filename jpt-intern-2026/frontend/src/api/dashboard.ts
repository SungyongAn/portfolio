import apiClient from "./client";

export type AlertLevel = "danger" | "warning" | null;

export type DashboardSummary = {
  unreadNotifications: number;
  pendingApprovals: number;
  inProgressProjects: number;
  completedProjects: number;
  dangerProjects: number;
  warningProjects: number;
  budgetWarningCount: number;

  totalProjects: number;
  totalBudget: number;
  totalActual: number;
  totalConsumptionRate: number;
  activeProjects: number;
  completedProjectCount: number;
  pendingApprovalCount: number;
  riskProjectCount: number;

  overdueTasks?: number;
  lowSpiProjects?: number;
  lowCpiProjects?: number;
  overdueTaskCount?: number;
};

export type StatusSummary = {
  draft: number;
  pending_dept: number;
  pending_hq: number;
  approved: number;
  in_progress: number;
  completed: number;
  rejected: number;
};

export type DepartmentSummary = {
  department_id: number;
  department_name: string;
  project_count: number;
  active_project_count: number;
  completed_project_count: number;
  budget_amount: number;
  actual_amount: number;
  consumption_rate: number;
  danger_projects: number;
  warning_projects: number;
  overdue_task_count: number;
};

export type OwnerSummary = {
  owner_id: number;
  owner_name: string;
  project_count: number;
  active_project_count: number;
  danger_projects: number;
  warning_projects: number;
  budget_amount: number;
  actual_amount: number;
  consumption_rate: number;
};

export type ProjectDashboard = {
  id: number;
  name: string;
  status: string;
  department_id: number;
  department_name: string | null;
  owner_id: number;
  owner_name: string | null;
  budget_amount: number;
  actual_amount: number;
  consumption_rate: number;
  progress: number;
  schedule_rate: number;
  overdue_task_count: number;
  alert_level: AlertLevel;
  alert_reason: string | null;
  spi: number | null;
  cpi: number | null;
  created_at?: string | null;
};

export type RiskProject = ProjectDashboard;

export type TaskSummary = {
  total_tasks: number;
  todo: number;
  in_progress: number;
  in_review: number;
  done: number;
  overdue: number;
  today_deadline: number;
};

export type TaskDashboardItem = {
  id: number;
  name: string;
  status: string;
  progress: number;
  project_id: number;
  project_name: string | null;
  department_name: string | null;
  assignee_name: string | null;
  start_date: string | null;
  due_date: string | null;
  priority: "danger" | "warning" | "normal";
};

export type ApplicantSummary = {
  draft: number;
  pending: number;
  approved: number;
  inProgress: number;
  completed: number;
  rejected: number;
};

export type DashboardResponse = {
  role: string;
  summary: DashboardSummary;
  statusSummary: StatusSummary;
  departments: DepartmentSummary[];
  owners: OwnerSummary[];
  riskProjects: RiskProject[];
  projects: ProjectDashboard[];

  taskSummary?: TaskSummary;
  tasks?: TaskDashboardItem[];
  applicantSummary?: ApplicantSummary;
};

export type ProjectListResponse = {
  items: ProjectDashboard[];
  total: number;
  page: number;
  limit: number;
};

export type ProjectListParams = {
  page: number;
  limit: number;
  keyword?: string;
  status?: string;
};

export const dashboardAPI = {
  getDashboard() {
    return apiClient.get<DashboardResponse>("/api/dashboard");
  },

  getAlerts() {
    return apiClient.get<RiskProject[]>("/api/dashboard/alerts");
  },

  getProjects(params: ProjectListParams) {
    const query = new URLSearchParams();

    query.set("page", String(params.page));
    query.set("limit", String(params.limit));

    if (params.keyword) {
      query.set("keyword", params.keyword);
    }

    if (params.status) {
      query.set("status", params.status);
    }

    return apiClient.get<ProjectListResponse>(
      `/api/projects?${query.toString()}`,
    );
  },
};

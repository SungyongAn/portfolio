export interface DepartmentSummary {
  department_id: number;
  department_name: string;

  project_count: number;

  budget_amount: number;
  actual_amount: number;

  consumption_rate: number;

  danger_projects: number;
}

export interface RiskProject {
  id: number;

  name: string;

  department_name: string;

  owner_name: string;

  progress: number;

  consumption_rate: number;

  alert_level: "danger" | "warning";
}

export interface DashboardSummary {
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
}

export interface ApplicantSummary {
  pending: number;

  in_progress: number;

  completed: number;
}

export interface TaskMemberSummary {
  todo: number;

  in_progress: number;

  in_review: number;

  done: number;
}

export interface DashboardResponse {
  role: string;

  summary: DashboardSummary;

  departments?: DepartmentSummary[];

  risk_projects?: RiskProject[];

  applicant_summary?: ApplicantSummary;

  task_summary?: TaskMemberSummary;
}

export type ManagementFilter =
  | "default"
  | "pending"
  | "active"
  | "danger"
  | "warning"
  | "budget";

export type DashboardMode =
  | "summary"
  | "pending"
  | "active"
  | "danger"
  | "warning"
  | "budget"
  | "projects";

export type SummaryData = DashboardSummary & {
  overdueTasks?: number;
  lowSpiProjects?: number;
  lowCpiProjects?: number;
  overdueTaskCount?: number;
};

export type DashboardViewMode =
  | "summary"
  | "approval"
  | "danger"
  | "warning"
  | "projects";

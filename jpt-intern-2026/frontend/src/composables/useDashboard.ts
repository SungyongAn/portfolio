import { ref, computed, onMounted } from "vue";
import { dashboardAPI } from "@/api/dashboard";

import type {
  DepartmentSummary,
  OwnerSummary,
  ProjectDashboard,
  RiskProject,
  StatusSummary,
  TaskDashboardItem,
  TaskSummary,
  ApplicantSummary,
} from "@/api/dashboard";

import type { DashboardViewMode } from "@/types/dashboard";

interface SummaryData {
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

  overdueTasks: number;
  lowSpiProjects: number;
  lowCpiProjects: number;
  overdueTaskCount: number;
}

interface ProjectListState {
  items: ProjectDashboard[];
  total: number;
  page: number;
  limit: number;
}

const initialSummaryData = (): SummaryData => ({
  unreadNotifications: 0,
  pendingApprovals: 0,

  inProgressProjects: 0,
  completedProjects: 0,

  dangerProjects: 0,
  warningProjects: 0,
  budgetWarningCount: 0,

  totalProjects: 0,
  totalBudget: 0,
  totalActual: 0,
  totalConsumptionRate: 0,

  activeProjects: 0,
  completedProjectCount: 0,
  pendingApprovalCount: 0,
  riskProjectCount: 0,

  overdueTasks: 0,
  lowSpiProjects: 0,
  lowCpiProjects: 0,
  overdueTaskCount: 0,
});

const initialProjectList = (): ProjectListState => ({
  items: [],
  total: 0,
  page: 1,
  limit: 10,
});

export function useDashboard() {
  const loading = ref(false);
  const projectListLoading = ref(false);

  const role = ref<string>("");

  const projectDashboard = ref<ProjectDashboard[]>([]);
  const projectList = ref<ProjectListState>(initialProjectList());

  const riskProjects = ref<RiskProject[]>([]);
  const departments = ref<DepartmentSummary[]>([]);
  const owners = ref<OwnerSummary[]>([]);
  const statusSummary = ref<StatusSummary | null>(null);

  const taskSummary = ref<TaskSummary | null>(null);
  const tasks = ref<TaskDashboardItem[]>([]);
  const applicantSummary = ref<ApplicantSummary | null>(null);

  const openPanels = ref<number[]>([]);
  const summaryData = ref<SummaryData>(initialSummaryData());

  const selectedDashboardView = ref<DashboardViewMode>("summary");

  const sortedProjectDashboard = computed(() => {
    return [...projectDashboard.value].sort(
      (a, b) => priority(a) - priority(b),
    );
  });

  const priority = (project: ProjectDashboard): number => {
    if (project.alert_level === "danger") {
      return 0;
    }

    if (project.alert_level === "warning") {
      return 1;
    }

    if ((project.consumption_rate ?? 0) >= 80) {
      return 2;
    }

    return 3;
  };

  const setDashboardView = (view: DashboardViewMode) => {
    selectedDashboardView.value = view;
    resetPanels();
  };

  const resetDashboardView = () => {
    selectedDashboardView.value = "summary";
    resetPanels();
  };

  const isPanelOpen = (id: number) => {
    return openPanels.value.includes(id);
  };

  const togglePanel = (id: number) => {
    const index = openPanels.value.indexOf(id);

    if (index === -1) {
      openPanels.value.push(id);
      return;
    }

    openPanels.value.splice(index, 1);
  };

  const resetPanels = () => {
    openPanels.value = [];
  };

  const fetchDashboard = async () => {
    loading.value = true;

    try {
      const dashboardRes = await dashboardAPI.getDashboard();
      const dashboard = dashboardRes.data;

      role.value = dashboard.role;

      projectDashboard.value = dashboard.projects ?? [];
      riskProjects.value = dashboard.riskProjects ?? [];
      departments.value = dashboard.departments ?? [];
      owners.value = dashboard.owners ?? [];
      statusSummary.value = dashboard.statusSummary ?? null;

      taskSummary.value = dashboard.taskSummary ?? null;
      tasks.value = dashboard.tasks ?? [];
      applicantSummary.value = dashboard.applicantSummary ?? null;

      summaryData.value = {
        ...initialSummaryData(),

        unreadNotifications: dashboard.summary.unreadNotifications ?? 0,

        pendingApprovals: dashboard.summary.pendingApprovals ?? 0,
        inProgressProjects: dashboard.summary.inProgressProjects ?? 0,
        completedProjects: dashboard.summary.completedProjects ?? 0,
        dangerProjects: dashboard.summary.dangerProjects ?? 0,
        warningProjects: dashboard.summary.warningProjects ?? 0,
        budgetWarningCount: dashboard.summary.budgetWarningCount ?? 0,

        totalProjects: dashboard.summary.totalProjects ?? 0,
        totalBudget: dashboard.summary.totalBudget ?? 0,
        totalActual: dashboard.summary.totalActual ?? 0,
        totalConsumptionRate: dashboard.summary.totalConsumptionRate ?? 0,

        activeProjects: dashboard.summary.activeProjects ?? 0,
        completedProjectCount: dashboard.summary.completedProjectCount ?? 0,
        pendingApprovalCount: dashboard.summary.pendingApprovalCount ?? 0,
        riskProjectCount: dashboard.summary.riskProjectCount ?? 0,

        overdueTasks: dashboard.summary.overdueTasks ?? 0,
        lowSpiProjects: dashboard.summary.lowSpiProjects ?? 0,
        lowCpiProjects: dashboard.summary.lowCpiProjects ?? 0,
        overdueTaskCount: dashboard.summary.overdueTaskCount ?? 0,
      };

      resetPanels();
    } catch (error) {
      console.error("ダッシュボード取得失敗", error);
    } finally {
      loading.value = false;
    }
  };

  const fetchDashboardProjects = async (
    page = 1,
    limit = 10,
    keyword = "",
    status = "",
  ) => {
    projectListLoading.value = true;

    try {
      const res = await dashboardAPI.getProjects({
        page,
        limit,
        keyword: keyword || undefined,
        status: status || undefined,
      });

      projectList.value = {
        items: res.data.items ?? [],
        total: res.data.total ?? 0,
        page: res.data.page ?? page,
        limit: res.data.limit ?? limit,
      };
    } catch (error) {
      console.error("案件一覧取得失敗", error);

      projectList.value = {
        ...projectList.value,
        items: [],
        total: 0,
      };
    } finally {
      projectListLoading.value = false;
    }
  };

  onMounted(() => {
    fetchDashboard();
    fetchDashboardProjects();
  });

  return {
    loading,
    projectListLoading,
    role,

    projectDashboard,
    projectList,
    sortedProjectDashboard,
    riskProjects,
    departments,
    owners,
    statusSummary,

    taskSummary,
    tasks,
    applicantSummary,

    summaryData,

    selectedDashboardView,
    setDashboardView,
    resetDashboardView,

    openPanels,
    isPanelOpen,
    togglePanel,
    resetPanels,

    fetchDashboard,
    fetchDashboardProjects,
  };
}

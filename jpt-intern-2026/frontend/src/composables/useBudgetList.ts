import { onMounted, ref } from "vue";
import { watchDebounced } from "@vueuse/core";
import { projectsAPI } from "@/api/projects";
import { departmentsAPI, type Department } from "@/api/departments";
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import type { ProjectStatus } from "@/api/models/ProjectStatus";

type BudgetFilter = "low" | "mid" | "high" | null;
type SortBy = "budget_amount" | null;
type SortOrder = "asc" | "desc";

type BudgetSummary = {
  total_projects: number;
  total_budget: number;
  total_actual: number;
  avg_consumption_rate: number;
};

export const useBudgetList = () => {
  const loading = ref(false);

  const projects = ref<ProjectResponse[]>([]);
  const departments = ref<Department[]>([]);

  const total = ref(0);
  const currentPage = ref(1);
  const pageSize = ref(10);

  const keyword = ref("");
  const statusFilter = ref<string>("");
  const departmentFilter = ref<number | null>(null);
  const budgetFilter = ref<BudgetFilter>(null);

  const sortBy = ref<SortBy>(null);
  const sortOrder = ref<SortOrder>("desc");

  const summary = ref<BudgetSummary>({
    total_projects: 0,
    total_budget: 0,
    total_actual: 0,
    avg_consumption_rate: 0,
  });

  const getBudgetRange = () => {
    switch (budgetFilter.value) {
      case "low":
        return { min: null, max: 5_000_000 };
      case "mid":
        return { min: 5_000_000, max: 10_000_000 };
      case "high":
        return { min: 10_000_000, max: null };
      default:
        return { min: null, max: null };
    }
  };

  const fetchDepartments = async () => {
    try {
      const deptRes = await departmentsAPI.getDepartments();
      departments.value = deptRes.data;
    } catch (error) {
      console.error("部門データ取得失敗", error);
    }
  };

  const fetchData = async () => {
    loading.value = true;

    try {
      const statusList = statusFilter.value
        ? [statusFilter.value as ProjectStatus]
        : undefined;

      const { min, max } = getBudgetRange();

      const [projectsRes, summaryRes] = await Promise.all([
        projectsAPI.getProjects(
          currentPage.value,
          pageSize.value,
          statusList,
          keyword.value || undefined,
          departmentFilter.value ?? undefined,
          min ?? undefined,
          max ?? undefined,
          sortBy.value ?? undefined,
          sortOrder.value,
        ),
        projectsAPI.getBudgetSummary(
          statusList,
          keyword.value || undefined,
          departmentFilter.value,
          min,
          max,
        ),
      ]);

      projects.value = projectsRes.data.items;
      total.value = projectsRes.data.total;
      summary.value = summaryRes.data;
    } catch (error) {
      console.error("データ取得失敗", error);
    } finally {
      loading.value = false;
    }
  };

  const handleSortChange = ({
    prop,
    order,
  }: {
    prop: string;
    order: "ascending" | "descending" | null;
  }) => {
    currentPage.value = 1;

    if (prop === "budget_amount" && order) {
      sortBy.value = "budget_amount";
      sortOrder.value = order === "ascending" ? "asc" : "desc";
    } else {
      sortBy.value = null;
      sortOrder.value = "desc";
    }

    fetchData();
  };

  const handlePageChange = (page: number) => {
    currentPage.value = page;
    fetchData();
  };

  onMounted(async () => {
    await fetchDepartments();
    fetchData();
  });

  watchDebounced(
    () => [
      keyword.value,
      statusFilter.value,
      departmentFilter.value,
      budgetFilter.value,
    ],
    () => {
      currentPage.value = 1;
      fetchData();
    },
    { debounce: 300 },
  );

  return {
    loading,
    projects,
    departments,
    total,
    currentPage,
    pageSize,
    keyword,
    statusFilter,
    departmentFilter,
    budgetFilter,
    summary,
    fetchData,
    handleSortChange,
    handlePageChange,
  };
};

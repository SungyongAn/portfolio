import { computed, ref } from "vue";
import type { ProjectDashboard } from "@/api/dashboard";
import type { ManagementFilter } from "@/types/dashboard";

export function useManagementDashboard(
  defaultProjects: () => ProjectDashboard[],
  projects: () => ProjectDashboard[],
) {
  const selectedFilter = ref<ManagementFilter>("default");

  const filteredProjects = computed(() => {
    const items = projects();

    switch (selectedFilter.value) {
      case "pending":
        return items.filter((project) =>
          ["PENDING_DEPT", "PENDING_HQ"].includes(project.status),
        );

      case "active":
        return items.filter((project) =>
          ["APPROVED", "IN_PROGRESS"].includes(project.status),
        );

      case "danger":
        return items.filter(
          (project) =>
            ["APPROVED", "IN_PROGRESS"].includes(project.status) &&
            project.alert_level === "danger",
        );

      case "warning":
        return items.filter(
          (project) =>
            ["APPROVED", "IN_PROGRESS"].includes(project.status) &&
            project.alert_level === "warning",
        );

      case "budget":
        return items.filter(
          (project) =>
            ["APPROVED", "IN_PROGRESS"].includes(project.status) &&
            (project.consumption_rate ?? 0) >= 80,
        );

      default:
        return defaultProjects();
    }
  });

  const showCharts = computed(() => selectedFilter.value === "default");

  const resetFilter = () => {
    selectedFilter.value = "default";
  };

  return {
    selectedFilter,
    filteredProjects,
    showCharts,
    resetFilter,
  };
}

<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>{{ pageTitle }}</h1>
    </div>

    <!-- 本部管理者：部門切替 -->
    <div v-if="role === 'HQ_MANAGER'" class="department-tabs">
      <el-button
        :type="selectedDepartmentId === null ? 'primary' : 'default'"
        @click="selectedDepartmentId = null"
      >
        全社
      </el-button>

      <el-button
        v-for="department in departments"
        :key="department.department_id"
        :type="
          selectedDepartmentId === department.department_id
            ? 'primary'
            : 'default'
        "
        @click="selectedDepartmentId = department.department_id"
      >
        {{ department.department_name }}
      </el-button>
    </div>

    <!-- 担当者 -->
    <TaskMemberDashboard
      v-if="role === 'TASK_MEMBER'"
      :summary="taskSummary"
      :tasks="tasks"
      :loading="loading"
      :active-panel="taskMemberPanel"
      @change-panel="taskMemberPanel = $event"
      @move="moveProjectDetail"
    />

    <!-- 申請者 -->
    <ApplicantDashboard
      v-if="role === 'APPLICANT'"
      :summary="summaryData"
      :applicant-summary="applicantSummary"
      :projects="projectDashboard"
      :loading="loading"
      :active-panel="applicantPanel"
      @change-panel="applicantPanel = $event"
      @move="moveProjectDetail"
    />

    <!-- 管理者 -->
    <template v-if="role !== 'TASK_MEMBER' && role !== 'APPLICANT'">
      <DashboardSummaryCards
        :summary="summaryData"
        @select-filter="handleSelectFilter"
      />

      <ManagementCharts
        v-if="!isProjectListMode && showManagementCharts"
        :departments="filteredDepartments"
        @select-department="selectedDepartmentId = $event"
      />

      <DashboardContentPanel
        :mode="dashboardMode"
        :projects="isProjectListMode ? projectList.items : contentProjects"
        :total="isProjectListMode ? projectList.total : contentProjects.length"
        :loading="loading || projectListLoading"
        @back="resetDashboardView"
        @open-project="moveProjectDetail"
        @open-approval="moveApproval"
        @page-change="fetchDashboardProjects"
      />
    </template>

    <ProjectCreateDrawer
      v-model="projectCreateDrawerVisible"
      @created="fetchDashboardProjects"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useDashboard } from "@/composables/useDashboard";
import { useDashboardActions } from "@/composables/useDashboardActions";
import { useManagementDashboard } from "@/composables/useManagementDashboard";

import DashboardSummaryCards from "@/components/dashboard/DashboardSummaryCards.vue";
import DashboardContentPanel from "@/components/dashboard/DashboardContentPanel.vue";
import ApplicantDashboard from "@/components/dashboard/applicant/ApplicantDashboard.vue";
import TaskMemberDashboard from "@/components/dashboard/task-member/TaskMemberDashboard.vue";
import ManagementCharts from "@/components/dashboard/management/ManagementCharts.vue";
import ProjectCreateDrawer from "@/components/projects/ProjectCreateDrawer.vue";

import type { DashboardMode, ManagementFilter } from "@/types/dashboard";

type SummaryCardFilter = ManagementFilter | "projects";

const route = useRoute();
const router = useRouter();

const selectedDepartmentId = ref<number | null>(null);
const selectedView = ref<DashboardMode>("summary");
const taskMemberPanel = ref<"tasks" | "projects">("tasks");
const applicantPanel = ref<"summary" | "projects">("summary");
const projectCreateDrawerVisible = ref(false);

const isProjectListMode = computed(() => selectedView.value === "projects");

const {
  loading,
  projectListLoading,

  role,

  summaryData,
  riskProjects,
  projectDashboard,

  projectList,

  applicantSummary,
  taskSummary,
  tasks,
  departments,

  fetchDashboardProjects,
} = useDashboard();

const { moveProjectDetail } = useDashboardActions();

const moveApproval = (projectId: number) => {
  router.push(`/projects/${projectId}/approval`);
};

const filteredDepartments = computed(() => {
  if (selectedDepartmentId.value === null) {
    return departments.value;
  }

  return departments.value.filter(
    (department) => department.department_id === selectedDepartmentId.value,
  );
});

const filteredRiskProjects = computed(() => {
  if (selectedDepartmentId.value === null) {
    return riskProjects.value;
  }

  return riskProjects.value.filter(
    (project) => project.department_id === selectedDepartmentId.value,
  );
});

const departmentFilteredProjects = computed(() => {
  if (selectedDepartmentId.value === null) {
    return projectDashboard.value;
  }

  return projectDashboard.value.filter(
    (project) => project.department_id === selectedDepartmentId.value,
  );
});

const {
  selectedFilter: selectedManagementFilter,
  filteredProjects: managementProjects,
  showCharts: showManagementCharts,
  resetFilter: resetManagementFilter,
} = useManagementDashboard(
  () => filteredRiskProjects.value,
  () => departmentFilteredProjects.value,
);

const dashboardMode = computed<DashboardMode>(() => {
  if (selectedView.value === "projects") {
    return "projects";
  }

  if (
    !selectedManagementFilter.value ||
    selectedManagementFilter.value === "default"
  ) {
    return "summary";
  }

  return selectedManagementFilter.value as DashboardMode;
});

const contentProjects = computed(() => {
  if (dashboardMode.value === "projects") {
    return departmentFilteredProjects.value;
  }

  return managementProjects.value;
});

const handleSelectFilter = (filter: SummaryCardFilter) => {
  if (filter === "projects") {
    selectedView.value = "projects";
    resetManagementFilter();
    return;
  }

  selectedView.value = "summary";
  selectedManagementFilter.value = filter;
};

const resetDashboardView = () => {
  selectedView.value = "summary";
  resetManagementFilter();
};

watch(
  [() => route.query.view, () => route.query.action, role],
  ([view, action, currentRole]) => {
    projectCreateDrawerVisible.value =
      currentRole === "APPLICANT" && action === "create-project";

    if (currentRole === "TASK_MEMBER") {
      taskMemberPanel.value = view === "projects" ? "projects" : "tasks";
      return;
    }

    if (currentRole === "APPLICANT") {
      applicantPanel.value = view === "projects" ? "projects" : "summary";
      return;
    }

    if (view === "projects") {
      selectedView.value = "projects";
      resetManagementFilter();
      return;
    }

    taskMemberPanel.value = "tasks";
    applicantPanel.value = "summary";
    selectedView.value = "summary";
  },
  { immediate: true },
);

watch(projectCreateDrawerVisible, async (visible) => {
  if (visible) return;
  if (route.query.action !== "create-project") return;

  const { action, ...query } = route.query;

  await router.replace({
    path: route.path,
    query,
  });
});

const pageTitle = computed(() => {
  if (role.value === "TASK_MEMBER") {
    return "担当者ダッシュボード";
  }

  if (role.value === "APPLICANT") {
    return "申請者ダッシュボード";
  }

  return "開発案件状況ダッシュボード";
});
</script>

<style scoped>
.dashboard {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.page-header p {
  margin: 6px 0 0;
  font-size: 13px;
  color: #909399;
}

.department-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
</style>

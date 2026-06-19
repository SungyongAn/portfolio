<template>
  <div class="project-detail-view">
    <div class="page-header">
      <div>
        <h1>案件詳細</h1>
        <p>案件情報・タスク・予算状況を確認できます</p>
      </div>

      <div class="header-actions">
        <el-button @click="router.back()">戻る</el-button>
        <el-button
          v-if="canEditProject"
          type="primary"
          @click="router.push(`/projects/${projectId}/edit`)"
        >
          編集
        </el-button>
      </div>
    </div>

    <el-skeleton v-if="loading" :rows="8" animated />

    <el-alert
      v-else-if="errorMessage"
      type="error"
      :title="errorMessage"
      show-icon
      :closable="false"
    />

    <template v-else-if="project">
      <div class="detail-layout">
        <ProjectInfoCard :project="project" />

        <ProjectTaskCard
          :tasks="tasks"
          :can-create-task="canEditTask"
          @create-task="goToTaskCreate"
          @open-task="openTaskDetail"
        />

        <ProjectBudgetSummaryCard
          :budget="budget"
          :can-open-budget="canViewBudget"
          @open-budget="goToBudgetDetail"
        />
      </div>

      <TaskDetailDialog
        v-model="taskDetailDialogVisible"
        :task="selectedTask"
        :project-id="projectId"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import ProjectInfoCard from "@/components/projects/detail/ProjectInfoCard.vue";
import ProjectTaskCard from "@/components/projects/detail/ProjectTaskCard.vue";
import ProjectBudgetSummaryCard from "@/components/projects/detail/ProjectBudgetSummaryCard.vue";
import TaskDetailDialog from "@/components/tasks/TaskDetailDialog.vue";

import { projectsAPI } from "@/api/projects";
import { tasksAPI } from "@/api/tasks";
import { budgetAPI } from "@/api/budget";
import { useAuthStore } from "@/stores/auth";
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import type { TaskResponse } from "@/api/models/TaskResponse";
import type { ProjectBudgetResponse } from "@/api/models/ProjectBudgetResponse";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const project = ref<ProjectResponse | null>(null);
const tasks = ref<TaskResponse[]>([]);
const budget = ref<ProjectBudgetResponse | null>(null);
const loading = ref(false);
const errorMessage = ref("");

const selectedTask = ref<TaskResponse | null>(null);
const taskDetailDialogVisible = ref(false);

const projectId = computed(() => Number(route.params.projectId));

const role = computed(() => authStore.role);

const canEditProject = computed(() => {
  return ["APPLICANT", "DEPT_MANAGER", "HQ_MANAGER"].includes(role.value ?? "");
});

const canEditTask = computed(() => {
  return ["APPLICANT", "DEPT_MANAGER", "HQ_MANAGER", "TASK_MEMBER"].includes(
    role.value ?? "",
  );
});

const canViewBudget = computed(() => {
  return ["APPLICANT", "DEPT_MANAGER", "HQ_MANAGER"].includes(role.value ?? "");
});

const fetchDetail = async () => {
  if (!projectId.value || Number.isNaN(projectId.value)) {
    errorMessage.value = "案件IDが不正です";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  try {
    const [projectRes, taskRes] = await Promise.all([
      projectsAPI.getProject(projectId.value),
      tasksAPI.getTasks(projectId.value),
    ]);

    project.value = projectRes.data;
    tasks.value = taskRes.data ?? [];

    try {
      const budgetRes = await budgetAPI.getBudget(projectId.value);
      budget.value = budgetRes.data ?? null;
    } catch (budgetError: any) {
      if (budgetError?.status === 404) {
        budget.value = null;
      } else {
        console.error(budgetError);
      }
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = "案件詳細の取得に失敗しました";
    ElMessage.error(errorMessage.value);
  } finally {
    loading.value = false;
  }
};

const openTaskDetail = (task: TaskResponse) => {
  selectedTask.value = task;
  taskDetailDialogVisible.value = true;
};

const goToTaskCreate = () => {
  router.push(`/projects/${projectId.value}/tasks/new`);
};

const goToBudgetDetail = () => {
  router.push(`/projects/${projectId.value}/budget`);
};

onMounted(() => {
  fetchDetail();
});
</script>

<style scoped>
.project-detail-view {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.page-header p {
  margin: 6px 0 0;
  color: #64748b;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.detail-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

@media (max-width: 768px) {
  .project-detail-view {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions .el-button {
    flex: 1;
  }
}
</style>

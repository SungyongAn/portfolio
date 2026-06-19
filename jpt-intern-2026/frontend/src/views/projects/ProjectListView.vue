<template>
  <div class="project-list-view">
    <div class="page-header">
      <div>
        <h1>案件一覧</h1>
        <p>案件の検索・絞り込み・詳細確認を行えます</p>
      </div>

      <el-button
        v-if="canCreateProject"
        type="primary"
        @click="router.push('/projects/new')"
      >
        新規案件申請
      </el-button>
    </div>

    <ProjectListPanel
      :initial-status="initialStatus"
      :initial-alert-level="initialAlertLevel"
      :initial-department-id="initialDepartmentId"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import ProjectListPanel from "@/components/projects/ProjectListPanel.vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const canCreateProject = computed(() => authStore.role === "APPLICANT");

const initialStatus = computed(() => {
  const status = route.query.status;

  if (typeof status !== "string" || !status) {
    return "";
  }

  return status;
});

const initialAlertLevel = computed(() => {
  const alertLevel = route.query.alertLevel;

  if (typeof alertLevel !== "string" || !alertLevel) {
    return "";
  }

  return alertLevel;
});

const initialDepartmentId = computed(() => {
  const departmentId = route.query.departmentId;

  if (typeof departmentId !== "string" || !departmentId) {
    return null;
  }

  const parsed = Number(departmentId);
  return Number.isNaN(parsed) ? null : parsed;
});
</script>

<style scoped>
.project-list-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
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

@media (max-width: 768px) {
  .project-list-view {
    padding: 16px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>

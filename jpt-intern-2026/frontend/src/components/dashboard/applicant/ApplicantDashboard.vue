<template>
  <div class="applicant-dashboard">
    <ApplicantSummaryCards
      :summary="summary"
      :applicant-summary="applicantSummary"
      @select-filter="selectedFilter = $event"
    />

    <ApplicantProjectTable
      v-if="activePanel === 'summary'"
      :projects="projects"
      :loading="loading"
      :filter="selectedFilter"
      @move="emit('move', $event)"
      @reset-filter="resetFilter"
    />

    <el-card v-else shadow="never" class="project-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">案件一覧</div>
            <div class="section-subtitle">自分が申請した案件を確認できます</div>
          </div>

          <el-button
            type="primary"
            plain
            round
            size="small"
            @click="emit('change-panel', 'summary')"
          >
            ↺ ダッシュボードへ戻る
          </el-button>
        </div>
      </template>

      <ProjectListPanel embedded />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import type {
  ApplicantSummary,
  DashboardSummary,
  ProjectDashboard,
} from "@/api/dashboard";

import ApplicantSummaryCards from "./ApplicantSummaryCards.vue";
import ApplicantProjectTable from "./ApplicantProjectTable.vue";

import ProjectListPanel from "@/components/projects/ProjectListPanel.vue";

type ApplicantFilter =
  | "active"
  | "pending"
  | "draft"
  | "rejected"
  | "risk"
  | "budget";

defineProps<{
  summary: DashboardSummary;
  applicantSummary: ApplicantSummary | null;
  projects: ProjectDashboard[];
  loading: boolean;
  activePanel: "summary" | "projects";
}>();

const emit = defineEmits<{
  (e: "move", projectId: number): void;
  (e: "change-panel", panel: "summary" | "projects"): void;
}>();

const selectedFilter = ref<ApplicantFilter>("active");

const resetFilter = () => {
  selectedFilter.value = "active";
};
</script>

<style scoped>
.applicant-dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-card {
  border-radius: 12px;
  border: 1px solid #dcdfe6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
}

.section-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}
</style>

<template>
  <el-card class="project-info-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>案件情報</span>

        <el-button
          v-if="canComplete"
          type="success"
          @click="$emit('complete-project')"
        >
          完了にする
        </el-button>
      </div>
    </template>

    <el-descriptions :column="3" border class="project-descriptions">
      <el-descriptions-item label="案件名" :span="3">
        {{ project.name }}
      </el-descriptions-item>

      <el-descriptions-item label="ステータス">
        <el-tag :type="statusTagType" effect="light">
          {{ statusLabel }}
        </el-tag>
      </el-descriptions-item>

      <el-descriptions-item label="概算予算（円）">
        {{ formatCurrency(project.budget_amount) }}
      </el-descriptions-item>

      <el-descriptions-item label="概算工数（人月）">
        {{ project.planned_months ?? "-" }} 人月
      </el-descriptions-item>

      <el-descriptions-item label="開発開始予定日">
        {{ formatDate(project.start_date) }}
      </el-descriptions-item>

      <el-descriptions-item label="完了予定日">
        {{ formatDate(project.end_date) }}
      </el-descriptions-item>

      <el-descriptions-item label="進捗率">
        <div class="progress-cell">
          <el-progress
            :percentage="project.progress"
            :stroke-width="8"
            :show-text="false"
          />
          <span>{{ project.progress }}%</span>
        </div>
      </el-descriptions-item>
    </el-descriptions>

    <div class="description-section">
      <h3>目的・概要</h3>
      <p>{{ project.description || "-" }}</p>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";

import type { ProjectResponse } from "@/api/models/ProjectResponse";
import {
  PROJECT_STATUS_LABEL,
  PROJECT_STATUS_TAG_TYPE,
} from "@/constants/project";

const props = defineProps<{
  project: ProjectResponse;
  canComplete?: boolean;
}>();

defineEmits<{
  (e: "complete-project"): void;
}>();

const statusLabel = computed(() => {
  return PROJECT_STATUS_LABEL[props.project.status];
});

const statusTagType = computed(() => {
  return PROJECT_STATUS_TAG_TYPE[props.project.status];
});

const formatDate = (value?: string | null) => {
  if (!value) return "-";
  return new Date(value).toLocaleDateString("ja-JP");
};

const formatCurrency = (value?: number | null) => {
  if (value == null) return "-";
  return `${value.toLocaleString("ja-JP")} 円`;
};
</script>

<style scoped>
.project-info-card {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.project-descriptions {
  margin-bottom: 20px;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-cell :deep(.el-progress) {
  flex: 1;
  min-width: 80px;
}

.description-section h3 {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 700;
}

.description-section p {
  margin: 0;
  line-height: 1.8;
  color: #334155;
  white-space: pre-wrap;
}
</style>

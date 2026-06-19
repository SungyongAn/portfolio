<template>
  <el-card shadow="never" class="project-card" v-loading="loading">
    <template #header>
      <div class="section-header">
        <div>
          <div class="section-title">
            {{ tableTitle }}
          </div>
          <div class="section-subtitle">
            {{ tableDescription }}
          </div>
        </div>

        <el-button
          v-if="filter !== 'active'"
          type="primary"
          plain
          round
          size="small"
          @click.stop="emit('resetFilter')"
        >
          ↺ 進行中案件に戻る
        </el-button>
      </div>
    </template>

    <el-table
      v-if="filteredProjects.length > 0"
      :data="filteredProjects"
      stripe
      @row-click="handleRowClick"
    >
      <el-table-column prop="name" label="案件名" min-width="220">
        <template #default="{ row }">
          <span class="project-name">{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="ステータス" width="130">
        <template #default="{ row }">
          <el-tag
            :type="PROJECT_STATUS_TAG_TYPE[row.status as ProjectStatus]"
            effect="plain"
          >
            {{ PROJECT_STATUS_LABEL[row.status as ProjectStatus] }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="進捗" width="150">
        <template #default="{ row }">
          <div class="progress-cell">
            <el-progress
              :percentage="row.progress ?? 0"
              :stroke-width="8"
              :show-text="false"
            />
            <span>{{ row.progress ?? 0 }}%</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="予算消費率" width="160">
        <template #default="{ row }">
          <div class="progress-cell">
            <el-progress
              :percentage="Math.min(row.consumption_rate ?? 0, 100)"
              :stroke-width="8"
              :show-text="false"
              :status="getBudgetStatus(row.consumption_rate)"
            />
            <span>{{ row.consumption_rate ?? 0 }}%</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="予算 / 実績" width="190">
        <template #default="{ row }">
          <span class="budget-text">
            {{ formatCurrency(row.actual_amount) }} /
            {{ formatCurrency(row.budget_amount) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="確認状態" width="110">
        <template #default="{ row }">
          <el-tag
            v-if="row.alert_level === 'danger'"
            type="danger"
            effect="dark"
          >
            危険
          </el-tag>
          <el-tag
            v-else-if="row.alert_level === 'warning'"
            type="warning"
            effect="plain"
          >
            注意
          </el-tag>
          <el-tag v-else type="success" effect="plain"> 通常 </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <el-empty
      v-else
      :description="`${tableLabel}はありません`"
      :image-size="80"
    />
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { ProjectDashboard } from "@/api/dashboard";
import {
  PROJECT_STATUS_LABEL,
  PROJECT_STATUS_TAG_TYPE,
} from "@/constants/project";
import type { ProjectStatus } from "@/api/models/ProjectStatus";

type ApplicantFilter =
  | "active"
  | "pending"
  | "draft"
  | "rejected"
  | "risk"
  | "budget";

const props = defineProps<{
  projects: ProjectDashboard[];
  loading: boolean;
  filter: ApplicantFilter;
}>();

const emit = defineEmits<{
  (e: "move", id: number): void;
  (e: "resetFilter"): void;
}>();

const filteredProjects = computed(() => {
  switch (props.filter) {
    case "pending":
      return props.projects.filter((project) =>
        ["PENDING_DEPT", "PENDING_HQ"].includes(project.status),
      );

    case "draft":
      return props.projects.filter((project) => project.status === "DRAFT");

    case "rejected":
      return props.projects.filter((project) => project.status === "REJECTED");

    case "risk":
      return props.projects.filter(
        (project) =>
          ["APPROVED", "IN_PROGRESS"].includes(project.status) &&
          ["danger", "warning"].includes(project.alert_level ?? ""),
      );

    case "budget":
      return props.projects.filter(
        (project) =>
          ["APPROVED", "IN_PROGRESS"].includes(project.status) &&
          (project.consumption_rate ?? 0) >= 80,
      );

    case "active":
    default:
      return props.projects.filter((project) =>
        ["APPROVED", "IN_PROGRESS"].includes(project.status),
      );
  }
});

const tableLabel = computed(() => {
  const labels: Record<ApplicantFilter, string> = {
    active: "進行中案件",
    pending: "申請中案件",
    draft: "下書き案件",
    rejected: "却下案件",
    risk: "注意・危険案件",
    budget: "予算注意案件",
  };

  return labels[props.filter];
});

const tableTitle = computed(() => {
  return `自分の${tableLabel.value}（${filteredProjects.value.length}件）`;
});

const tableDescription = computed(() => {
  const descriptions: Record<ApplicantFilter, string> = {
    active: "承認済み案件の進捗・予算消費状況を確認できます",
    pending: "部門・本部の承認待ち案件を確認できます",
    draft: "未申請の保存案件を確認できます",
    rejected: "却下された案件と差し戻し内容を確認できます",
    risk: "進捗・予算面で確認が必要な案件を確認できます",
    budget: "予算消費率が高い案件を確認できます",
  };

  return descriptions[props.filter];
});

const handleRowClick = (row: ProjectDashboard) => {
  emit("move", row.id);
};

const formatCurrency = (value?: number) => {
  const amount = value ?? 0;

  if (amount >= 100000000) {
    return `${Math.round(amount / 100000000)}億円`;
  }

  if (amount >= 10000) {
    return `${Math.round(amount / 10000)}万円`;
  }

  return `${amount.toLocaleString()}円`;
};

const getBudgetStatus = (rate?: number) => {
  const value = rate ?? 0;

  if (value >= 100) {
    return "exception";
  }

  if (value >= 80) {
    return "warning";
  }

  return undefined;
};
</script>

<style scoped>
.project-card {
  border-radius: 12px;
  border: 1px solid #dcdfe6;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #303133;
}

.section-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.project-name {
  font-weight: 600;
  color: #303133;
  cursor: pointer;
}

.project-name:hover {
  color: #409eff;
  text-decoration: underline;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-cell .el-progress {
  flex: 1;
}

.budget-text {
  font-size: 12px;
  color: #606266;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>

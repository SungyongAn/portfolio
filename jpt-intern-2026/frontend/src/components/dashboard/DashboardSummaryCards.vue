<template>
  <div class="summary-cards">
    <el-card
      v-for="card in cards"
      :key="card.title"
      class="summary-card clickable"
      :class="card.type"
      shadow="hover"
      @click="card.onClick"
    >
      <div class="summary-header">
        <div class="summary-icon" :class="card.type">
          <el-icon :size="22">
            <component :is="card.icon" />
          </el-icon>
        </div>

        <div class="summary-title">
          {{ card.title }}
        </div>
      </div>

      <div class="summary-value">
        {{ card.value }}
        <span class="summary-unit">
          {{ card.unit }}
        </span>
      </div>

      <div class="summary-description">
        {{ card.description }}
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import {
  Warning,
  Bell,
  CircleCheck,
  Money,
  DataAnalysis,
} from "@element-plus/icons-vue";
import type { DashboardSummary } from "@/api/dashboard";
import type { ManagementFilter } from "@/types/dashboard";

const props = defineProps<{
  summary: DashboardSummary;
}>();

type SummaryCardFilter = ManagementFilter | "projects";

const emit = defineEmits<{
  (e: "select-filter", filter: SummaryCardFilter): void;
}>();

const formatCurrency = (value?: number) => {
  const amount = value ?? 0;

  if (amount >= 100000000) {
    return `${Math.round(amount / 100000000)}億`;
  }

  if (amount >= 10000) {
    return `${Math.round(amount / 10000)}万`;
  }

  return amount.toLocaleString();
};

const cards = computed(() => [
  {
    title: "承認待ち",
    value: props.summary.pendingApprovals ?? 0,
    unit: "件",
    icon: CircleCheck,
    type: "info",
    description: "部門・本部承認待ちの案件",
    onClick: () => emit("select-filter", "pending"),
  },
  {
    title: "進行中案件",
    value:
      props.summary.activeProjects ?? props.summary.inProgressProjects ?? 0,
    unit: "件",
    icon: DataAnalysis,
    type: "success",
    description: "承認済み・進行中の案件",
    onClick: () => emit("select-filter", "active"),
  },
  {
    title: "危険案件",
    value: props.summary.dangerProjects ?? 0,
    unit: "件",
    icon: Warning,
    type: "danger",
    description: "進捗・予算に重大な懸念",
    onClick: () => emit("select-filter", "danger"),
  },
  {
    title: "注意案件",
    value: props.summary.warningProjects ?? 0,
    unit: "件",
    icon: Bell,
    type: "warning",
    description: "早期確認が必要な案件",
    onClick: () => emit("select-filter", "warning"),
  },
  {
    title: "予算消費率",
    value: props.summary.totalConsumptionRate ?? 0,
    unit: "%",
    icon: Money,
    type: "warning",
    description: `実績 ${formatCurrency(
      props.summary.totalActual,
    )}円 / 予算 ${formatCurrency(
      props.summary.totalBudget,
    )}円 / 注意案件 ${props.summary.budgetWarningCount}件`,
    onClick: () => emit("select-filter", "budget"),
  },
]);
</script>

<style scoped>
.summary-cards {
  display: flex;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
  width: 100%;
  overflow-x: auto;
  padding-bottom: 8px;
}

.summary-card {
  border-radius: 12px;
  min-width: 0;
  flex: 0 0 220px;
}

.summary-card.clickable {
  cursor: pointer;
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;
}

.summary-card.clickable:hover {
  transform: translateY(-2px);
}

.summary-card.clickable:active {
  transform: translateY(0);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.summary-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-title {
  font-size: 13px;
  color: #555;
  white-space: nowrap;
}

.summary-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  color: #222;
}

.summary-unit {
  font-size: 13px;
  font-weight: 500;
  color: #666;
  margin-left: 2px;
}

.summary-description {
  margin-top: 8px;
  font-size: 11px;
  line-height: 1.4;
  color: #606266;
}

.summary-card.danger {
  background: #fff1f0;
  border-color: #ffccc7;
}

.summary-card.warning {
  background: #fff7e6;
  border-color: #ffd591;
}

.summary-card.info {
  background: #f0f5ff;
  border-color: #adc6ff;
}

.summary-card.success {
  background: #f6ffed;
  border-color: #b7eb8f;
}
</style>

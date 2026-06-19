<template>
  <el-card shadow="never" class="project-list-card" v-loading="loading">
    <template #header>
      <div class="card-header">
        <div>
          <div class="card-title">{{ listTitle }}</div>
          <div class="card-subtitle">{{ listDescription }}</div>
        </div>

        <el-button
          v-if="filter !== 'default'"
          type="primary"
          plain
          round
          size="small"
          @click.stop="emit('resetFilter')"
        >
          ↺ ダッシュボード表示に戻る
        </el-button>
      </div>
    </template>

    <el-table
      v-if="projects.length > 0"
      :data="projects"
      stripe
      class="project-table"
      @row-click="handleRowClick"
    >
      <el-table-column label="危険度" width="90">
        <template #default="{ row }">
          <el-tag v-if="row.alert_level === 'danger'" type="danger" effect="dark">
            危険
          </el-tag>
          <el-tag
            v-else-if="row.alert_level === 'warning'"
            type="warning"
            effect="plain"
          >
            注意
          </el-tag>
          <el-tag v-else type="info" effect="plain">通常</el-tag>
        </template>
      </el-table-column>

      <el-table-column label="注視理由" min-width="180">
        <template #default="{ row }">
          {{ row.alert_reason ?? "-" }}
        </template>
      </el-table-column>

      <el-table-column prop="department_name" label="部門" min-width="120" />

      <el-table-column prop="name" label="案件名" min-width="180">
        <template #default="{ row }">
          <span class="project-name">{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="owner_name" label="責任者" min-width="120" />

      <el-table-column label="進捗" width="140">
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

      <el-table-column label="SPI" width="90" align="center">
        <template #default="{ row }">
          {{ row.spi ?? "-" }}
        </template>
      </el-table-column>

      <el-table-column label="CPI" width="90" align="center">
        <template #default="{ row }">
          {{ row.cpi ?? "-" }}
        </template>
      </el-table-column>

      <el-table-column label="予算消費率" width="150">
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
          <el-popover
            placement="top"
            width="260"
            trigger="click"
            @click.stop
          >
            <template #reference>
              <button class="budget-popover-trigger" @click.stop>
                {{ formatCurrency(row.actual_amount) }} /
                {{ formatCurrency(row.budget_amount) }}
              </button>
            </template>

            <div class="budget-popover">
              <div class="popover-title">予算サマリ</div>

              <div class="budget-row">
                <span>予算額</span>
                <strong>{{ formatCurrency(row.budget_amount) }}</strong>
              </div>

              <div class="budget-row">
                <span>実績額</span>
                <strong>{{ formatCurrency(row.actual_amount) }}</strong>
              </div>

              <div class="budget-row">
                <span>消費率</span>
                <strong>{{ row.consumption_rate ?? 0 }}%</strong>
              </div>

              <div class="budget-row">
                <span>CPI</span>
                <strong>{{ row.cpi ?? "-" }}</strong>
              </div>

              <el-divider />

              <div class="popover-note">
                詳細確認が必要な場合は案件詳細、または予算管理画面で確認してください。
              </div>
            </div>
          </el-popover>
        </template>
      </el-table-column>

      <el-table-column label="期限超過" width="100">
        <template #default="{ row }">
          <el-tag
            v-if="row.overdue_task_count > 0"
            type="danger"
            effect="plain"
          >
            {{ row.overdue_task_count }}件
          </el-tag>
          <span v-else class="muted">なし</span>
        </template>
      </el-table-column>
    </el-table>

    <el-empty
      v-else
      :description="`${listTitle}はありません`"
      :image-size="80"
    />
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { ProjectDashboard } from "@/api/dashboard";
import type { ManagementFilter } from "@/types/dashboard";

const props = defineProps<{
  projects: ProjectDashboard[];
  loading?: boolean;
  filter: ManagementFilter;
}>();

const emit = defineEmits<{
  (e: "move", id: number): void;
  (e: "resetFilter"): void;
}>();

const listTitle = computed(() => {
  const labels: Record<ManagementFilter, string> = {
    default: "注視すべき案件",
    pending: "承認待ち案件",
    active: "進行中案件",
    danger: "危険案件",
    warning: "注意案件",
    budget: "予算注意案件",
  };

  return `${labels[props.filter]}（${props.projects.length}件）`;
});

const listDescription = computed(() => {
  const descriptions: Record<ManagementFilter, string> = {
    default: "危険・注意案件を部門、責任者、予算状況とあわせて確認できます",
    pending: "部門・本部承認待ちの案件を確認できます",
    active: "承認済み・進行中の案件を確認できます",
    danger: "進捗・予算に重大な懸念がある案件を確認できます",
    warning: "早期確認が必要な案件を確認できます",
    budget: "予算消費率に注意が必要な案件を確認できます",
  };

  return descriptions[props.filter];
});

const handleRowClick = (row: ProjectDashboard) => {
  emit("move", row.id);
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
</script>

<style scoped>
.project-list-card {
  border-radius: 12px;
  border: 1px solid #dcdfe6;
  margin-top: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  color: #303133;
}

.card-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.project-table {
  width: 100%;
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

.budget-popover-trigger {
  padding: 0;
  border: none;
  background: transparent;
  color: #409eff;
  font-size: 12px;
  cursor: pointer;
}

.budget-popover-trigger:hover {
  text-decoration: underline;
}

.budget-popover {
  font-size: 13px;
}

.popover-title {
  margin-bottom: 10px;
  font-weight: 700;
  color: #303133;
}

.budget-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin: 6px 0;
}

.budget-row span {
  color: #606266;
}

.budget-row strong {
  color: #303133;
}

.popover-note {
  color: #909399;
  font-size: 12px;
  line-height: 1.6;
}

.muted {
  color: #909399;
  font-size: 12px;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>
<template>
  <el-row :gutter="16" class="summary-cards">
    <el-col :xs="24" :sm="12" :lg="6">
      <el-card shadow="hover">
        <div class="summary-card">
          <span class="label">案件数</span>
          <span class="value">{{ summary.total_projects }}</span>
        </div>
      </el-card>
    </el-col>

    <el-col :xs="24" :sm="12" :lg="6">
      <el-card shadow="hover">
        <div class="summary-card">
          <span class="label">総予算</span>
          <span class="value">{{ formatYen(summary.total_budget) }}</span>
        </div>
      </el-card>
    </el-col>

    <el-col :xs="24" :sm="12" :lg="6">
      <el-card shadow="hover">
        <div class="summary-card">
          <span class="label">総実績</span>
          <span class="value">{{ formatYen(summary.total_actual) }}</span>
        </div>
      </el-card>
    </el-col>

    <el-col :xs="24" :sm="12" :lg="6">
      <el-card shadow="hover">
        <div class="summary-card">
          <span class="label">平均消化率</span>
          <span class="value">{{ summary.avg_consumption_rate }}%</span>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
type BudgetSummary = {
  total_projects: number;
  total_budget: number;
  total_actual: number;
  avg_consumption_rate: number;
};

defineProps<{
  summary: BudgetSummary;
}>();

const formatYen = (value: number) => {
  return `${Number(value || 0).toLocaleString()}円`;
};
</script>

<style scoped>
.summary-cards {
  margin-bottom: 24px;
}

.summary-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-card .label {
  font-size: 0.9rem;
  color: #909399;
}

.summary-card .value {
  font-size: 1.5rem;
  font-weight: 700;
}
</style>
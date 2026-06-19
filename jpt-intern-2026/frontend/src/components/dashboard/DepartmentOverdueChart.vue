<template>
  <el-card shadow="never" class="chart-card">
    <template #header>
      <div class="section-title">部門別期限超過タスク件数</div>
      <div class="section-subtitle">部門ごとの遅延タスク状況を確認できます</div>
    </template>

    <div v-if="departments.length > 0" class="horizontal-chart">
      <div
        v-for="(department, index) in departments"
        :key="department.department_id"
        class="bar-row"
      >
        <div class="bar-label">
          {{ department.department_name }}
        </div>

        <div class="bar-track">
          <div
            class="bar-fill"
            :style="{
              width: `${calcWidth(department.overdue_task_count)}%`,
              backgroundColor: colors[index % colors.length],
            }"
          />
        </div>

        <div class="bar-value">{{ department.overdue_task_count }}件</div>
      </div>
    </div>

    <el-empty
      v-else
      description="部門別期限超過タスクデータがありません"
      :image-size="80"
    />
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { DepartmentSummary } from "@/api/dashboard";
import { DEPARTMENT_CHART_COLORS } from "@/constants/chartColors";

const props = defineProps<{
  departments: DepartmentSummary[];
}>();

const colors = DEPARTMENT_CHART_COLORS;

const maxOverdueCount = computed(() => {
  const max = Math.max(
    ...props.departments.map((department) => department.overdue_task_count),
    0,
  );

  return max === 0 ? 1 : max;
});

const calcWidth = (count: number) => {
  if (count <= 0) return 0;
  return Math.max((count / maxOverdueCount.value) * 100, 6);
};
</script>

<style scoped>
.chart-card {
  border-radius: 12px;
  border: 1px solid #dcdfe6;
  margin-bottom: 16px;
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

.horizontal-chart {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 24px 4px;
}

.bar-row {
  display: grid;
  grid-template-columns: 140px 1fr 48px;
  align-items: center;
  gap: 12px;
}

.bar-label {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
  overflow-wrap: anywhere;
}

.bar-track {
  height: 18px;
  border-radius: 999px;
  background-color: #ebeef5;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.2s ease;
}

.bar-value {
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  text-align: right;
}

@media (max-width: 768px) {
  .bar-row {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .bar-value {
    text-align: left;
  }
}
</style>

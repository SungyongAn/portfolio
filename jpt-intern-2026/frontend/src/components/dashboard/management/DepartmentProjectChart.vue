<template>
  <el-card shadow="never" class="chart-card">
    <template #header>
      <div class="section-title">部門別 案件数</div>
      <div class="section-subtitle">部門ごとの案件保有状況を確認できます</div>
    </template>

    <div v-if="departments.length > 0" class="chart-layout">
      <div class="donut-chart" :style="{ background: donutBackground }">
        <div class="donut-center">
          <div class="center-label">合計</div>
          <div class="center-value">{{ totalProjects }}件</div>
        </div>
      </div>

      <div class="legend-list">
        <div
          v-for="(department, index) in departments"
          :key="department.department_id"
          class="legend-item clickable"
          @click="emit('selectDepartment', department.department_id)"
        >
          <span
            class="legend-color"
            :style="{ backgroundColor: colors[index % colors.length] }"
          />

          <div class="legend-text">
            <div class="department-name">
              {{ department.department_name }}
            </div>
            <div class="department-count">
              {{ department.project_count }}件（{{ calcRate(department.project_count) }}%）
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-empty v-else description="部門別案件データがありません" :image-size="80" />
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { DepartmentSummary } from "@/api/dashboard";
import { DEPARTMENT_CHART_COLORS } from "@/constants/chartColors";

const emit = defineEmits<{
  selectDepartment: [departmentId: number];
}>();

const props = defineProps<{
  departments: DepartmentSummary[];
}>();

const colors = DEPARTMENT_CHART_COLORS;

const totalProjects = computed(() => {
  return props.departments.reduce(
    (sum, department) => sum + department.project_count,
    0,
  );
});

const calcRate = (count: number) => {
  if (totalProjects.value === 0) return 0;
  return Math.round((count / totalProjects.value) * 100);
};

const donutBackground = computed(() => {
  if (totalProjects.value === 0) return "#ebeef5";

  let current = 0;

  const segments = props.departments.map((department, index) => {
    const rate = (department.project_count / totalProjects.value) * 100;
    const start = current;
    const end = current + rate;
    current = end;

    return `${colors[index % colors.length]} ${start}% ${end}%`;
  });

  return `conic-gradient(${segments.join(", ")})`;
});
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

.chart-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.donut-chart {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  position: relative;
  flex-shrink: 0;
}

.donut-chart::after {
  content: "";
  position: absolute;
  inset: 48px;
  background: #fff;
  border-radius: 50%;
}

.donut-center {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.center-label {
  font-size: 12px;
  color: #909399;
}

.center-value {
  margin-top: 4px;
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}

.legend-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 240px;
}

.legend-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  width: 100%;
}

.legend-color {
  width: 12px;
  height: 12px;
  margin-top: 3px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-text {
  flex: 1;
}

.department-name {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.department-count {
  margin-top: 2px;
  font-size: 12px;
  color: #606266;
}

.legend-item.clickable {
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 8px;
  transition: background-color 0.15s ease;
}

.legend-item.clickable:hover {
  background-color: #f5f7fa;
}

@media (max-width: 768px) {
  .donut-chart {
    width: 180px;
    height: 180px;
  }

  .legend-list {
    width: 100%;
  }
}
</style>
<template>
  <div class="management-chart-grid">
    <DepartmentProjectChart
      :departments="departments"
      @select-department="emit('selectDepartment', $event)"
    />

    <DepartmentBudgetChart :departments="departments" />

    <DepartmentOverdueChart :departments="departments" />
  </div>
</template>

<script setup lang="ts">
import DepartmentProjectChart from "@/components/dashboard/management/DepartmentProjectChart.vue";
import DepartmentBudgetChart from "@/components/dashboard/DepartmentBudgetChart.vue";
import DepartmentOverdueChart from "@/components/dashboard/DepartmentOverdueChart.vue";
import type { DepartmentSummary } from "@/api/dashboard";

defineProps<{
  departments: DepartmentSummary[];
}>();

const emit = defineEmits<{
  (e: "selectDepartment", departmentId: number): void;
}>();
</script>

<style scoped>
.management-chart-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 16px;
}

@media (max-width: 1200px) {
  .management-chart-grid {
    grid-template-columns: 1fr;
  }
}
</style>

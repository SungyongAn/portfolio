<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>案件別予算一覧</span>
      </div>
    </template>

    <el-table
      :data="projects"
      border
      stripe
      v-loading="loading"
      style="width: 100%"
      @sort-change="emit('sort-change', $event)"
    >
      <el-table-column prop="name" label="案件名" min-width="220" />

      <el-table-column label="部門" width="160">
        <template #default="{ row }">
          {{ departmentName(row.department_id) }}
        </template>
      </el-table-column>

      <el-table-column
        prop="budget_amount"
        label="予算"
        width="160"
        align="right"
        sortable="custom"
      >
        <template #default="{ row }">
          {{ formatYen(row.budget_amount) }}
        </template>
      </el-table-column>

      <el-table-column label="実績" width="160" align="right">
        <template #default="{ row }">
          {{ formatYen(row.actual_amount) }}
        </template>
      </el-table-column>

      <el-table-column label="消化率" width="140">
        <template #default="{ row }">
          <el-tag
            v-if="row.consumption_rate !== null"
            :type="getRateType(row.consumption_rate)"
          >
            {{ row.consumption_rate }}%
          </el-tag>
          <span v-else>--</span>
        </template>
      </el-table-column>

      <el-table-column prop="status" label="状態" width="140">
        <template #default="{ row }">
          {{ PROJECT_STATUS_LABEL[row.status as ProjectStatus] }}
        </template>
      </el-table-column>

      <el-table-column label="" width="140" fixed="right">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="emit('detail', row.id)"
          >
            詳細
          </el-button>
        </template>
      </el-table-column>

      <template #empty>
        <el-empty description="案件がありません" />
      </template>
    </el-table>

    <div class="pagination-wrapper">
      <el-pagination
        background
        layout="prev, pager, next, total"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="emit('page-change', $event)"
      />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { PROJECT_STATUS_LABEL } from "@/constants/project";
import type { Department } from "@/api/departments";
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import type { ProjectStatus } from "@/api/models/ProjectStatus";

const props = defineProps<{
  projects: ProjectResponse[];
  departments: Department[];
  loading: boolean;
  total: number;
  currentPage: number;
  pageSize: number;
}>();

const emit = defineEmits<{
  (
    e: "sort-change",
    payload: {
      prop: string;
      order: "ascending" | "descending" | null;
    },
  ): void;
  (e: "page-change", page: number): void;
  (e: "detail", projectId: number): void;
}>();

const departmentName = (id: number): string => {
  return (
    props.departments.find((department: Department) => department.id === id)
      ?.name ?? String(id)
  );
};

const formatYen = (value: number) => {
  return `${Number(value || 0).toLocaleString()}円`;
};

const getRateType = (rate: number) => {
  if (rate >= 100) return "danger";
  if (rate >= 80) return "warning";
  return "success";
};
</script>

<style scoped>
.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>

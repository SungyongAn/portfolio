<template>
  <el-table :data="projects" stripe style="width: 100%" v-loading="loading">
    <el-table-column prop="name" label="案件名" min-width="180">
      <template #default="{ row }">
        <span
          class="project-name-link"
          @click="emitMove(row)"
          @click.middle.prevent
        >
          {{ row.name }}
        </span>
      </template>
    </el-table-column>

    <el-table-column label="部門" width="160">
      <template #default="{ row }">
        {{ departmentName(row.department_id) }}
      </template>
    </el-table-column>

    <el-table-column label="ステータス" width="140">
      <template #default="{ row }">
        <el-tag :type="PROJECT_STATUS_TAG_TYPE[row.status as ProjectStatus]">
          {{ PROJECT_STATUS_LABEL[row.status as ProjectStatus] }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column label="進捗率" width="160">
      <template #default="{ row }">
        <el-progress
          v-if="row.status === 'APPROVED'"
          :percentage="row.progress"
          :status="row.progress === 100 ? 'success' : undefined"
          :stroke-width="8"
        />
        <span v-else class="text-gray">—</span>
      </template>
    </el-table-column>

    <el-table-column label="予算消化率" width="180">
      <template #default="{ row }">
        <div v-if="row.status === 'APPROVED'">
          <el-progress
            :percentage="Math.min(row.consumption_rate ?? 0, 100)"
            :status="getConsumptionStatus(row.consumption_rate)"
            :stroke-width="8"
          />
        </div>
        <span v-else class="text-gray">—</span>
      </template>
    </el-table-column>

    <el-table-column prop="created_at" label="申請日" width="120">
      <template #default="{ row }">
        {{ formatDate(row.created_at) }}
      </template>
    </el-table-column>

    <template #empty>
      <el-empty :description="emptyText" />
    </template>
  </el-table>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import type { ProjectStatus } from "@/api/models/ProjectStatus";
import { useProjectTable } from "@/composables/useProjectTable";
import { departmentsAPI, type Department } from "@/api/departments";

defineProps<{
  projects: ProjectResponse[];
  loading?: boolean;
  emptyText?: string;
}>();

const {
  PROJECT_STATUS_LABEL,
  PROJECT_STATUS_TAG_TYPE,
  formatDate,
  getConsumptionStatus,
} = useProjectTable();

const departments = ref<Department[]>([]);

const departmentName = (id: number): string => {
  return (
    departments.value.find((d: Department) => d.id === id)?.name ?? String(id)
  );
};

const emit = defineEmits<{
  (e: "move", projectId: number): void;
}>();

const emitMove = (row: ProjectResponse & { project_id?: number }) => {
  const projectId = row.id ?? row.project_id;
  if (!projectId) return;
  emit("move", projectId);
};

onMounted(async () => {
  try {
    const res = await departmentsAPI.getDepartments();
    departments.value = res.data;
  } catch {
    // 取得失敗時はIDをそのまま表示
  }
});
</script>

<style scoped></style>

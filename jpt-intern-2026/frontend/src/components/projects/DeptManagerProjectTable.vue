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
          v-if="['APPROVED', 'IN_PROGRESS'].includes(row.status)"
          :percentage="row.progress"
          :status="row.progress === 100 ? 'success' : undefined"
          :stroke-width="8"
        />
        <span v-else class="text-gray">—</span>
      </template>
    </el-table-column>

    <el-table-column label="予算消化率" width="180">
      <template #default="{ row }">
        <div v-if="['APPROVED', 'IN_PROGRESS'].includes(row.status)">
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
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import type { ProjectStatus } from "@/api/models/ProjectStatus";
import { useProjectTable } from "../../composables/useProjectTable";

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

const emit = defineEmits<{
  (e: "move", projectId: number): void;
}>();

const emitMove = (row: ProjectResponse & { project_id?: number }) => {
  const projectId = row.id ?? row.project_id;
  if (!projectId) return;
  emit("move", projectId);
};
</script>

<style scoped></style>

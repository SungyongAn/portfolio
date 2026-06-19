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

    <el-table-column
      v-if="
        !props.filterStatus?.some((s) =>
          ['IN_PROGRESS', 'APPROVED'].includes(s),
        ) ||
        props.filterStatus?.some(
          (s) => !['IN_PROGRESS', 'APPROVED'].includes(s),
        )
      "
      label="ステータス"
      width="140"
    >
      <template #default="{ row }">
        <el-tag :type="PROJECT_STATUS_TAG_TYPE[row.status as ProjectStatus]">
          {{ PROJECT_STATUS_LABEL[row.status as ProjectStatus] }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column
      v-if="
        !props.filterStatus?.some((s) =>
          ['IN_PROGRESS', 'APPROVED'].includes(s),
        ) ||
        props.filterStatus?.some(
          (s) => !['IN_PROGRESS', 'APPROVED'].includes(s),
        )
      "
      label="承認ステップ"
      width="200"
    >
      <template #default="{ row }">
        <div class="approval-steps">
          <el-tag size="small" :type="getApprovalStepType(row.status, 'dept')">
            部門
          </el-tag>
          <span class="step-arrow">→</span>
          <el-tag size="small" :type="getApprovalStepType(row.status, 'hq')">
            本部
          </el-tag>
          <span class="step-arrow">→</span>
          <el-tag
            size="small"
            :type="getApprovalStepType(row.status, 'approved')"
          >
            完了
          </el-tag>
        </div>
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

const props = defineProps<{
  projects: ProjectResponse[];
  loading?: boolean;
  emptyText?: string;
  filterStatus?: string[];
}>();

const {
  PROJECT_STATUS_LABEL,
  PROJECT_STATUS_TAG_TYPE,
  formatDate,
  getApprovalStepType,
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

<style scoped>
.approval-steps {
  display: flex;
  align-items: center;
  gap: 4px;
}

.step-arrow {
  color: #909399;
  font-size: 0.75rem;
}
</style>

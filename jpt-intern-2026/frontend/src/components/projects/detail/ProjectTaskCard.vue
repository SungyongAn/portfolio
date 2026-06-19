<template>
  <el-card class="project-task-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>タスク一覧</span>

        <div class="header-actions">
          <el-button
            v-if="canCreateTask"
            type="primary"
            size="small"
            @click="$emit('create-task')"
          >
            タスク追加
          </el-button>
        </div>
      </div>
    </template>

    <TaskGanttTable
      v-if="tasks.length > 0"
      :tasks="tasks"
      @open-task-detail="handleRowClick"
    />

    <el-empty
      v-else
      description="タスクが登録されていません"
      :image-size="80"
    />
  </el-card>
</template>

<script setup lang="ts">
import type { TaskResponse } from "@/api/models/TaskResponse";
import TaskGanttTable from "@/components/projects/TaskGanttTable.vue";

defineProps<{
  tasks: TaskResponse[];
  canCreateTask?: boolean;
}>();

const emit = defineEmits<{
  (e: "open-task", task: TaskResponse): void;
  (e: "create-task"): void;
}>();

const handleRowClick = (task: TaskResponse) => {
  emit("open-task", task);
};
</script>

<style scoped>
.project-task-card {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-actions {
  display: flex;
  gap: 8px;
}
</style>

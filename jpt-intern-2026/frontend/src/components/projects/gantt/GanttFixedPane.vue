<template>
  <div class="fixed-pane">
    <div class="fixed-header">
      <div class="col phase">工程</div>
      <div class="col task">タスク</div>
      <div class="col assignee">担当者</div>
      <div class="col status">状態</div>
      <div class="col progress">進捗</div>
    </div>

    <div
      v-for="task in tasks"
      :key="`fixed-${task.id}`"
      class="fixed-row clickable-row"
      @click="emit('openTaskDetail', task)"
    >
      <div class="col phase">
        {{ task.phase_name || "未設定" }}
      </div>

      <div class="col task task-name">
        {{ task.name }}
      </div>

      <div class="col assignee">
        {{ task.assignee_name || "未割当" }}
      </div>

      <el-tag size="small" :type="getTaskStatusTagType(task.status)">
        {{ getTaskStatusLabel(task.status) }}
      </el-tag>

      <div class="col progress">
        <span class="progress-text">{{ task.progress ?? 0 }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TaskResponse } from "@/api/models/TaskResponse";
import {
  getTaskStatusLabel,
  getTaskStatusTagType,
} from "@/constants/taskStatus";

defineProps<{
  tasks: TaskResponse[];
}>();

const emit = defineEmits<{
  (e: "openTaskDetail", task: TaskResponse): void;
}>();
</script>

<style scoped>
.fixed-pane {
  flex: 0 0 580px;
  width: 580px;
}

.fixed-header,
.fixed-row {
  display: grid;
  grid-template-columns: 90px 210px 100px 80px 60px;
  height: var(--gantt-row-height);
}

.fixed-header {
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  font-weight: 600;
  color: #606266;
}

.fixed-row {
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}

.fixed-row:last-child {
  border-bottom: none;
}

.fixed-row:hover {
  background: #f8fafc;
}

.col {
  padding: 10px 8px;
  border-right: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  height: var(--gantt-row-height);
  box-sizing: border-box;
  font-size: 13px;
  overflow: hidden;
}

.col:last-child {
  border-right: none;
}

.phase,
.task,
.assignee {
  white-space: nowrap;
  text-overflow: ellipsis;
}

.task-name {
  font-weight: 600;
  color: #303133;
}

.task-name:hover {
  color: #409eff;
  text-decoration: underline;
}

.progress-text {
  font-size: 12px;
  color: #606266;
  min-width: 36px;
  text-align: right;
}

.clickable-row {
  cursor: pointer;
}

@media (max-width: 768px) {
  .fixed-pane {
    flex: 0 0 540px;
    width: 540px;
  }

  .fixed-header,
  .fixed-row {
    grid-template-columns: 90px 180px 100px 100px 120px;
  }
}
</style>

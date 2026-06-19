<template>
  <div class="task-gantt-table">
    <GanttToolbar
      :selected-assignee="selectedAssignee"
      :assignee-options="assigneeOptions"
      :view-mode="viewMode"
      @update:selected-assignee="handleSelectedAssigneeChange"
      @update:view-mode="handleViewModeChange"
      @scroll-today="scrollToToday"
    />

    <el-empty
      v-if="filteredTasks.length === 0"
      description="表示するタスクがありません"
    />

    <div v-else class="gantt-layout">
      <GanttFixedPane
        :tasks="filteredTasks"
        @open-task-detail="openTaskDetail"
      />

      <GanttTimelinePane
        ref="timelinePaneRef"
        :tasks="filteredTasks"
        :visible-timeline-days="visibleTimelineDays"
        :timeline-width="timelineWidth"
        :day-width="dayWidth"
        :today-line-style="todayLineStyle"
        :get-date-label="getDateLabel"
        :get-date-left="getDateLeft"
        :get-task-bar-style="getTaskBarStyle"
        @open-task-detail="openTaskDetail"
      />
    </div>

    <p class="gantt-note">
      ※ 日 / 週 /
      月の表示切替、担当者フィルター、本日ラインにより、工程状況を俯瞰できます。
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";

import GanttToolbar from "@/components/projects/gantt/GanttToolbar.vue";
import GanttFixedPane from "@/components/projects/gantt/GanttFixedPane.vue";
import GanttTimelinePane from "@/components/projects/gantt/GanttTimelinePane.vue";

import { useTaskGantt } from "@/composables/useTaskGantt";
import type { GanttViewMode } from "@/composables/useTaskGantt";
import type { TaskResponse } from "@/api/models/TaskResponse";

const props = defineProps<{
  tasks: TaskResponse[];
}>();

const emit = defineEmits<{
  (e: "open-task-detail", task: TaskResponse): void;
}>();

const tasksRef = computed(() => props.tasks);

const {
  selectedAssignee,
  viewMode,
  filteredTasks,
  assigneeOptions,
  visibleTimelineDays,
  timelineWidth,
  dayWidth,
  todayLineStyle,
  getDateLabel,
  getDateLeft,
  getTaskBarStyle,
} = useTaskGantt(tasksRef);

const timelinePaneRef = ref<InstanceType<typeof GanttTimelinePane> | null>(
  null,
);

const handleSelectedAssigneeChange = (value: string | null) => {
  selectedAssignee.value = value ?? "";
};

const handleViewModeChange = (value: GanttViewMode) => {
  viewMode.value = value;
};

const openTaskDetail = (task: TaskResponse) => {
  emit("open-task-detail", task);
};

const scrollToToday = async () => {
  await nextTick();

  if (!todayLineStyle.value) {
    return;
  }

  const left = Number.parseInt(String(todayLineStyle.value.left), 10);

  if (Number.isNaN(left)) {
    return;
  }

  await timelinePaneRef.value?.scrollToToday(left);
};

watch(
  [viewMode, selectedAssignee],
  () => {
    void scrollToToday();
  },
  { immediate: true },
);
</script>

<style scoped>
.task-gantt-table {
  width: 100%;
  --gantt-row-height: 58px;
}

.gantt-layout {
  display: flex;
  width: 100%;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}

.gantt-note {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .gantt-layout {
    overflow-x: auto;
  }
}
</style>

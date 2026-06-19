<template>
  <div ref="timelinePaneRef" class="timeline-pane">
    <div class="timeline-inner" :style="{ width: `${timelineWidth}px` }">
      <div class="timeline-header">
        <div
          v-for="date in visibleTimelineDays"
          :key="date.toISOString()"
          class="date-cell"
          :style="{
            left: `${getDateLeft(date)}px`,
            width: `${dayWidth}px`,
          }"
        >
          {{ getDateLabel(date) }}
        </div>
      </div>

      <div
        v-for="task in tasks"
        :key="`timeline-${task.id}`"
        class="timeline-row"
      >
        <div v-if="todayLineStyle" class="today-line" :style="todayLineStyle" />

        <div
          v-if="getTaskBarStyle(task)"
          class="task-bar"
          :class="getTaskStatusClass(task.status)"
          :style="getTaskBarStyle(task)"
          @click.stop="emit('openTaskDetail', task)"
        >
          <span class="task-bar-label">
            {{ task.name }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref } from "vue";
import type { CSSProperties } from "vue";
import type { TaskResponse } from "@/api/models/TaskResponse";
import { getTaskStatusClass } from "@/constants/taskStatus";

defineProps<{
  tasks: TaskResponse[];
  visibleTimelineDays: Date[];
  timelineWidth: number;
  dayWidth: number;
  todayLineStyle: CSSProperties | null;
  getDateLabel: (date: Date) => string;
  getDateLeft: (date: Date) => number;
  getTaskBarStyle: (task: TaskResponse) => CSSProperties | null;
}>();

const emit = defineEmits<{
  (e: "openTaskDetail", task: TaskResponse): void;
}>();

const timelinePaneRef = ref<HTMLElement | null>(null);

const scrollToToday = async (todayLeft?: number) => {
  await nextTick();

  if (!timelinePaneRef.value) return;

  const left =
    typeof todayLeft === "number"
      ? todayLeft
      : Number.parseInt(
          String(
            getComputedStyle(timelinePaneRef.value)
              .getPropertyValue("--today-left")
              .replace("px", ""),
          ),
          10,
        );

  if (Number.isNaN(left)) return;

  timelinePaneRef.value.scrollLeft = Math.max(
    left - timelinePaneRef.value.clientWidth / 2,
    0,
  );
};

defineExpose({
  scrollToToday,
});
</script>

<style scoped>
.timeline-pane {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
}

.timeline-inner {
  position: relative;
}

.timeline-header {
  position: relative;
  height: var(--gantt-row-height);
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.timeline-row {
  position: relative;
  height: var(--gantt-row-height);
  border-bottom: 1px solid #ebeef5;
  background-image: linear-gradient(to right, #ebeef5 1px, transparent 1px);
  background-size: 34px 100%;
}

.timeline-row:last-child {
  border-bottom: none;
}

.date-cell {
  position: absolute;
  top: 0;
  height: var(--gantt-row-height);
  padding-top: 10px;
  border-left: 1px solid #ebeef5;
  text-align: center;
  font-size: 12px;
  color: #606266;
  box-sizing: border-box;
}

.today-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #f56c6c;
  z-index: 3;
}

.today-line::before {
  content: "今日";
  position: absolute;
  top: 2px;
  left: 4px;
  background: #f56c6c;
  color: #fff;
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 4px;
  white-space: nowrap;
}

.task-bar {
  position: absolute;
  top: 17px;
  height: 24px;
  border-radius: 12px;
  color: #fff;
  font-size: 12px;
  line-height: 24px;
  padding: 0 10px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  z-index: 2;
  box-sizing: border-box;
  cursor: pointer;
}

.task-bar.todo,
.task-bar.not-started {
  background: #909399;
}

.task-bar.in-progress {
  background: #409eff;
}

.task-bar.in-review,
.task-bar.review {
  background: #e6a23c;
}

.task-bar.done,
.task-bar.completed {
  background: #67c23a;
}

.task-bar-label {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .timeline-pane {
    flex: 0 0 400px;
  }
}
</style>

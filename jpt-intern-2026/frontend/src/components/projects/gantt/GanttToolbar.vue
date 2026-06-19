<template>
  <div class="gantt-toolbar">
    <el-select
      :model-value="selectedAssignee"
      placeholder="担当者で絞り込み"
      clearable
      class="assignee-filter"
      @update:model-value="emit('update:selectedAssignee', $event)"
    >
      <el-option
        v-for="assignee in assigneeOptions"
        :key="assignee"
        :label="assignee"
        :value="assignee"
      />
    </el-select>

    <div class="gantt-actions">
      <el-radio-group
        :model-value="viewMode"
        size="small"
        @update:model-value="emit('update:viewMode', $event)"
      >
        <el-radio-button value="day">日</el-radio-button>
        <el-radio-button value="week">週</el-radio-button>
        <el-radio-button value="month">月</el-radio-button>
      </el-radio-group>

      <el-button size="small" type="primary" plain @click="emit('scrollToday')">
        📍 今日へ移動
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  selectedAssignee: string | null;
  assigneeOptions: string[];
  viewMode: "day" | "week" | "month";
}>();

const emit = defineEmits<{
  (e: "update:selectedAssignee", value: string | null): void;
  (e: "update:viewMode", value: "day" | "week" | "month"): void;
  (e: "scrollToday"): void;
}>();
</script>

<style scoped>
.gantt-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.gantt-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.assignee-filter {
  width: 240px;
}

@media (max-width: 768px) {
  .gantt-toolbar {
    align-items: stretch;
  }

  .assignee-filter {
    width: 100%;
  }
}
</style>

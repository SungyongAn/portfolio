<template>
  <el-dialog
    :model-value="modelValue"
    title="タスク詳細"
    width="700px"
    @close="closeDialog"
  >
    <el-form v-if="form" label-width="100px">
      <!-- タスク名（編集不可） -->
      <el-form-item label="タスク名">
        <el-input v-model="form.name" disabled />
      </el-form-item>

      <!-- 進捗 -->
      <el-form-item label="進捗">
        <el-input-number
          v-model="form.progress"
          :min="0"
          :max="100"
          :disabled="!authStore.isApplicant && !authStore.isTaskMember"
        />
      </el-form-item>

      <!-- ステータス -->
      <el-form-item label="ステータス">
        <el-select
          v-model="form.status"
          :disabled="!authStore.isApplicant && !authStore.isTaskMember"
        >
          <el-option label="未着手" value="TODO" />
          <el-option label="進行中" value="IN_PROGRESS" />
          <el-option label="レビュー中" value="IN_REVIEW" />
          <el-option label="完了" value="DONE" />
        </el-select>
      </el-form-item>

      <!-- 説明 -->
      <el-form-item label="説明">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="4"
          :disabled="!authStore.isApplicant && !authStore.isTaskMember"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="closeDialog">閉じる</el-button>
      <el-button
        v-if="authStore.isApplicant || authStore.isTaskMember"
        type="primary"
        :loading="saving"
        @click="saveTask"
      >
        保存
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import type { TaskUpdate } from "@/api/models/TaskUpdate";
import type { TaskResponse } from "@/api/models/TaskResponse";
import { tasksAPI } from "@/api/tasks";
import { useAuthStore } from "@/stores/auth";

const props = defineProps<{
  modelValue: boolean;
  task: TaskResponse | null;
  projectId: number;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "updated"): void;
}>();

const authStore = useAuthStore();

/**
 * 編集フォーム
 */
const form = ref<TaskUpdate>({});
const saving = ref(false);

/**
 * task → form 反映
 */
const resetForm = (task: TaskResponse) => {
  form.value = {
    name: task.name,
    status: task.status,
    progress: task.progress ?? 0,
    description: task.description ?? "",
    start_date: task.start_date ?? undefined,
    due_date: task.due_date ?? undefined,
    assignee_id: task.assignee_id ?? undefined,
  };
};

watch(
  () => props.task,
  (task) => {
    if (!task) return;
    resetForm(task);
  },
  { immediate: true },
);

/**
 * 保存処理
 */
const saveTask = async () => {
  if (!props.task) return;

  try {
    saving.value = true;

    await tasksAPI.updateTask(props.projectId, props.task.id, form.value);

    emit("updated");
    emit("update:modelValue", false);
  } catch (e) {
    console.error(e);
  } finally {
    saving.value = false;
  }
};

/**
 * 閉じる
 */
const closeDialog = () => {
  emit("update:modelValue", false);
};
</script>

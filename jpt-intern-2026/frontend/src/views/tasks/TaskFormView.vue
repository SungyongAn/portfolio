<template>
  <div class="task-form-view">
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          ダッシュボード
        </el-breadcrumb-item>

        <el-breadcrumb-item :to="{ path: '/projects' }">
          案件一覧
        </el-breadcrumb-item>

        <el-breadcrumb-item :to="{ path: `/projects/${projectId}` }">
          案件詳細
        </el-breadcrumb-item>

        <el-breadcrumb-item>
          {{ isEdit ? "タスク更新" : "タスク登録" }}
        </el-breadcrumb-item>
      </el-breadcrumb>

      <h1 class="page-title">
        {{ isEdit ? "タスク更新" : "タスク登録" }}
      </h1>
    </div>

    <TaskFormCard
      v-model:form-ref="formRef"
      :form="form"
      :rules="rules"
      :users="users"
      :task-status-options="taskStatusOptions"
      :progress-max="progressMax"
      :can-edit-master-fields="canEditMasterFields"
      :can-edit-progress-fields="canEditProgressFields"
    />

    <TaskFormActions
      :is-edit="isEdit"
      :loading="loading"
      :can-submit-task="canSubmitTask"
      :can-manage-task="canManageTask"
      @back="goBack"
      @submit="handleSubmit"
      @delete="handleDelete"
    />
  </div>
</template>

<script setup lang="ts">
import { useTaskForm } from "@/composables/useTaskForm";
import TaskFormCard from "@/components/tasks/TaskFormCard.vue";
import TaskFormActions from "@/components/tasks/TaskFormActions.vue";

const {
  projectId,
  isEdit,
  formRef,
  loading,
  users,
  form,
  rules,
  canManageTask,
  canEditMasterFields,
  canEditProgressFields,
  canSubmitTask,
  taskStatusOptions,
  progressMax,
  handleSubmit,
  handleDelete,
  goBack,
} = useTaskForm();
</script>

<style scoped>
.task-form-view {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}
</style>

<template>
  <el-card shadow="never">
    <template #header>
      <span>タスク情報</span>
    </template>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-position="top"
    >
      <!-- タスク名 -->
      <el-form-item label="タスク名" prop="name">
        <el-input
          v-model="form.name"
          :disabled="!canEditMasterFields"
        />
      </el-form-item>

      <!-- 工程 -->
      <el-form-item label="工程名" prop="phase_name">
        <el-select
          v-model="form.phase_name"
          placeholder="工程を選択してください"
          :disabled="!canEditMasterFields"
        >
          <el-option
            v-for="item in WATERFALL_PHASES"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-form-item>

      <!-- 担当者 -->
      <el-form-item label="担当者" prop="assignee_id">
        <el-select
          v-model="form.assignee_id"
          placeholder="選択してください"
          :disabled="!canEditMasterFields"
        >
          <el-option
            v-for="user in users"
            :key="user.id"
            :label="user.name"
            :value="user.id"
          />
        </el-select>
      </el-form-item>

      <!-- ステータス -->
      <el-form-item label="ステータス" prop="status">
        <el-select
          v-model="form.status"
          :disabled="!canEditProgressFields"
        >
          <el-option
            v-for="(label, value) in taskStatusOptions"
            :key="value"
            :label="label"
            :value="value"
          />
        </el-select>
      </el-form-item>

      <!-- 進捗率 -->
      <el-form-item label="進捗率（%）" prop="progress">
        <el-input-number
          v-model="form.progress"
          :min="0"
          :max="progressMax"
          :disabled="!canEditProgressFields"
        />
      </el-form-item>

      <!-- 開始日 -->
      <el-form-item label="開始日" prop="start_date">
        <el-date-picker
          v-model="form.start_date"
          type="date"
          value-format="YYYY-MM-DD"
          :disabled="!canEditMasterFields"
        />
      </el-form-item>

      <!-- 期限 -->
      <el-form-item label="期限" prop="due_date">
        <el-date-picker
          v-model="form.due_date"
          type="date"
          value-format="YYYY-MM-DD"
          :disabled="!canEditMasterFields"
        />
      </el-form-item>

      <!-- 備考 -->
      <el-form-item label="備考">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          :disabled="!canEditProgressFields"
        />
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import type { FormRules } from "element-plus";
import { WATERFALL_PHASES } from "@/constants/task";
import type { TaskCreate } from "@/api/models/TaskCreate";
import { TaskStatus } from "@/api/models/TaskStatus";

import type { UserResponse } from "@/api/models/UserResponse";

defineProps<{
  form: TaskCreate;
  rules: FormRules;
  users: UserResponse[];
  taskStatusOptions: Partial<Record<TaskStatus, string>>;
  progressMax: number;
  canEditMasterFields: boolean;
  canEditProgressFields: boolean;
}>();
</script>
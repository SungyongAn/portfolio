<template>
  <div class="project-create-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-position="top"
      class="form"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="案件名" prop="name">
        <el-input
          v-model="form.name"
          placeholder="例：顧客管理システム刷新"
          maxlength="50"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="目的・概要" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="4"
          placeholder="なぜこの案件が必要か、何を実現するかを記載してください"
        />
      </el-form-item>

      <el-form-item label="担当部門" prop="department_id">
        <el-input :value="authStore.userName + ' の所属部門'" disabled />
        <div class="form-hint">申請者の所属部門が自動でセットされます</div>
      </el-form-item>

      <el-row :gutter="16">
        <el-col :xs="24" :sm="12">
          <el-form-item label="概算予算（円）" prop="budget_amount">
            <el-input-number
              v-model="form.budget_amount"
              :min="1"
              :precision="0"
              style="width: 100%"
              placeholder="例：500"
            />
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="12">
          <el-form-item label="概算工数（人月）" prop="planned_months">
            <el-input-number
              v-model="form.planned_months"
              :min="0"
              :precision="1"
              style="width: 100%"
              placeholder="例：10"
            />
            <div class="form-hint">任意・入力推奨</div>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :xs="24" :sm="12">
          <el-form-item label="開発開始予定日" prop="start_date">
            <el-date-picker
              v-model="form.start_date"
              type="date"
              placeholder="開始日を選択"
              format="YYYY/MM/DD"
              value-format="YYYY-MM-DD"
              :disabled-date="disabledStartDate"
              style="width: 100%"
            />
            <div class="form-hint">任意</div>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="12">
          <el-form-item label="完了予定日" prop="end_date">
            <el-date-picker
              v-model="form.end_date"
              type="date"
              placeholder="完了日を選択"
              format="YYYY/MM/DD"
              value-format="YYYY-MM-DD"
              :disabled-date="disabledEndDate"
              style="width: 100%"
            />
            <div class="form-hint">任意・開始日以降の日付</div>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <div class="form-actions">
          <el-button @click="emit('cancel')">キャンセル</el-button>

          <el-button type="primary" native-type="submit" :loading="loading">
            申請する
          </el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

import { projectsAPI } from "@/api/projects";
import { useAuthStore } from "@/stores/auth";

const emit = defineEmits<{
  (e: "created"): void;
  (e: "cancel"): void;
}>();

const authStore = useAuthStore();

const formRef = ref<FormInstance>();
const loading = ref(false);

const form = ref({
  name: "",
  description: "",
  budget_amount: undefined as number | undefined,
  planned_months: undefined as number | undefined,
  start_date: "",
  end_date: "",
});

const rules: FormRules = {
  name: [
    { required: true, message: "案件名を入力してください", trigger: "blur" },
    { max: 50, message: "50字以内で入力してください", trigger: "blur" },
  ],
  description: [
    {
      required: true,
      message: "目的・概要を入力してください",
      trigger: "blur",
    },
  ],
  budget_amount: [
    { required: true, message: "概算予算を入力してください", trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value > 999_999_999) {
          callback(new Error("概算予算は999,999,999円以下で入力してください"));
          return;
        }

        callback();
      },
      trigger: "blur",
    },
  ],
  start_date: [
    {
      validator: (_rule, value, callback) => {
        if (!value) {
          callback();
          return;
        }

        const today = new Date().toISOString().substring(0, 10);

        if (value < today) {
          callback(new Error("開始日に過去の日付は選択できません"));
          return;
        }

        callback();
      },
      trigger: "change",
    },
  ],
  end_date: [
    {
      validator: (_rule, value, callback) => {
        if (value && form.value.start_date && value < form.value.start_date) {
          callback(new Error("完了予定日は開始日以降の日付を選択してください"));
          return;
        }

        callback();
      },
      trigger: "change",
    },
  ],
};

const disabledStartDate = (date: Date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return date < today;
};

const disabledEndDate = (date: Date) => {
  if (!form.value.start_date) return false;

  const start = new Date(`${form.value.start_date}T00:00:00`);
  const selectedDate = new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate(),
  );

  return selectedDate < start;
};

watch(
  () => form.value.start_date,
  () => {
    if (form.value.end_date) {
      formRef.value?.validateField("end_date");
    }
  },
);

const resetForm = () => {
  form.value = {
    name: "",
    description: "",
    budget_amount: undefined,
    planned_months: undefined,
    start_date: "",
    end_date: "",
  };
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  loading.value = true;

  try {
    await projectsAPI.createProject({
      name: form.value.name,
      description: form.value.description,
      budget_amount: form.value.budget_amount,
      planned_months: form.value.planned_months,
      start_date: form.value.start_date || undefined,
      end_date: form.value.end_date || undefined,
    });

    ElMessage.success("案件を申請しました");
    resetForm();
    emit("created");
  } catch {
    ElMessage.error("申請に失敗しました");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.project-create-form {
  padding: 8px;
}

.form {
  width: 100%;
}

.form-hint {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.form-actions {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>

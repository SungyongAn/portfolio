<template>
  <div class="expense-form-view">
    <!-- ヘッダー -->
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"
          >ダッシュボード</el-breadcrumb-item
        >
        <el-breadcrumb-item :to="{ path: '/projects' }"
          >案件一覧</el-breadcrumb-item
        >
        <el-breadcrumb-item :to="{ path: `/projects/${projectId}` }"
          >案件詳細</el-breadcrumb-item
        >
        <el-breadcrumb-item :to="{ path: `/projects/${projectId}/budget` }"
          >予算管理</el-breadcrumb-item
        >
        <el-breadcrumb-item>{{
          isEdit ? "直接経費編集" : "直接経費入力"
        }}</el-breadcrumb-item>
      </el-breadcrumb>
      <h1 class="page-title">{{ isEdit ? "直接経費編集" : "直接経費入力" }}</h1>
    </div>

    <el-card shadow="never">
      <template #header>
        <span>直接経費情報</span>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <!-- 経費種別 -->
        <el-form-item label="経費種別" prop="expense_type">
          <el-select
            v-model="form.expense_type"
            placeholder="選択してください"
            style="width: 100%"
          >
            <el-option
              v-for="(label, type) in EXPENSE_TYPE_LABEL"
              :key="type"
              :label="label"
              :value="type"
            />
          </el-select>
        </el-form-item>

        <!-- 金額 -->
        <el-form-item label="金額（円）" prop="amount">
          <el-input-number
            v-model="form.amount"
            :min="0.1"
            :precision="1"
            style="width: 100%"
            placeholder="例：50"
          />
        </el-form-item>

        <!-- 発生日 -->
        <el-form-item label="発生日" prop="expense_date">
          <el-date-picker
            v-model="form.expense_date"
            type="date"
            placeholder="発生日を選択"
            format="YYYY/MM/DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <!-- 備考 -->
        <el-form-item label="備考">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="任意"
          />
        </el-form-item>

        <!-- ボタン -->
        <el-form-item>
          <div class="form-actions">
            <el-button @click="handleCancel">キャンセル</el-button>
            <el-button type="primary" :loading="loading" @click="handleSubmit">
              {{ isEdit ? "更新" : "保存" }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { EXPENSE_TYPE_LABEL } from "@/constants/budget";
import { budgetAPI } from "@/api/budget";
import type { ExpenseCreate } from "@/api/models/ExpenseCreate";
import { ExpenseType } from "@/api/models/ExpenseType";
import { projectsAPI } from "@/api/projects";
import type { ProjectResponse } from "@/api/models/ProjectResponse";

const route = useRoute();
const router = useRouter();

const project = ref<ProjectResponse | null>(null);
const projectId = Number(route.params.projectId);
const expenseId = route.params.expenseId
  ? Number(route.params.expenseId)
  : undefined;
const isEdit = !!expenseId;

const formRef = ref<FormInstance>();
const loading = ref(false);

const form = ref<ExpenseCreate>({
  expense_type: "OTHER" as ExpenseType,
  amount: undefined as unknown as number,
  expense_date: "",
  description: "",
});

const rules: FormRules = {
  expense_type: [
    {
      required: true,
      message: "経費種別を選択してください",
      trigger: "change",
    },
  ],
  amount: [
    { required: true, message: "金額を入力してください", trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value <= 0) {
          callback(new Error("金額は0より大きい値を入力してください"));
        } else if (value > 999_999_999) {
          callback(new Error("金額は999,999,999円以下で入力してください"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  expense_date: [
    { required: true, message: "発生日を選択してください", trigger: "change" },
    {
      validator: (_rule, value, callback) => {
        if (!value) {
          callback();
          return;
        }
        const today = new Date().toISOString().substring(0, 10);
        if (value > today) {
          callback(new Error("未来の日付は登録できません"));
          return;
        }
        if (project.value?.start_date) {
          const projectStartDate = project.value.start_date.substring(0, 10);
          if (value < projectStartDate) {
            callback(
              new Error(
                `案件開始日（${projectStartDate}）以降を選択してください`,
              ),
            );
            return;
          }
        }
        callback();
      },
      trigger: "change",
    },
  ],
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  loading.value = true;
  try {
    if (isEdit) {
      await budgetAPI.updateExpense(projectId, expenseId!, form.value);
      ElMessage.success("直接経費を更新しました");
    } else {
      await budgetAPI.createExpense(projectId, form.value);
      ElMessage.success("直接経費を登録しました");
    }
    router.push(`/projects/${projectId}/budget`);
  } catch {
    ElMessage.error(isEdit ? "更新に失敗しました" : "登録に失敗しました");
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  router.push(`/projects/${projectId}/budget`);
};

onMounted(async () => {
  try {
    const response = await projectsAPI.getProject(projectId);
    project.value = response.data;

    // 編集時：既存データを取得
    if (isEdit) {
      const expensesResponse = await budgetAPI.getExpenses(projectId);
      const expense = expensesResponse.data.find((e) => e.id === expenseId);
      if (expense) {
        form.value = {
          expense_type: expense.expense_type as ExpenseType,
          amount: expense.amount,
          expense_date: expense.expense_date,
          description: expense.description ?? "",
        };
      }
    }
  } catch (error) {
    console.error("データの取得に失敗しました", error);
  }
});
</script>

<style scoped>
.expense-form-view {
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
}
</style>

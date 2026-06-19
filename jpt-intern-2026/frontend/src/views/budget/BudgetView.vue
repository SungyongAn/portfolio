<template>
  <div class="budget-view">
    <!-- ヘッダー -->
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"
          >ダッシュボード</el-breadcrumb-item
        >
        <el-breadcrumb-item :to="{ path: '/projects' }">
          {{ authStore.isApplicant ? "申請中案件一覧" : "案件一覧" }}
        </el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/projects/${projectId}` }"
          >案件詳細</el-breadcrumb-item
        >
        <el-breadcrumb-item>予算管理</el-breadcrumb-item>
      </el-breadcrumb>
      <h1 class="page-title">予算管理</h1>
    </div>

    <!-- サマリー -->
    <el-card shadow="never" class="mb-16">
      <template #header>
        <span>予算サマリー</span>
      </template>
      <div v-if="summary">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="計画工数">
            {{ summary.planned_months }} 人月
          </el-descriptions-item>
          <el-descriptions-item label="実績工数">
            {{ summary.actual_months }} 人月
          </el-descriptions-item>
          <el-descriptions-item label="工数消化率">
            <el-tag :type="getRateType(summary.months_consumption_rate)">
              {{ summary.months_consumption_rate }} %
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="残工数">
            {{ summary.remaining_months }} 人月
          </el-descriptions-item>
          <el-descriptions-item label="予算金額">
            {{ summary.budget_amount.toLocaleString() }} 円
          </el-descriptions-item>
          <el-descriptions-item label="実績金額">
            {{ summary.actual_amount.toLocaleString() }} 円
          </el-descriptions-item>
          <el-descriptions-item label="金額消化率">
            <el-tag :type="getRateType(summary.amount_consumption_rate)">
              {{ summary.amount_consumption_rate }} %
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="残予算">
            {{ summary.remaining_amount.toLocaleString() }} 円
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <el-empty v-else description="予算情報がありません" />
    </el-card>

    <!-- 工数実績一覧 -->
    <el-card shadow="never" class="mb-16">
      <template #header>
        <div class="card-header">
          <span>工数実績一覧</span>
          <el-button
            v-if="canInput"
            type="primary"
            size="small"
            @click="goWorklog"
          >
            工数実績入力
          </el-button>
        </div>
      </template>
      <el-table :data="worklogs" border>
        <el-table-column prop="work_month" label="対象月" width="120" />
        <el-table-column
          prop="actual_months"
          label="実績工数（人月）"
          width="160"
        />
        <el-table-column label="金額（円）" width="160">
          <template #default="{ row }">
            {{ (Number(row.actual_months) * row.unit_price).toLocaleString() }}
            円
          </template>
        </el-table-column>
        <el-table-column label="" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="canInput"
              type="primary"
              size="small"
              text
              :icon="Edit"
              @click="
                router.push(
                  `/projects/${projectId}/budget/worklogs/${row.id}/edit`,
                )
              "
            />
            <el-button
              v-if="canInput"
              type="danger"
              size="small"
              text
              :icon="Delete"
              @click="handleDeleteWorklog(row.id)"
            />
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="工数実績がありません" />
        </template>
      </el-table>
    </el-card>

    <!-- 直接経費一覧 -->
    <el-card shadow="never" class="mb-16">
      <template #header>
        <div class="card-header">
          <span>直接経費一覧</span>
          <el-button
            v-if="canInput"
            type="success"
            size="small"
            @click="goExpense"
          >
            直接経費入力
          </el-button>
        </div>
      </template>
      <el-table :data="expenses" border>
        <el-table-column prop="expense_date" label="発生日" width="120" />
        <el-table-column label="経費種別" width="140">
          <template #default="{ row }">
            {{ EXPENSE_TYPE_LABEL[row.expense_type as ExpenseType] }}
          </template>
        </el-table-column>
        <el-table-column label="金額（円）" width="140">
          <template #default="{ row }">
            {{ Number(row.amount).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="備考" />
        <el-table-column label="" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="canInput"
              type="primary"
              size="small"
              text
              :icon="Edit"
              @click="
                router.push(
                  `/projects/${projectId}/budget/expenses/${row.id}/edit`,
                )
              "
            />
            <el-button
              v-if="canInput"
              type="danger"
              size="small"
              text
              :icon="Delete"
              @click="handleDeleteExpense(row.id)"
            />
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="直接経費がありません" />
        </template>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { ElMessage, ElMessageBox } from "element-plus";
import { EXPENSE_TYPE_LABEL } from "@/constants/budget";
import { projectsAPI } from "@/api/projects";
import { budgetAPI } from "@/api/budget";
import type { ProjectResponse } from "@/api/models/ProjectResponse";
import { ProjectStatus } from "@/api/models/ProjectStatus";
import type { ProjectBudgetResponse } from "@/api/models/ProjectBudgetResponse";
import type { WorklogResponse } from "@/api/models/WorklogResponse";
import type { ExpenseResponse } from "@/api/models/ExpenseResponse";
import { ExpenseType } from "@/api/models/ExpenseType";
import { Edit, Delete } from "@element-plus/icons-vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const projectId = Number(route.params.projectId);

const project = ref<ProjectResponse | null>(null);
const budget = ref<ProjectBudgetResponse | null>(null);
const worklogs = ref<WorklogResponse[]>([]);
const expenses = ref<ExpenseResponse[]>([]);

const summary = computed(() => {
  if (!budget.value) return null;

  const budgetAmount = budget.value.budget_amount;
  const actualAmount = budget.value.actual_amount;
  const plannedMonths = budget.value.planned_months ?? 0;
  const actualMonths = worklogs.value.reduce(
    (sum, w) => sum + parseFloat(w.actual_months),
    0,
  );
  const monthsRate =
    plannedMonths > 0 ? Math.round((actualMonths / plannedMonths) * 100) : 0;

  return {
    planned_months: plannedMonths,
    actual_months: Math.round(actualMonths * 100) / 100,
    months_consumption_rate: monthsRate,
    remaining_months: Math.round((plannedMonths - actualMonths) * 100) / 100,
    budget_amount: budgetAmount,
    actual_amount: actualAmount,
    amount_consumption_rate: budget.value.consumption_rate ?? 0,
    remaining_amount: budgetAmount - actualAmount,
  };
});

const canInput = computed(() => {
  if (!project.value) return false;

  return (
    authStore.role === "APPLICANT" &&
    [ProjectStatus.APPROVED, ProjectStatus.IN_PROGRESS].includes(
      project.value.status,
    ) &&
    budget.value !== null
  );
});

const getRateType = (rate: number) => {
  if (rate >= 100) return "danger";
  if (rate >= 80) return "warning";
  return "success";
};

onMounted(async () => {
  try {
    const projectRes = await projectsAPI.getProject(projectId);
    project.value = projectRes.data;

    // 承認済み以降のステータスのみworklogs・expenses・budgetを取得する
    const approvedStatuses = [
      ProjectStatus.APPROVED,
      ProjectStatus.IN_PROGRESS,
      ProjectStatus.COMPLETED,
    ];

    if (project.value && approvedStatuses.includes(project.value.status)) {
      const [worklogsRes, expensesRes] = await Promise.all([
        budgetAPI.getWorklogs(projectId),
        budgetAPI.getExpenses(projectId),
      ]);
      worklogs.value = worklogsRes.data;
      expenses.value = expensesRes.data;

      try {
        const budgetRes = await budgetAPI.getBudget(projectId);
        budget.value = budgetRes.data;
      } catch {
        // 予算未登録
      }
    }
  } catch (error) {
    console.error("データの取得に失敗しました", error);
  }
});

const goWorklog = () => {
  router.push(`/projects/${projectId}/budget/worklogs/new`);
};

const goExpense = () => {
  router.push(`/projects/${projectId}/budget/expenses/new`);
};

const handleDeleteWorklog = async (worklogId: number) => {
  try {
    await ElMessageBox.confirm(
      "この工数実績を削除してよろしいですか？",
      "削除確認",
      {
        type: "warning",
        confirmButtonText: "削除",
        cancelButtonText: "キャンセル",
        confirmButtonClass: "el-button--danger",
      },
    );
  } catch {
    return;
  }
  try {
    await budgetAPI.deleteWorklog(projectId, worklogId);
    worklogs.value = worklogs.value.filter((w) => w.id !== worklogId);
    const budgetRes = await budgetAPI.getBudget(projectId);
    budget.value = budgetRes.data;
    ElMessage.success("工数実績を削除しました");
  } catch {
    ElMessage.error("削除に失敗しました");
  }
};

const handleDeleteExpense = async (expenseId: number) => {
  try {
    await ElMessageBox.confirm(
      "この直接経費を削除してよろしいですか？",
      "削除確認",
      {
        type: "warning",
        confirmButtonText: "削除",
        cancelButtonText: "キャンセル",
        confirmButtonClass: "el-button--danger",
      },
    );
  } catch {
    return;
  }
  try {
    await budgetAPI.deleteExpense(projectId, expenseId);
    expenses.value = expenses.value.filter((e) => e.id !== expenseId);
    const budgetRes = await budgetAPI.getBudget(projectId);
    budget.value = budgetRes.data;
    ElMessage.success("直接経費を削除しました");
  } catch {
    ElMessage.error("削除に失敗しました");
  }
};
</script>

<style scoped>
.budget-view {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}
</style>

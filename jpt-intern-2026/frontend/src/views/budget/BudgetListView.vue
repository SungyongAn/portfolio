<template>
  <div class="budget-list-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">予算管理</h1>
        <p class="page-subtitle">{{ pageSubtitle }}</p>
      </div>

      <BudgetFilters
        v-model:keyword="keyword"
        v-model:status-filter="statusFilter"
        v-model:department-filter="departmentFilter"
        v-model:budget-filter="budgetFilter"
        :departments="departments"
        :show-department-filter="!authStore.isDeptManager"
      />
    </div>

    <BudgetSummaryCards :summary="summary" />

    <BudgetProjectTable
      :projects="projects"
      :departments="departments"
      :loading="loading"
      :total="total"
      :current-page="currentPage"
      :page-size="pageSize"
      @sort-change="handleSortChange"
      @page-change="handlePageChange"
      @detail="goDetail"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import BudgetFilters from "@/components/budget/BudgetFilters.vue";
import BudgetSummaryCards from "@/components/budget/BudgetSummaryCards.vue";
import BudgetProjectTable from "@/components/budget/BudgetProjectTable.vue";
import { useBudgetList } from "@/composables/useBudgetList";

const router = useRouter();
const authStore = useAuthStore();

const pageSubtitle = computed(() =>
  authStore.isDeptManager
    ? "自部門の予算・実績・消化率を確認できます"
    : "全案件の予算・実績・消化率を確認できます",
);

const {
  loading,
  projects,
  departments,
  total,
  currentPage,
  pageSize,
  keyword,
  statusFilter,
  departmentFilter,
  budgetFilter,
  summary,
  handleSortChange,
  handlePageChange,
} = useBudgetList();

const goDetail = (projectId: number) => {
  router.push(`/projects/${projectId}/budget`);
};
</script>

<style scoped>
.budget-list-view {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
</style>

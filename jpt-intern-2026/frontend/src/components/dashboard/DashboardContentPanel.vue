<template>
  <el-card v-if="mode !== 'summary'" class="content-panel" shadow="never">
    <!-- KPIカード選択時：承認待ち / 危険 / 注意 -->
    <DashboardProjectList
      v-if="mode !== 'projects'"
      :projects="projects"
      :loading="loading"
      :filter="dashboardFilter"
      @move="handleMove"
    />

    <!-- サイドメニュー「案件一覧」選択時 -->
    <div v-else class="project-list-area">
      <div class="filters">
        <el-input
          v-model="keyword"
          placeholder="案件名で検索"
          clearable
          class="filter-input"
        />

        <el-select
          v-model="selectedStatus"
          placeholder="ステータスで絞り込み"
          clearable
          class="filter-select"
        >
          <el-option label="下書き" value="DRAFT" />
          <el-option label="部門承認待ち" value="PENDING_DEPT" />
          <el-option label="本部承認待ち" value="PENDING_HQ" />
          <el-option label="承認済み" value="APPROVED" />
          <el-option label="進行中" value="IN_PROGRESS" />
          <el-option label="完了" value="COMPLETED" />
          <el-option label="却下" value="REJECTED" />
        </el-select>

        <el-button @click="clearFilters">クリア</el-button>
      </div>

      <el-table :data="projects" :loading="loading" border stripe>
        <el-table-column prop="name" label="案件名" min-width="240">
          <template #default="{ row }">
            <el-link type="primary" @click="handleMove(row.id)">
              {{ row.name }}
            </el-link>
          </template>
        </el-table-column>

        <el-table-column prop="department_name" label="部門" width="180" />

        <el-table-column label="ステータス" width="150">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">
              {{ statusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="進捗率" width="140">
          <template #default="{ row }">
            {{ formatRate(row.progress) }}
          </template>
        </el-table-column>

        <el-table-column label="予算消化率" width="140">
          <template #default="{ row }">
            {{ formatRate(row.consumption_rate) }}
          </template>
        </el-table-column>

        <el-table-column label="申請日" width="140">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="props.total"
          layout="total, sizes, prev, pager, next"
          @current-change="handlePageChange"
          @size-change="handlePageChange"
        />
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";

import DashboardProjectList from "@/components/dashboard/DashboardProjectList.vue";

import type { ProjectDashboard } from "@/api/dashboard";
import type { DashboardMode, ManagementFilter } from "@/types/dashboard";

const props = defineProps<{
  mode: DashboardMode;
  projects: ProjectDashboard[];
  total: number;
  loading?: boolean;
}>();

const emit = defineEmits<{
  back: [];
  "open-project": [projectId: number];
  "open-approval": [projectId: number];
  "page-change": [page: number, limit: number, keyword: string, status: string];
}>();

const keyword = ref("");
const selectedStatus = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const handleMove = (projectId: number) => {
  if (props.mode === "pending") {
    emit("open-approval", projectId);
    return;
  }

  emit("open-project", projectId);
};

const handlePageChange = () => {
  emit(
    "page-change",
    currentPage.value,
    pageSize.value,
    keyword.value,
    selectedStatus.value,
  );
};

const dashboardFilter = computed<ManagementFilter>(() => {
  switch (props.mode) {
    case "pending":
      return "pending";
    case "active":
      return "active";
    case "danger":
      return "danger";
    case "warning":
      return "warning";
    case "budget":
      return "budget";
    default:
      return "active";
  }
});

const clearFilters = () => {
  keyword.value = "";
  selectedStatus.value = "";
  currentPage.value = 1;

  emit(
    "page-change",
    currentPage.value,
    pageSize.value,
    keyword.value,
    selectedStatus.value,
  );
};

const statusLabel = (status: string) => {
  const labels: Record<string, string> = {
    DRAFT: "下書き",
    PENDING_DEPT: "部門承認待ち",
    PENDING_HQ: "本部承認待ち",
    APPROVED: "承認済み",
    IN_PROGRESS: "進行中",
    COMPLETED: "完了",
    REJECTED: "却下",
  };

  return labels[status] ?? status;
};

const statusTagType = (
  status: string,
): "success" | "warning" | "danger" | "info" | "primary" => {
  const types: Record<
    string,
    "success" | "warning" | "danger" | "info" | "primary"
  > = {
    DRAFT: "info",
    PENDING_DEPT: "warning",
    PENDING_HQ: "warning",
    APPROVED: "info",
    IN_PROGRESS: "primary",
    COMPLETED: "success",
    REJECTED: "danger",
  };

  return types[status] ?? "info";
};

const formatDate = (date?: string | null) => {
  if (!date) return "—";
  return date.slice(0, 10);
};

const formatRate = (value?: number | null) => {
  if (value === null || value === undefined) {
    return "—";
  }

  return `${value}%`;
};

watch(
  () => [keyword.value, selectedStatus.value],
  () => {
    currentPage.value = 1;

    emit(
      "page-change",
      currentPage.value,
      pageSize.value,
      keyword.value,
      selectedStatus.value,
    );
  },
);
</script>

<style scoped>
.content-panel {
  margin-top: 16px;
  border-radius: 12px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.panel-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}

.panel-description {
  margin: 6px 0 0;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.project-list-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filters {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-input {
  max-width: 360px;
}

.filter-select {
  max-width: 280px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 4px;
}

@media (max-width: 768px) {
  .panel-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .filters {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-input,
  .filter-select {
    max-width: none;
    width: 100%;
  }

  .pagination-wrapper {
    justify-content: center;
  }
}
</style>

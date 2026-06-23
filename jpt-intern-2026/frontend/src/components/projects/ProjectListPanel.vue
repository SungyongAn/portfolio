<template>
  <el-card class="project-list-panel" shadow="never">
    <div class="filter-area">
      <el-input
        v-model="keyword"
        placeholder="案件名で検索"
        clearable
        class="filter-input"
        @keyup.enter="fetchProjects"
      />

      <el-select
        v-model="statusFilter"
        placeholder="ステータス"
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

      <el-select
        v-if="showDepartmentFilter"
        v-model="departmentId"
        placeholder="部門"
        clearable
        class="filter-select"
      >
        <el-option
          v-for="department in departments"
          :key="department.id"
          :label="department.name"
          :value="department.id"
        />
      </el-select>

      <el-select
        v-model="alertLevel"
        placeholder="アラート"
        clearable
        class="filter-select"
      >
        <el-option label="危険" value="danger" />
        <el-option label="注意" value="warning" />
      </el-select>

      <el-button type="primary" @click="fetchProjects"> 検索 </el-button>

      <el-button @click="clearFilters"> クリア </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="projects"
      border
      stripe
      class="project-table"
      empty-text="該当する案件はありません"
    >
      <el-table-column prop="name" label="案件名" min-width="240">
        <template #default="{ row }">
          <el-link type="primary" @click="openProject(row.id)">
            {{ row.name }}
          </el-link>
        </template>
      </el-table-column>

      <el-table-column label="ステータス" width="150">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)">
            {{ statusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column
        v-if="showDepartmentColumn"
        prop="department_name"
        label="部門"
        width="160"
      >
        <template #default="{ row }">
          {{ row.department_name ?? departmentName(row.department_id) }}
        </template>
      </el-table-column>

      <el-table-column label="予算" width="130" align="right">
        <template #default="{ row }">
          {{ formatCurrency(getBudgetAmount(row)) }}
        </template>
      </el-table-column>

      <el-table-column label="実績" width="130" align="right">
        <template #default="{ row }">
          {{ formatCurrency(getActualAmount(row)) }}
        </template>
      </el-table-column>

      <el-table-column label="消費率" width="110" align="center">
        <template #default="{ row }">
          <el-tag :type="consumptionTagType(getConsumptionRate(row))">
            {{ getConsumptionRate(row) ?? 0 }}%
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="アラート" width="120" align="center">
        <template #default="{ row }">
          <el-tag
            v-if="row.alert_level"
            :type="row.alert_level === 'danger' ? 'danger' : 'warning'"
          >
            {{ row.alert_level === "danger" ? "危険" : "注意" }}
          </el-tag>
          <span v-else>—</span>
        </template>
      </el-table-column>

      <el-table-column label="作成日" width="130">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-area">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="limit"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        background
        @current-change="fetchProjects"
        @size-change="handleSizeChange"
      />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

import { projectsAPI } from "@/api/projects";
import { departmentsAPI, type Department } from "@/api/departments";
import type { ProjectResponse } from "@/api/models/ProjectResponse";

const props = withDefaults(
  defineProps<{
    initialStatus?: string;
    initialAlertLevel?: string;
    initialDepartmentId?: number | null;
  }>(),
  {
    initialStatus: "",
    initialAlertLevel: "",
    initialDepartmentId: null,
  },
);

const router = useRouter();

const loading = ref(false);

type ProjectListItem = ProjectResponse & {
  budget_amount?: number | string | null;
  actual_amount?: number | string | null;
  consumption_rate?: number | string | null;
  alert_level?: "danger" | "warning" | "normal" | null;
  department_name?: string | null;
};

const getNestedBudgetValue = (
  project: ProjectListItem,
  key: "budget_amount" | "actual_amount",
): unknown => {
  const budget = (project as Record<string, unknown>).budget;

  if (!budget || typeof budget !== "object") {
    return undefined;
  }

  return (budget as Record<string, unknown>)[key];
};

const getBudgetAmount = (project: ProjectListItem): number | null => {
  return toNumber(
    project.budget_amount ?? getNestedBudgetValue(project, "budget_amount"),
  );
};

const getActualAmount = (project: ProjectListItem): number | null => {
  return toNumber(
    project.actual_amount ?? getNestedBudgetValue(project, "actual_amount"),
  );
};

const projects = ref<ProjectListItem[]>([]);
const departments = ref<Department[]>([]);

const page = ref(1);
const limit = ref(10);
const total = ref(0);

const keyword = ref("");
const statusFilter = ref(props.initialStatus);
const departmentId = ref<number | null>(props.initialDepartmentId);
const alertLevel = ref(props.initialAlertLevel);

const showDepartmentFilter = computed(() => departments.value.length > 0);
const showDepartmentColumn = computed(() => departments.value.length > 0);

const toNumber = (value: unknown): number | null => {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  const numberValue = Number(value);
  return Number.isNaN(numberValue) ? null : numberValue;
};

const getConsumptionRate = (project: ProjectListItem): number | null => {
  return toNumber(project.consumption_rate);
};

const formatCurrency = (value?: number | null) => {
  if (value === null || value === undefined) {
    return "—";
  }

  return `${value.toLocaleString()}円`;
};

const fetchDepartments = async () => {
  try {
    const res = await departmentsAPI.getDepartments();
    departments.value = res.data;
  } catch (error) {
    console.error("部門一覧の取得に失敗しました", error);
  }
};

const fetchProjects = async () => {
  loading.value = true;

  try {
    const statuses = statusFilter.value ? [statusFilter.value] : undefined;

    const res = await projectsAPI.getProjects(
      page.value,
      limit.value,
      statuses,
      keyword.value || undefined,
      departmentId.value ?? undefined,
      undefined,
      undefined,
      undefined, // sortBy
      undefined, // sortOrder
      alertLevel.value || undefined,
    );

    projects.value = (res.data.items ?? []) as ProjectListItem[];

    total.value = res.data.total ?? 0;
  } catch (error) {
    console.error("案件一覧の取得に失敗しました", error);
  } finally {
    loading.value = false;
  }
};

const clearFilters = async () => {
  keyword.value = "";
  statusFilter.value = "";
  departmentId.value = props.initialDepartmentId ?? null;
  alertLevel.value = props.initialAlertLevel ?? "";
  page.value = 1;

  await fetchProjects();
};

const handleSizeChange = async () => {
  page.value = 1;
  await fetchProjects();
};

const openProject = (projectId: number) => {
  router.push(`/projects/${projectId}`);
};

const departmentName = (id?: number | null) => {
  if (!id) return "—";
  return (
    departments.value.find((department) => department.id === id)?.name ??
    String(id)
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

const consumptionTagType = (
  rate?: number | null,
): "success" | "warning" | "danger" | "info" => {
  const value = rate ?? 0;

  if (value >= 100) return "danger";
  if (value >= 80) return "warning";
  if (value > 0) return "success";

  return "info";
};

const formatDate = (value?: string | null) => {
  if (!value) return "—";
  return value.slice(0, 10);
};

watch(
  () => [
    props.initialAlertLevel,
    props.initialDepartmentId,
    props.initialStatus,
  ],
  async () => {
    alertLevel.value = props.initialAlertLevel ?? "";
    departmentId.value = props.initialDepartmentId ?? null;
    statusFilter.value = props.initialStatus ?? "";
    page.value = 1;
    await fetchProjects();
  },
);

onMounted(async () => {
  await fetchDepartments();
  await fetchProjects();
});
</script>

<style scoped>
.project-list-panel {
  border-radius: 12px;
}

.filter-area {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.filter-input {
  width: 260px;
}

.filter-select {
  width: 180px;
}

.project-table {
  width: 100%;
}

.pagination-area {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .filter-area {
    flex-direction: column;
  }

  .filter-input,
  .filter-select {
    width: 100%;
  }

  .pagination-area {
    justify-content: center;
  }
}
</style>

<template>
  <div class="member-task-view">
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          ダッシュボード
        </el-breadcrumb-item>
        <el-breadcrumb-item>メンバータスク状況</el-breadcrumb-item>
      </el-breadcrumb>
      <h1 class="page-title">メンバータスク状況</h1>
    </div>

    <!-- メンバーサマリ -->
    <el-row :gutter="12" class="mb-16" v-loading="loading">
      <el-col
        v-for="member in memberSummaries"
        :key="member.id"
        :xs="24"
        :sm="12"
        :md="8"
        class="mb-16"
      >
        <el-card
          shadow="never"
          class="summary-card"
          :class="{
            'summary-card-danger': member.overdueCount > 0,
            'summary-card-active': filterAssignee === member.id,
          }"
          @click="toggleMemberFilter(member.id)"
        >
          <div class="summary-header">
            <el-avatar :size="32" :icon="UserFilled" />
            <span class="summary-name">{{ member.name }}</span>
            <el-tag
              v-if="member.overdueCount > 0"
              type="danger"
              size="small"
              class="ml-8"
            >
              期限超過 {{ member.overdueCount }}件
            </el-tag>
            <el-tag
              v-else-if="member.inProgressCount === 0"
              type="success"
              size="small"
              class="ml-8"
            >
              余裕あり
            </el-tag>
          </div>

          <el-divider style="margin: 8px 0" />

          <div class="summary-stats">
            <div class="stat-item">
              <span class="stat-label">担当タスク</span>
              <span class="stat-value">{{ member.totalCount }}件</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">進行中</span>
              <span class="stat-value">{{ member.inProgressCount }}件</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">完了</span>
              <span class="stat-value text-success">
                {{ member.doneCount }}件
              </span>
            </div>
            <div class="stat-item">
              <span class="stat-label">未着手</span>
              <span class="stat-value">{{ member.todoCount }}件</span>
            </div>
          </div>

          <el-progress
            :percentage="member.completionRate"
            :color="member.overdueCount > 0 ? '#f56c6c' : undefined"
            :stroke-width="6"
          />
        </el-card>
      </el-col>
    </el-row>

    <!-- フィルター -->
    <el-card shadow="never" class="filter-card">
      <el-row :gutter="12">
        <el-col :xs="24" :sm="10">
          <el-select
            v-model="filterAssignee"
            placeholder="担当者で絞り込み"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="user in assignees"
              :key="user.id"
              :label="user.name"
              :value="user.id"
            />
          </el-select>
        </el-col>

        <el-col :xs="24" :sm="10">
          <el-select
            v-model="filterStatus"
            placeholder="ステータスで絞り込み"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="(label, value) in TASK_STATUS_LABEL"
              :key="value"
              :label="label"
              :value="value"
            />
          </el-select>
        </el-col>

        <el-col :xs="24" :sm="4">
          <el-button style="width: 100%" @click="resetFilter">
            クリア
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- タスク一覧 -->
    <el-card shadow="never">
      <el-table
        :data="filteredTasks"
        border
        stripe
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column label="担当者" width="120">
          <template #default="{ row }">
            {{ row.assignee_name ?? userName(row.assignee_id) }}
          </template>
        </el-table-column>

        <el-table-column prop="name" label="タスク名" min-width="160" />

        <el-table-column label="案件名" min-width="160">
          <template #default="{ row }">
            {{ projectName(row.project_id) }}
          </template>
        </el-table-column>

        <el-table-column label="ステータス" width="130">
          <template #default="{ row }">
            <el-tag :type="TASK_STATUS_TYPE[row.status as TaskStatus]">
              {{ TASK_STATUS_LABEL[row.status as TaskStatus] }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="進捗率" width="160">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="8" />
          </template>
        </el-table-column>

        <el-table-column label="期限" width="120">
          <template #default="{ row }">
            <span :class="{ overdue: isOverdue(row.due_date) }">
              {{ row.due_date ?? "未設定" }}
            </span>
          </template>
        </el-table-column>

        <template #empty>
          <el-empty description="タスクがありません" />
        </template>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { UserFilled } from "@element-plus/icons-vue";
import { tasksAPI } from "@/api/tasks";
import { usersAPI } from "@/api/users";
import { projectsAPI } from "@/api/projects";
import { TASK_STATUS_LABEL, TASK_STATUS_TYPE } from "@/constants/task";
import { TaskStatus } from "@/api/models/TaskStatus";
import type { TaskResponse } from "@/api/models/TaskResponse";
import type { UserResponse } from "@/api/models/UserResponse";
import type { ProjectResponse } from "@/api/models/ProjectResponse";

const authStore = useAuthStore();

const loading = ref(false);
const tasks = ref<TaskResponse[]>([]);
const users = ref<UserResponse[]>([]);
const projects = ref<ProjectResponse[]>([]);

const filterAssignee = ref<number | null>(null);
const filterStatus = ref<string>("");

// ── メンバーサマリ ────────────────────────────────────
const memberSummaries = computed(() => {
  const today = new Date().toISOString().substring(0, 10);

  return users.value
    .map((user) => {
      const userTasks = tasks.value.filter((t) => t.assignee_id === user.id);
      const totalCount = userTasks.length;
      const doneCount = userTasks.filter((t) => t.status === "DONE").length;
      const inProgressCount = userTasks.filter(
        (t) => t.status === "IN_PROGRESS",
      ).length;
      const todoCount = userTasks.filter((t) => t.status === "TODO").length;
      const overdueCount = userTasks.filter(
        (t) => t.due_date && t.due_date < today && t.status !== "DONE",
      ).length;
      const completionRate =
        totalCount > 0 ? Math.round((doneCount / totalCount) * 100) : 0;

      return {
        id: user.id,
        name: user.name,
        totalCount,
        doneCount,
        inProgressCount,
        todoCount,
        overdueCount,
        completionRate,
      };
    })
    .filter((m) => m.totalCount > 0);
});

// ── フィルター ────────────────────────────────────────
const assignees = computed(() => {
  const ids = new Set(tasks.value.map((t) => t.assignee_id).filter(Boolean));
  return users.value.filter((u) => ids.has(u.id));
});

const filteredTasks = computed(() => {
  return tasks.value.filter((t) => {
    if (filterAssignee.value && t.assignee_id !== filterAssignee.value) {
      return false;
    }

    if (filterStatus.value && t.status !== filterStatus.value) {
      return false;
    }

    return true;
  });
});

const toggleMemberFilter = (memberId: number) => {
  filterAssignee.value = filterAssignee.value === memberId ? null : memberId;
};

// ── ヘルパー ─────────────────────────────────────────
const userName = (id: number | null): string => {
  if (!id) return "未割当";
  return users.value.find((u) => u.id === id)?.name ?? String(id);
};

const projectName = (id: number): string => {
  return projects.value.find((p) => p.id === id)?.name ?? String(id);
};

const isOverdue = (dueDate: string | null): boolean => {
  if (!dueDate) return false;
  return dueDate < new Date().toISOString().substring(0, 10);
};

const resetFilter = () => {
  filterAssignee.value = null;
  filterStatus.value = "";
};

// ── データ取得 ────────────────────────────────────────
onMounted(async () => {
  if (!authStore.departmentId) return;

  loading.value = true;

  try {
    const [tasksRes, usersRes, projectsRes] = await Promise.all([
      tasksAPI.getDepartmentTasks(authStore.departmentId),
      usersAPI.getDepartmentUsers(authStore.departmentId),
      projectsAPI.getProjects(1, 100),
    ]);

    tasks.value = tasksRes.data;
    users.value = usersRes.data;
    projects.value = projectsRes.data.items;
  } catch (error) {
    console.error("データの取得に失敗しました", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.member-task-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 16px;
}

.summary-card {
  cursor: pointer;
  transition:
    transform 0.15s ease,
    border-color 0.15s ease,
    box-shadow 0.15s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.18);
}

.summary-card-active {
  border-color: #409eff;
  box-shadow: 0 0 0 1px rgba(64, 158, 255, 0.35);
  background: #f5faff;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.summary-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 4px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-label {
  font-size: 11px;
  color: #909399;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.text-success {
  color: #67c23a;
}

.summary-card-danger {
  border-color: #fde2e2;
  background: #fff5f5;
}

.summary-card-danger.summary-card-active {
  border-color: #f56c6c;
  box-shadow: 0 0 0 1px rgba(245, 108, 108, 0.35);
}

.ml-8 {
  margin-left: 8px;
}

.overdue {
  color: #f56c6c;
  font-weight: 600;
}
</style>

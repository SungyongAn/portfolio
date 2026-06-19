<template>
  <div class="task-member-dashboard">
    <div class="summary-cards">
      <el-card
        class="summary-card info"
        shadow="hover"
        @click="showTasks('all')"
      >
        <div class="card-title">担当タスク数</div>
        <div class="card-value">
          {{ summary?.total_tasks ?? 0 }}<span>件</span>
        </div>
        <div class="card-desc">自分に割り当てられたタスク</div>
      </el-card>

      <el-card
        class="summary-card warning"
        shadow="hover"
        @click="showTasks('today_deadline')"
      >
        <div class="card-title">今日期限</div>
        <div class="card-value">
          {{ summary?.today_deadline ?? 0 }}<span>件</span>
        </div>
        <div class="card-desc">本日中に対応が必要なタスク</div>
      </el-card>

      <el-card
        class="summary-card danger"
        shadow="hover"
        @click="showTasks('overdue')"
      >
        <div class="card-title">期限超過</div>
        <div class="card-value">{{ summary?.overdue ?? 0 }}<span>件</span></div>
        <div class="card-desc">期限を過ぎた未完了タスク</div>
      </el-card>

      <el-card
        class="summary-card success"
        shadow="hover"
        @click="showTasks('in_progress')"
      >
        <div class="card-title">進行中</div>
        <div class="card-value">
          {{ summary?.in_progress ?? 0 }}<span>件</span>
        </div>
        <div class="card-desc">現在作業中のタスク</div>
      </el-card>

      <el-card
        class="summary-card review"
        shadow="hover"
        @click="showTasks('in_review')"
      >
        <div class="card-title">レビュー中</div>
        <div class="card-value">
          {{ summary?.in_review ?? 0 }}<span>件</span>
        </div>
        <div class="card-desc">確認待ちのタスク</div>
      </el-card>
    </div>

    <template v-if="props.activePanel === 'tasks'">
      <el-card shadow="never" class="task-card" v-loading="loading">
        <template #header>
          <div class="section-header">
            <div>
              <div class="section-title">
                {{ tableTitle }}
              </div>
              <div class="section-subtitle">
                自分に割り当てられたタスクの状況を確認できます
              </div>
            </div>

            <el-button
              v-if="selectedFilter !== 'all'"
              type="primary"
              plain
              round
              size="small"
              @click="showTasks('all')"
            >
              ↺ 全件表示に戻る
            </el-button>
          </div>
        </template>

        <el-table
          v-if="filteredTasks.length > 0"
          :data="filteredTasks"
          stripe
          @row-click="handleRowClick"
        >
          <el-table-column label="優先度" width="90">
            <template #default="{ row }">
              <el-tag
                v-if="row.priority === 'danger'"
                type="danger"
                effect="dark"
              >
                超過
              </el-tag>

              <el-tag
                v-else-if="row.priority === 'warning'"
                type="warning"
                effect="plain"
              >
                本日
              </el-tag>

              <el-tag v-else type="info" effect="plain">通常</el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="project_name" label="案件名" min-width="180" />

          <el-table-column prop="name" label="タスク名" min-width="220">
            <template #default="{ row }">
              <span class="task-name">{{ row.name }}</span>
            </template>
          </el-table-column>

          <el-table-column label="ステータス" width="130">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" effect="plain">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column label="進捗" width="150">
            <template #default="{ row }">
              <div class="progress-cell">
                <el-progress
                  :percentage="row.progress ?? 0"
                  :stroke-width="8"
                  :show-text="false"
                />
                <span>{{ row.progress ?? 0 }}%</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="開始日" width="110">
            <template #default="{ row }">
              {{ formatDate(row.start_date) }}
            </template>
          </el-table-column>

          <el-table-column label="期限" width="110">
            <template #default="{ row }">
              <span :class="{ overdue: row.priority === 'danger' }">
                {{ formatDate(row.due_date) }}
              </span>
            </template>
          </el-table-column>
        </el-table>

        <el-empty
          v-else
          description="対象タスクはありません"
          :image-size="80"
        />
      </el-card>
    </template>

    <template v-else-if="props.activePanel === 'projects'">
      <el-card shadow="never" class="task-card">
        <template #header>
          <div class="section-header">
            <div>
              <div class="section-title">案件一覧</div>
              <div class="section-subtitle">
                自分が担当しているタスクに紐づく案件を確認できます
              </div>
            </div>

            <el-button
              type="primary"
              plain
              round
              size="small"
              @click="emit('change-panel', 'tasks')"
            >
              ↺ タスク一覧に戻る
            </el-button>
          </div>
        </template>

        <ProjectListPanel embedded />
      </el-card>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { TaskDashboardItem } from "@/api/dashboard";
import ProjectListPanel from "@/components/projects/ProjectListPanel.vue";

type TaskMemberFilter =
  | "all"
  | "today_deadline"
  | "overdue"
  | "in_progress"
  | "in_review";

const props = defineProps<{
  summary: Record<string, number> | null;
  tasks: TaskDashboardItem[];
  loading: boolean;
  activePanel: "tasks" | "projects";
}>();

const emit = defineEmits<{
  (e: "move", projectId: number): void;
  (e: "change-panel", panel: "tasks" | "projects"): void;
}>();

const selectedFilter = ref<TaskMemberFilter>("all");

const showTasks = (filter: TaskMemberFilter) => {
  selectedFilter.value = filter;
  emit("change-panel", "tasks");
};

const filteredTasks = computed(() => {
  switch (selectedFilter.value) {
    case "today_deadline":
      return props.tasks.filter((task) => task.priority === "warning");
    case "overdue":
      return props.tasks.filter((task) => task.priority === "danger");
    case "in_progress":
      return props.tasks.filter((task) => task.status === "IN_PROGRESS");
    case "in_review":
      return props.tasks.filter((task) => task.status === "IN_REVIEW");
    case "all":
    default:
      return props.tasks;
  }
});

const tableTitle = computed(() => {
  const labels: Record<TaskMemberFilter, string> = {
    all: "自分の担当タスク",
    today_deadline: "今日期限タスク",
    overdue: "期限超過タスク",
    in_progress: "進行中タスク",
    in_review: "レビュー中タスク",
  };

  return `${labels[selectedFilter.value]}（${filteredTasks.value.length}件）`;
});

const handleRowClick = (row: TaskDashboardItem) => {
  if (!row.project_id) return;
  emit("move", row.project_id);
};

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    TODO: "未着手",
    IN_PROGRESS: "進行中",
    IN_REVIEW: "レビュー中",
    DONE: "完了",
  };

  return labels[status] ?? status;
};

const getStatusType = (status: string) => {
  const types: Record<string, "info" | "warning" | "success"> = {
    TODO: "info",
    IN_PROGRESS: "warning",
    IN_REVIEW: "warning",
    DONE: "success",
  };

  return types[status] ?? "info";
};

const formatDate = (value: string | null) => {
  if (!value) return "-";
  return value.replaceAll("-", "/");
};
</script>

<style scoped>
.task-member-dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.summary-cards {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.summary-card {
  flex: 0 0 190px;
  border-radius: 12px;
  cursor: pointer;
}

.summary-card.info {
  background: #f0f5ff;
  border-color: #adc6ff;
}

.summary-card.warning {
  background: #fff7e6;
  border-color: #ffd591;
}

.summary-card.danger {
  background: #fff1f0;
  border-color: #ffccc7;
}

.summary-card.success {
  background: #f6ffed;
  border-color: #b7eb8f;
}

.summary-card.review {
  background: #f4f4f5;
  border-color: #dcdfe6;
}

.card-title {
  font-size: 13px;
  color: #606266;
}

.card-value {
  margin-top: 12px;
  font-size: 32px;
  font-weight: 700;
}

.card-value span {
  margin-left: 4px;
  font-size: 13px;
}

.card-desc {
  margin-top: 8px;
  font-size: 11px;
  color: #909399;
}

.task-card {
  border-radius: 12px;
  border: 1px solid #dcdfe6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
}

.section-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.task-name {
  font-weight: 600;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-cell .el-progress {
  flex: 1;
}

.overdue {
  color: #f56c6c;
  font-weight: 700;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>

<template>
  <div class="approval-view">
    <!-- ページヘッダー -->
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
        <el-breadcrumb-item>承認・却下</el-breadcrumb-item>
      </el-breadcrumb>
      <h1 class="page-title">承認・却下</h1>
    </div>

    <!-- ■ 案件情報 -->
    <el-card shadow="never" class="mb-16" v-if="project">
      <template #header>
        <span>案件情報</span>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="案件名" :span="2">
          {{ project.name }}
        </el-descriptions-item>

        <el-descriptions-item label="担当部門">
          {{ project.department_id }}
        </el-descriptions-item>

        <el-descriptions-item label="申請者">
          {{ project.applicant_id }}
        </el-descriptions-item>

        <el-descriptions-item label="概算工数">
          {{ project.planned_months ?? "未設定" }} 人月
        </el-descriptions-item>

        <el-descriptions-item label="概算予算">
          {{ project.budget_amount }} 万円
        </el-descriptions-item>

        <el-descriptions-item label="開始予定日">
          {{ project.start_date ?? "未設定" }}
        </el-descriptions-item>

        <el-descriptions-item label="完了予定日">
          {{ project.end_date ?? "未設定" }}
        </el-descriptions-item>

        <el-descriptions-item label="ステータス" :span="2">
          <el-tag :type="PROJECT_STATUS_TAG_TYPE[project.status]">
            {{ PROJECT_STATUS_LABEL[project.status] }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div class="mt-16">
        <strong>目的・概要</strong>
        <p class="description">{{ project.description }}</p>
      </div>
    </el-card>

    <!-- ■ 承認・却下フォーム -->
    <el-card shadow="never" class="mb-16">
      <template #header>
        <span>承認・却下入力</span>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="コメント（承認時任意）" prop="comment">
          <el-input
            v-model="form.comment"
            type="textarea"
            :rows="3"
            placeholder="承認時のコメントを入力してください（任意）"
          />
        </el-form-item>

        <el-form-item label="却下理由（却下時必須）" prop="reject_reason">
          <el-input
            v-model="form.reject_reason"
            type="textarea"
            :rows="3"
            placeholder="却下する場合は理由を入力してください"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
    </el-card>

    <!-- ■ 操作ボタン -->
    <div class="actions">
      <el-button @click="goBack">戻る</el-button>
      <el-button
        type="success"
        :disabled="!canApprove"
        :loading="loading"
        @click="handleApprove"
      >
        承認
      </el-button>
      <el-button
        type="danger"
        :disabled="!canApprove"
        :loading="loading"
        @click="handleReject"
      >
        却下
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormRules } from "element-plus";
import { PROJECT_STATUS_LABEL, PROJECT_STATUS_TAG_TYPE } from "@/constants/project";
import { projectsAPI } from "@/api/projects";
import type { ProjectResponse } from "@/api/models/ProjectResponse";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const projectId = Number(route.params.projectId);
const project = ref<ProjectResponse | null>(null);
const loading = ref(false);
const actionDone = ref(false);

const form = ref({
  comment: "",
  reject_reason: "",
});

const rules: FormRules = {
  reject_reason: [
    {
      max: 500,
      message: "却下理由は500字以内で入力してください",
      trigger: "blur",
    },
  ],
};

const canApprove = computed(() => {
  if (actionDone.value) return false;
  if (authStore.isDeptManager) {
    return project.value?.status === "PENDING_DEPT";
  }
  if (authStore.isHqManager) {
    return project.value?.status === "PENDING_HQ";
  }
  return false;
});

onMounted(async () => {
  try {
    const response = await projectsAPI.getProject(projectId);
    project.value = response.data;
  } catch (error) {
    console.error("案件詳細の取得に失敗しました", error);
  }
});

const handleApprove = async () => {
  if (!canApprove.value) return;

  try {
    await ElMessageBox.confirm(
      "この案件を承認してよろしいですか？",
      "承認確認",
      {
        type: "success",
        confirmButtonText: "承認",
        cancelButtonText: "キャンセル",
      },
    );
  } catch {
    return;
  }

  loading.value = true;
  try {
    await projectsAPI.approveProject(projectId, { reject_reason: null });
    actionDone.value = true;
    ElMessage.success("承認しました");
    router.push("/projects");
  } catch {
    ElMessage.error("承認に失敗しました");
  } finally {
    loading.value = false;
  }
};

const handleReject = async () => {
  if (!canApprove.value) return;

  if (!form.value.reject_reason.trim()) {
    ElMessage.error("却下理由を入力してください");
    return;
  }

  try {
    await ElMessageBox.confirm(
      "この案件を却下してよろしいですか？",
      "却下確認",
      {
        type: "warning",
        confirmButtonText: "却下",
        cancelButtonText: "キャンセル",
      },
    );
  } catch {
    return;
  }

  loading.value = true;
  try {
    await projectsAPI.approveProject(projectId, {
      reject_reason: form.value.reject_reason,
    });
    actionDone.value = true;
    ElMessage.success("却下しました");
    router.push("/projects");
  } catch {
    ElMessage.error("却下に失敗しました");
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.approval-view {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.description {
  margin-top: 8px;
  color: #606266;
  line-height: 1.6;
}
</style>

<template>
  <div class="worklog-form-view">
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
          isEdit ? "工数実績編集" : "工数実績入力"
        }}</el-breadcrumb-item>
      </el-breadcrumb>
      <h1 class="page-title">{{ isEdit ? "工数実績編集" : "工数実績入力" }}</h1>
    </div>

    <el-card shadow="never">
      <template #header>
        <span>工数実績情報</span>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <!-- 対象月 -->
        <el-form-item label="対象月" prop="work_month">
          <el-date-picker
            v-model="form.work_month"
            type="month"
            :disabled="isEdit"
            placeholder="対象月を選択"
            format="YYYY年MM月"
            value-format="YYYY-MM"
            style="width: 100%"
          />
        </el-form-item>

        <!-- 実績工数 -->
        <el-form-item label="実績工数（人月）" prop="actual_months">
          <el-input-number
            v-model="form.actual_months"
            :min="0"
            :precision="1"
            :step="0.5"
            style="width: 100%"
            placeholder="例：1.5"
          />
          <div class="form-hint">
            その月に投入した工数を人月単位で入力してください
          </div>
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
import { budgetAPI } from "@/api/budget";
import type { WorklogCreate } from "@/api/models/WorklogCreate";
import { projectsAPI } from "@/api/projects";
import type { ProjectResponse } from "@/api/models/ProjectResponse";

const route = useRoute();
const router = useRouter();

const project = ref<ProjectResponse | null>(null);
const projectId = Number(route.params.projectId);
const worklogId = route.params.worklogId
  ? Number(route.params.worklogId)
  : undefined;
const isEdit = !!worklogId;

const formRef = ref<FormInstance>();
const loading = ref(false);

const form = ref<{
  work_month: string;
  actual_months: number | null;
}>({
  work_month: "",
  actual_months: null,
});

const rules: FormRules = {
  work_month: [
    { required: true, message: "対象月を選択してください", trigger: "change" },
    {
      validator: (_rule, value, callback) => {
        if (!value) {
          callback();
          return;
        }
        const today = new Date();
        const currentMonth = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}`;
        if (value > currentMonth) {
          callback(new Error("未来の月は選択できません"));
          return;
        }
        if (project.value?.start_date) {
          const projectStartMonth = project.value.start_date.substring(0, 7);
          if (value < projectStartMonth) {
            callback(
              new Error(
                `案件開始月（${projectStartMonth}）以降を選択してください`,
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
  actual_months: [
    { required: true, message: "実績工数を入力してください", trigger: "blur" },
    {
      validator: (_rule, value: number, callback) => {
        if (!isEdit && value <= 0) {
          callback(new Error("実績工数は0より大きい値を入力してください"));
        } else if (value < 0) {
          callback(new Error("実績工数は0以上の値を入力してください"));
        } else if (value > 20) {
          callback(new Error("実績工数は20人月以下で入力してください"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  loading.value = true;
  try {
    const data: WorklogCreate = {
      work_month: form.value.work_month,
      actual_months: String(form.value.actual_months),
    };
    if (isEdit) {
      await budgetAPI.updateWorklog(projectId, worklogId!, {
        actual_months: String(form.value.actual_months),
      });
      ElMessage.success("工数実績を更新しました");
    } else {
      await budgetAPI.createWorklog(projectId, data);
      ElMessage.success("工数実績を登録しました");
    }
    router.push(`/projects/${projectId}/budget`);
  } catch (error: any) {
    const status = error?.response?.status;
    const detail = error?.response?.data?.detail;
    if (status === 400 && detail) {
      ElMessage.error(detail);
    } else {
      ElMessage.error(isEdit ? "更新に失敗しました" : "登録に失敗しました");
    }
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
      const worklogsResponse = await budgetAPI.getWorklogs(projectId);
      const worklog = worklogsResponse.data.find((w) => w.id === worklogId);
      if (worklog) {
        form.value = {
          work_month: worklog.work_month,
          actual_months: Number(worklog.actual_months),
        };
      }
    }
  } catch (error) {
    console.error("データの取得に失敗しました", error);
  }
});
</script>

<style scoped>
.worklog-form-view {
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
}

.form-hint {
  font-size: 0.75rem;
  color: #909399;
  margin-top: 4px;
}
</style>

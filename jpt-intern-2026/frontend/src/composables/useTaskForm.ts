import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

import { useAuthStore } from "@/stores/auth";
import { TASK_STATUS_LABEL } from "@/constants/task";

import { projectsAPI } from "@/api/projects";
import { tasksAPI } from "@/api/tasks";

import type { ProjectResponse } from "@/api/models/ProjectResponse";
import { ProjectStatus } from "@/api/models/ProjectStatus";
import type { TaskCreate } from "@/api/models/TaskCreate";
import { TaskStatus } from "@/api/models/TaskStatus";
import type { UserResponse } from "@/api/models/UserResponse";

export const useTaskForm = () => {
  const route = useRoute();
  const router = useRouter();
  const authStore = useAuthStore();

  const projectId = Number(route.params.projectId);
  const taskId = route.params.taskId ? Number(route.params.taskId) : undefined;
  const isEdit = !!taskId;

  const formRef = ref<FormInstance>();
  const loading = ref(false);

  const project = ref<ProjectResponse | null>(null);
  const users = ref<UserResponse[]>([]);

  const form = ref<TaskCreate>({
    name: "",
    phase_name: "",
    assignee_id: undefined,
    status: TaskStatus.TODO,
    progress: 0,
    start_date: "",
    due_date: "",
    description: "",
  });

  const isEditableProjectStatus = computed(() =>
    project.value
      ? [ProjectStatus.APPROVED, ProjectStatus.IN_PROGRESS].includes(
          project.value.status,
        )
      : false,
  );

  const canManageTask = computed(() => {
    return authStore.role === "APPLICANT";
  });

  const canUpdateOwnTask = computed(() => {
    return (
      authStore.role === "TASK_MEMBER" &&
      isEdit &&
      isEditableProjectStatus.value
    );
  });

  const canEditMasterFields = computed(() => {
    return canManageTask.value;
  });

  const canEditProgressFields = computed(() => {
    return canManageTask.value || canUpdateOwnTask.value;
  });

  const canSubmitTask = computed(() => {
    if (!isEditableProjectStatus.value) {
      return false;
    }

    if (!isEdit) {
      return canManageTask.value;
    }

    return canManageTask.value || canUpdateOwnTask.value;
  });

  const taskStatusOptions = computed(() => {
    if (authStore.role === "TASK_MEMBER") {
      return {
        TODO: TASK_STATUS_LABEL.TODO,
        IN_PROGRESS: TASK_STATUS_LABEL.IN_PROGRESS,
      };
    }

    return TASK_STATUS_LABEL;
  });

  const progressMax = computed(() => {
    return authStore.role === "TASK_MEMBER" ? 99 : 100;
  });

  const rules: FormRules = {
    name: [
      {
        required: true,
        message: "タスク名は必須です",
        trigger: "blur",
      },
    ],
    phase_name: [
      {
        required: true,
        message: "工程名は必須です",
        trigger: "change",
      },
    ],
    assignee_id: [
      {
        required: true,
        message: "担当者は必須です",
        trigger: "change",
      },
    ],
    status: [
      {
        required: true,
        message: "ステータスは必須です",
        trigger: "change",
      },
    ],
    progress: [
      {
        required: true,
        message: "進捗率は必須です",
        trigger: "blur",
      },
    ],
    start_date: [
      {
        required: true,
        message: "開始日は必須です",
        trigger: "change",
      },
    ],
    due_date: [
      {
        required: true,
        message: "期限は必須です",
        trigger: "change",
      },
    ],
  };

  const fetchInitialData = async () => {
    try {
      const projectResponse = await projectsAPI.getProject(projectId);
      project.value = projectResponse.data;

      const deptId = project.value?.department_id;
      if (!deptId) {
        ElMessage.error("部門情報が取得できません");
        return;
      }

      if (isEdit) {
        const tasksResponse = await tasksAPI.getTasks(projectId);
        const task = tasksResponse.data.find((item) => item.id === taskId);

        if (!task) {
          ElMessage.error("タスクが見つかりません");
          await router.push(`/projects/${projectId}`);
          return;
        }

        form.value = {
          name: task.name,
          phase_name: task.phase_name ?? "",
          assignee_id: task.assignee_id ?? undefined,
          status: task.status,
          progress: task.progress,
          start_date: task.start_date ?? "",
          due_date: task.due_date ?? "",
          description: task.description ?? "",
        };
      }
    } catch (error) {
      console.error("データ取得失敗", error);
      ElMessage.error("データ取得に失敗しました");
    }
  };

  const handleSubmit = async () => {
    if (!formRef.value) {
      return;
    }

    if (!canSubmitTask.value) {
      ElMessage.error("このタスクを更新する権限がありません");
      return;
    }

    await formRef.value.validate();

    loading.value = true;

    try {
      if (isEdit) {
        await tasksAPI.updateTask(projectId, taskId!, form.value);
        ElMessage.success("更新しました");
      } else {
        await tasksAPI.createTask(projectId, form.value);
        ElMessage.success("登録しました");
      }

      await router.push(`/projects/${projectId}`);
    } catch {
      ElMessage.error("処理に失敗しました");
    } finally {
      loading.value = false;
    }
  };

  const handleDelete = async () => {
    if (!taskId || !canManageTask.value) {
      return;
    }

    try {
      await ElMessageBox.confirm("削除してよろしいですか？", "確認", {
        type: "warning",
      });
    } catch {
      return;
    }

    loading.value = true;

    try {
      await tasksAPI.deleteTask(projectId, taskId);
      ElMessage.success("削除しました");
      await router.push(`/projects/${projectId}`);
    } catch {
      ElMessage.error("削除に失敗しました");
    } finally {
      loading.value = false;
    }
  };

  const goBack = () => {
    router.back();
  };

  onMounted(fetchInitialData);

  watch(
    () => form.value.status,
    (val) => {
      if (!canManageTask.value) return;

      if (val === TaskStatus.DONE) {
        form.value.progress = 100;
      }
    },
  );

  watch(
    () => form.value.progress,
    (val) => {
      if (!canManageTask.value) return;

      if (val === 100) {
        form.value.status = TaskStatus.DONE;
      } else if (form.value.status === TaskStatus.DONE) {
        form.value.status = TaskStatus.IN_PROGRESS;
      }
    },
  );

  return {
    projectId,
    taskId,
    isEdit,

    formRef,
    loading,
    project,
    users,
    form,
    rules,

    canManageTask,
    canEditMasterFields,
    canEditProgressFields,
    canSubmitTask,

    taskStatusOptions,
    progressMax,

    handleSubmit,
    handleDelete,
    goBack,
  };
};

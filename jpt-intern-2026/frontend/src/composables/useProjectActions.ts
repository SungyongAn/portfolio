/**
 * useProjectActions.ts
 * 案件詳細画面のアクション定義・権限制御・ハンドラーを管理するcomposable
 */
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { projectsAPI } from "@/api/projects";
import type { ProjectResponse } from "@/api/models/ProjectResponse";

export function useProjectActions(
  projectId: number,
  project: ReturnType<typeof ref<ProjectResponse | null>>,
  onProjectUpdated: () => Promise<void>,
  onBeforeStart?: () => Promise<boolean>,
) {
  const router = useRouter();
  const authStore = useAuthStore();

  const actionLoading = ref(false);

  const canApprove = computed(
    () =>
      authStore.canApprove &&
      (project.value?.status === "PENDING_DEPT" ||
        project.value?.status === "PENDING_HQ"),
  );

  const canStart = computed(() => {
    const s = project.value?.status;
    if (!s) return false;
    return (
      (authStore.isApplicant ||
        authStore.isDeptManager ||
        authStore.isHqManager) &&
      s === "APPROVED"
    );
  });

  const canComplete = computed(
    () =>
      (authStore.isDeptManager || authStore.isHqManager) &&
      project.value?.status === "IN_PROGRESS",
  );

  const canEditTask = computed(() => {
    const s = project.value?.status;
    if (!s) return false;
    return authStore.isApplicant && (s === "APPROVED" || s === "IN_PROGRESS");
  });

  const canEditBudget = computed(() => {
    const s = project.value?.status;
    if (!s) return false;
    return authStore.isApplicant && (s === "APPROVED" || s === "IN_PROGRESS");
  });

  const goApprove = () => {
    router.push(`/projects/${projectId}/approval`);
  };

  const handleStart = async () => {
    if (actionLoading.value) return;

    const canProceed = onBeforeStart ? await onBeforeStart() : true;
    if (!canProceed) return;

    actionLoading.value = true;
    try {
      await projectsAPI.startProject(projectId);
      await onProjectUpdated();
    } catch (e) {
      console.error("着手に失敗しました", e);
    } finally {
      actionLoading.value = false;
    }
  };

  const handleComplete = async () => {
    if (actionLoading.value) return;
    actionLoading.value = true;
    try {
      await projectsAPI.completeProject(projectId);
      await onProjectUpdated();
    } catch (e) {
      console.error("完了に失敗しました", e);
    } finally {
      actionLoading.value = false;
    }
  };

  const goTaskNew = () => {
    router.push(`/projects/${projectId}/tasks/new`);
  };

  const goBudget = () => {
    router.push(`/projects/${projectId}/budget`);
  };

  const actions = computed(() => [
    {
      key: "approve",
      show: canApprove.value,
      label: "承認 / 却下",
      type: "success" as const,
      handler: goApprove,
    },
    {
      key: "start",
      show: canStart.value,
      label: "着手する",
      type: "primary" as const,
      handler: handleStart,
    },
    {
      key: "complete",
      show: canComplete.value,
      label: "完了にする",
      type: "success" as const,
      handler: handleComplete,
    },
    {
      key: "task",
      show: canEditTask.value,
      label: "タスク登録",
      type: "primary" as const,
      handler: goTaskNew,
    },
    {
      key: "budget",
      show: canEditBudget.value,
      label: "予算管理",
      type: "warning" as const,
      handler: goBudget,
    },
  ]);

  return {
    actionLoading,
    actions,
    canEditTask,
    canEditBudget,
    goTaskNew,
    goBudget,
  };
}

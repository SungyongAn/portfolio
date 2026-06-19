import type { ProjectStatus } from "@/api/models/ProjectStatus";

export const PROJECT_STATUS_LABEL: Record<ProjectStatus, string> = {
  DRAFT: "下書き",
  PENDING_DEPT: "部門承認待ち",
  PENDING_HQ: "本部承認待ち",
  APPROVED: "承認済み",
  IN_PROGRESS: "進行中",
  COMPLETED: "完了",
  REJECTED: "却下",
};

export const PROJECT_STATUS_TAG_TYPE: Record<
  ProjectStatus,
  "info" | "warning" | "success" | "danger"
> = {
  DRAFT: "info",
  PENDING_DEPT: "warning",
  PENDING_HQ: "warning",
  APPROVED: "success",
  IN_PROGRESS: "success",
  COMPLETED: "info",
  REJECTED: "danger",
};

export type TaskStatusTagType =
  | "success"
  | "warning"
  | "info"
  | "primary"
  | "danger";

const TASK_STATUS_LABELS: Record<string, string> = {
  TODO: "未着手",
  NOT_STARTED: "未着手",

  IN_PROGRESS: "進行中",

  IN_REVIEW: "レビュー中",
  REVIEW: "レビュー中",

  DONE: "完了",
  COMPLETED: "完了",
};

const TASK_STATUS_TAG_TYPES: Record<string, TaskStatusTagType> = {
  TODO: "info",
  NOT_STARTED: "info",

  IN_PROGRESS: "primary",

  IN_REVIEW: "warning",
  REVIEW: "warning",

  DONE: "success",
  COMPLETED: "success",
};

export const getTaskStatusLabel = (status: string): string => {
  return TASK_STATUS_LABELS[status] ?? status;
};

export const getTaskStatusTagType = (
  status: string,
): TaskStatusTagType | undefined => {
  return TASK_STATUS_TAG_TYPES[status];
};

export const getTaskStatusClass = (status: string): string => {
  return status.toLowerCase().replaceAll("_", "-");
};

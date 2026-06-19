export type NotificationLike = {
  title: string;
  message: string;
};

export type NotificationKind =
  | "approval"
  | "rejected"
  | "started"
  | "completed"
  | "review"
  | "default";

export type NotificationTagType =
  | "success"
  | "warning"
  | "info"
  | "primary"
  | "danger";

export type NotificationToastType = "success" | "warning" | "info" | "error";

export type NotificationMeta = {
  kind: NotificationKind;
  label: string;
  tagType: NotificationTagType;
  toastType: NotificationToastType;
  className: string;
};

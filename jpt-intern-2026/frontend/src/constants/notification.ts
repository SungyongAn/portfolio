import type { NotificationLike, NotificationMeta } from "@/types/notification";

export const getNotificationMeta = (
  notification: NotificationLike,
): NotificationMeta => {
  const text = `${notification.title} ${notification.message}`;

  if (text.includes("却下") || text.includes("差し戻し")) {
    return {
      kind: "rejected",
      label: "要対応",
      tagType: "danger",
      toastType: "error",
      className: "notification-rejected",
    };
  }

  if (text.includes("承認依頼") || text.includes("承認待ち")) {
    return {
      kind: "approval",
      label: "承認依頼",
      tagType: "warning",
      toastType: "warning",
      className: "notification-approval",
    };
  }

  if (text.includes("着手") || text.includes("開始")) {
    return {
      kind: "started",
      label: "着手",
      tagType: "primary",
      toastType: "info",
      className: "notification-started",
    };
  }

  if (text.includes("完了")) {
    return {
      kind: "completed",
      label: "完了",
      tagType: "success",
      toastType: "success",
      className: "notification-completed",
    };
  }

  if (text.includes("レビュー")) {
    return {
      kind: "review",
      label: "レビュー",
      tagType: "info",
      toastType: "info",
      className: "notification-review",
    };
  }

  return {
    kind: "default",
    label: "通知",
    tagType: "info",
    toastType: "info",
    className: "notification-default",
  };
};

import { ref } from "vue";
import { ElMessage } from "element-plus";

import { notificationsAPI } from "@/api/notifications";
import { unreadCount } from "@/services/notificationService";

import type { NotificationResponse } from "@/api/models/NotificationResponse";

export function useNotifications() {
  const loading = ref(false);
  const notifications = ref<NotificationResponse[]>([]);

  const fetchNotifications = async () => {
    loading.value = true;

    try {
      const response = await notificationsAPI.getNotifications();

      notifications.value = response.data.items;

      unreadCount.value = notifications.value.filter(
        (notification) => !notification.is_read,
      ).length;
    } catch {
      ElMessage.error("通知の取得に失敗しました");
    } finally {
      loading.value = false;
    }
  };

  const markAsRead = async (notificationId: number) => {
    const target = notifications.value.find(
      (notification) => notification.id === notificationId,
    );

    if (!target || target.is_read) {
      return;
    }

    try {
      await notificationsAPI.markAsRead(notificationId);

      notifications.value = notifications.value.map((notification) =>
        notification.id === notificationId
          ? { ...notification, is_read: true }
          : notification,
      );

      if (unreadCount.value > 0) {
        unreadCount.value -= 1;
      }
    } catch {
      ElMessage.error("既読処理に失敗しました");
    }
  };

  const markAllAsRead = async () => {
    const hasUnread = notifications.value.some(
      (notification) => !notification.is_read,
    );

    if (!hasUnread) {
      return;
    }

    try {
      await notificationsAPI.markAllAsRead();

      notifications.value = notifications.value.map((notification) => ({
        ...notification,
        is_read: true,
      }));

      unreadCount.value = 0;

      ElMessage.success("すべて既読にしました");
    } catch {
      ElMessage.error("処理に失敗しました");
    }
  };

  return {
    loading,
    notifications,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
  };
}
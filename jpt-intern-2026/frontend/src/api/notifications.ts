import apiClient from "./client";
import type { NotificationResponse } from "@/api/models/NotificationResponse";
import type { NotificationListResponse } from "@/api/models/NotificationListResponse";

export const notificationsAPI = {
  getNotifications(page: number = 1, limit: number = 10) {
    return apiClient.get<NotificationListResponse>(
      `/api/notifications?page=${page}&limit=${limit}`,
    );
  },

  markAsRead(notificationId: number) {
    return apiClient.put<NotificationResponse>(
      `/api/notifications/${notificationId}/read`,
    );
  },

  markAllAsRead() {
    return apiClient.put("/api/notifications/read-all");
  },
};

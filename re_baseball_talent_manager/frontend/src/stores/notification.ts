import { defineStore } from "pinia";
import {
  connectNotifications,
  disconnectNotifications,
  NotificationMessage,
} from "@/services/notificationService";


// ==============================
// 型定義
// ==============================

// 通知1件の型
export type NotificationItem = NotificationMessage & {
  timestamp: Date;
};

// state全体
type NotificationState = {
  notifications: NotificationItem[];
  isConnected: boolean;
};

// ==============================
// Store
// ==============================
export const useNotificationStore = defineStore("notification", {
  state: (): NotificationState => ({
    notifications: [],
    isConnected: false,
  }),

  actions: {
    connect(token: string): void {
      this.isConnected = true;

      connectNotifications(token, (data: NotificationMessage) => {
        this.notifications.unshift({
          type: data.type,
          message: data.message,
          timestamp: new Date(),
        });

        console.log("通知受信:", data);
      });
    },

    disconnect(): void {
      this.isConnected = false;
      disconnectNotifications();
      this.notifications = [];
    },

    clearNotifications(): void {
      this.notifications = [];
    },
  },
});

import { defineStore } from "pinia";
import {
  connectNotifications,
  disconnectNotifications,
} from "@/services/notificationService";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    // { type, message, timestamp } の配列
    notifications: [],
    isConnected: false,
  }),

  actions: {
    connect(token) {
      this.isConnected = true;
      connectNotifications(token, (data) => {
        // 受信した通知を先頭に追加
        this.notifications.unshift({
          type: data.type,
          message: data.message,
          timestamp: new Date(),
        });

        console.log("通知受信:", data);
      });
    },

    disconnect() {
      this.isConnected = false;
      disconnectNotifications();
      this.notifications = [];
    },

    clearNotifications() {
      this.notifications = [];
    },
  },
});

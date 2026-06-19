<template>
  <aside class="app-sidebar">
    <div class="sidebar-header">
      <router-link to="/" class="brand">
        <el-icon :size="22"><Management /></el-icon>
        <span>開発管理システム</span>
      </router-link>
    </div>

    <div class="sidebar-notification">
      <el-popover
        placement="right-end"
        width="360"
        trigger="click"
        @show="fetchNotifications"
      >
        <template #reference>
          <button class="notification-button">
            <el-badge :value="unreadCount" :hidden="unreadCount === 0">
              <el-icon :size="20"><Bell /></el-icon>
            </el-badge>
            <span>お知らせ</span>
          </button>
        </template>

        <div class="notification-popover">
          <div class="notification-popover-header">
            <span>お知らせ</span>

            <el-button
              size="small"
              text
              :disabled="unreadCount === 0"
              @click="markAllAsRead"
            >
              すべて既読
            </el-button>
          </div>

          <NotificationList
            :notifications="notifications"
            @select="openNotificationDetail"
          />
        </div>
      </el-popover>
    </div>

    <el-menu
      class="sidebar-menu"
      :default-active="activeMenu"
      background-color="transparent"
      text-color="#cbd5e1"
      active-text-color="#ffffff"
      @select="handleMenuSelect"
    >
      <el-menu-item v-for="item in menuItems" :key="item.to" :index="item.to">
        <el-icon>
          <component :is="item.icon" />
        </el-icon>
        <span>{{ item.label }}</span>
      </el-menu-item>
    </el-menu>

    <div class="sidebar-footer">
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="36" :icon="UserFilled" />

          <div class="user-text">
            <div class="user-name">
              {{ authStore.userName }}
            </div>

            <div class="user-role">
              {{ authStore.displayRole }}
            </div>
          </div>

          <el-icon><ArrowDown /></el-icon>
        </div>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="logout" :icon="SwitchButton">
              ログアウト
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <NotificationDetailDialog
      :visible="notificationDetailVisible"
      :notification="selectedNotification"
      width="520px"
      @close="notificationDetailVisible = false"
      @mark-as-read="handleMarkAsRead"
    />
  </aside>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import {
  Management,
  Bell,
  UserFilled,
  ArrowDown,
  SwitchButton,
} from "@element-plus/icons-vue";

import { useAuthStore } from "@/stores/auth";
import { useNotifications } from "@/composables/useNotifications";
import { unreadCount } from "@/services/notificationService";
import { menuMap, type MenuItem } from "@/constants/navigation";

import NotificationList from "@/components/notifications/NotificationList.vue";
import NotificationDetailDialog from "@/components/notifications/NotificationDetailDialog.vue";

import type { NotificationResponse } from "@/api/models/NotificationResponse";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const { notifications, fetchNotifications, markAsRead, markAllAsRead } =
  useNotifications();

const notificationDetailVisible = ref(false);
const selectedNotification = ref<NotificationResponse | null>(null);

const activeMenu = computed(() => {
  if (route.query.action === "create-project") {
    return "/?action=create-project";
  }

  if (route.query.view === "projects") {
    return "/?view=projects";
  }

  if (route.path.startsWith("/projects")) {
    return "/?view=projects";
  }

  return route.path;
});

const menuItems = computed<MenuItem[]>(() => {
  if (!authStore.role) return [];
  return menuMap[authStore.role] ?? [];
});

const openNotificationDetail = (notification: NotificationResponse) => {
  selectedNotification.value = notification;
  notificationDetailVisible.value = true;
};

const handleMarkAsRead = async (notificationId: number) => {
  await markAsRead(notificationId);

  if (selectedNotification.value?.id === notificationId) {
    selectedNotification.value = {
      ...selectedNotification.value,
      is_read: true,
    };
  }
};

const handleCommand = async (command: string) => {
  if (command === "logout") {
    await authStore.logout();
  }
};

const handleMenuSelect = async (index: string) => {
  if (index === "/?action=create-project") {
    await router.push({
      path: "/",
      query: {
        ...route.query,
        action: "create-project",
      },
    });
    return;
  }

  if (index === "/?view=projects" || index.startsWith("/projects")) {
    await router.push({
      path: "/",
      query: { view: "projects" },
    });
    return;
  }

  await router.push(index);
};
</script>

<style scoped>
.app-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;

  width: 240px;
  min-width: 240px;
  height: 100vh;

  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  color: #ffffff;

  display: flex;
  flex-direction: column;

  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ffffff;
  text-decoration: none;
  font-weight: 700;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.notification-button:hover {
  background: rgba(255, 255, 255, 0.14);
}

.notification-popover {
  max-height: 520px;
  overflow-y: auto;
}

.notification-popover-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  font-weight: 700;
}

.user-info {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #ffffff;
  padding: 8px;
  border-radius: 10px;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.08);
}

.user-text {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

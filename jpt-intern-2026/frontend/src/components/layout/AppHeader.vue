<template>
  <el-header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="brand">
        <el-icon :size="20"><Management /></el-icon>
        <span>開発管理システム</span>
      </router-link>

      <div class="header-right">
        <el-badge :value="unreadCount" :hidden="unreadCount === 0">
          <el-button
            :icon="Bell"
            circle
            text
            style="color: white"
            @click="openNotificationDrawer"
          />
        </el-badge>

        <el-dropdown @command="handleCommand">
          <div class="user-info">
            <el-avatar :size="32" :icon="UserFilled" />
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

        <el-button
          :icon="menuOpen ? Close : Expand"
          circle
          text
          style="color: white"
          @click="menuOpen = !menuOpen"
        />
      </div>
    </div>

    <el-drawer
      v-model="notificationDrawerVisible"
      title="お知らせ"
      direction="rtl"
      size="90%"
    >
      <NotificationList
        :notifications="notifications"
        @select="openNotificationDetail"
      />
    </el-drawer>

    <NotificationDetailDialog
      :visible="notificationDetailVisible"
      :notification="selectedNotification"
      width="90%"
      @close="notificationDetailVisible = false"
      @mark-as-read="handleMarkAsRead"
    />

    <el-drawer
      v-model="menuOpen"
      direction="ltr"
      size="70%"
      :with-header="false"
    >
      <div class="mobile-menu">
        <div class="mobile-menu-user">
          <el-avatar :size="40" :icon="UserFilled" />

          <div>
            <div class="mobile-user-name">
              {{ authStore.userName }}
            </div>

            <div class="mobile-user-role">
              {{ authStore.displayRole }}
            </div>
          </div>
        </div>

        <el-divider />

        <el-menu @select="handleMenuSelect">
          <el-menu-item
            v-for="item in menuItems"
            :key="item.to"
            :index="item.to"
          >
            <el-icon>
              <component :is="item.icon" />
            </el-icon>

            {{ item.label }}
          </el-menu-item>
        </el-menu>
      </div>
    </el-drawer>
  </el-header>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { ElNotification } from "element-plus";

import {
  Management,
  Bell,
  UserFilled,
  ArrowDown,
  SwitchButton,
  Expand,
  Close,
} from "@element-plus/icons-vue";

import { useAuthStore } from "@/stores/auth";
import { useNotifications } from "@/composables/useNotifications";
import {
  unreadCount,
  latestNotification,
} from "@/services/notificationService";
import { menuMap, type MenuItem } from "@/constants/navigation";
import { getNotificationMeta } from "@/constants/notification";

import NotificationList from "@/components/notifications/NotificationList.vue";
import NotificationDetailDialog from "@/components/notifications/NotificationDetailDialog.vue";

import type { NotificationResponse } from "@/api/models/NotificationResponse";

const authStore = useAuthStore();
const router = useRouter();

const { notifications, fetchNotifications, markAsRead } = useNotifications();

const menuOpen = ref(false);
const notificationDrawerVisible = ref(false);
const notificationDetailVisible = ref(false);
const selectedNotification = ref<NotificationResponse | null>(null);

watch(latestNotification, (notification) => {
  if (!notification) return;

  const meta = getNotificationMeta(notification);

  ElNotification({
    title: notification.title,
    message: notification.message,
    type: meta.toastType,
    duration: 4000,
    position: "bottom-right",
  });

  void fetchNotifications();
});

const openNotificationDrawer = async () => {
  notificationDrawerVisible.value = true;
  await fetchNotifications();
};

const openNotificationDetail = (notification: NotificationResponse ) => {
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

const menuItems = computed<MenuItem[]>(() => {
  if (!authStore.role) return [];
  return menuMap[authStore.role] ?? [];
});

const handleCommand = async (command: string) => {
  if (command === "logout") {
    await authStore.logout();
  }
};

const handleMenuSelect = async (index: string) => {
  menuOpen.value = false;

  if (index === "/projects") {
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
.app-header {
  background-color: #409eff;
  padding: 0;
  height: 56px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  text-decoration: none;
  font-weight: 700;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.user-info {
  display: flex;
  align-items: center;
  color: white;
  cursor: pointer;
}

.mobile-menu {
  padding: 16px;
}

.mobile-menu-user {
  display: flex;
  gap: 12px;
}

.mobile-user-name {
  font-weight: 700;
}

.mobile-user-role {
  font-size: 12px;
  color: #909399;
}
</style>
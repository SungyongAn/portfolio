<template>
  <div id="app">
    <template v-if="showNavigation">
      <div class="app-layout">
        <!-- PC -->
        <AppSidebar v-if="!isMobile" />

        <div class="app-content">
          <!-- Mobile -->
          <AppHeader v-if="isMobile" />

          <main :class="{ 'with-header': isMobile }">
            <router-view :key="route.fullPath" />
          </main>
        </div>
      </div>
    </template>

    <!-- login / 404 -->
    <template v-else>
      <router-view :key="route.fullPath" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useWindowSize } from "@vueuse/core";

import AppHeader from "@/components/layout/AppHeader.vue";
import AppSidebar from "@/components/layout/AppSidebar.vue";

import { useAuthStore } from "@/stores/auth";
import {
  startNotificationWs,
  stopNotificationWs,
} from "@/services/notificationService";
import { notificationsAPI } from "@/api/notifications";

const route = useRoute();
const authStore = useAuthStore();

const { width } = useWindowSize();
const isMobile = computed(() => width.value < 768);

const showNavigation = computed(() => {
  const hiddenRoutes = ["/login", "/404"];
  return !hiddenRoutes.includes(route.path);
});

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await initNotificationWs();
  }
});

watch(
  () => authStore.isAuthenticated,
  async (authenticated) => {
    if (authenticated) {
      await initNotificationWs();
    } else {
      stopNotificationWs();
    }
  },
);

async function initNotificationWs() {
  const token = authStore.accessToken;

  if (!token) {
    return;
  }

  try {
    const response = await notificationsAPI.getNotifications();

    const initialUnread = response.data.items.filter(
      (notification: { is_read: boolean }) => !notification.is_read,
    ).length;

    startNotificationWs(token, initialUnread);
  } catch {
    startNotificationWs(token, 0);
  }
}
</script>

<style>
#app {
  min-height: 100vh;
}

.app-layout {
  display: flex;
  min-height: 100vh;
}

.app-content {
  flex: 1;
  min-width: 0;
  background: #f5f7fa;
}

main {
  min-height: 100vh;
}

main.with-header {
  min-height: calc(100vh - 56px);
}

@media (min-width: 768px) {
  .app-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
}

@media (max-width: 767px) {
  .app-layout {
    display: block;
  }
}
</style>

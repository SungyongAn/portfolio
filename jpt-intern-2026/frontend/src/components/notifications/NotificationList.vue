<template>
  <div class="notification-list">
    <div v-if="notifications.length === 0" class="notification-empty">
      お知らせはありません
    </div>

    <NotificationItem
      v-for="notification in notifications"
      v-else
      :key="notification.id"
      :notification="notification"
      @select="emit('select', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import NotificationItem from "@/components/notifications/NotificationItem.vue";
import type { NotificationResponse } from "@/api/models/NotificationResponse";

defineProps<{
  notifications: NotificationResponse[];
}>();

const emit = defineEmits<{
  (e: "select", notification: NotificationResponse): void;
}>();
</script>

<style scoped>
.notification-list {
  width: 100%;
}

.notification-empty {
  padding: 24px 0;
  text-align: center;
  color: #909399;
}
</style>

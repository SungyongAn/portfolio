<template>
  <div
    class="notification-item"
    :class="[{ unread: !notification.is_read }, meta.className]"
    @click="emit('select', notification)"
  >
    <div class="notification-title-row">
      <el-tag size="small" :type="meta.tagType" effect="light">
        {{ meta.label }}
      </el-tag>

      <span class="notification-title">
        {{ notification.title }}
      </span>
    </div>

    <div class="notification-message">
      {{ notification.message }}
    </div>

    <div class="notification-date">
      {{ formatDate(notification.created_at) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { NotificationResponse } from "@/api/models/NotificationResponse";
import { getNotificationMeta } from "@/constants/notification";

const props = defineProps<{
  notification: NotificationResponse;
}>();

const emit = defineEmits<{
  (e: "select", notification: NotificationResponse): void;
}>();

const meta = computed(() => getNotificationMeta(props.notification));

const formatDate = (value?: string) => {
  if (!value) return "";

  return new Date(value).toLocaleString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<style scoped>
.notification-item {
  padding: 12px 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
  border-left: 4px solid transparent;
  border-radius: 6px;
  cursor: pointer;
}

.notification-item:hover {
  background: #f5f7fa;
}

.notification-item.unread {
  background: #ecf5ff;
}

.notification-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.notification-title {
  font-size: 14px;
  font-weight: 700;
}

.notification-message {
  margin-top: 4px;
  font-size: 13px;
  line-height: 1.5;

  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;

  overflow: hidden;
}

.notification-date {
  margin-top: 4px;
  font-size: 11px;
  color: #909399;
}

.notification-approval {
  border-left-color: #e6a23c;
}

.notification-rejected {
  border-left-color: #f56c6c;
}

.notification-started {
  border-left-color: #409eff;
}

.notification-completed {
  border-left-color: #67c23a;
}

.notification-review {
  border-left-color: #8e44ad;
}

.notification-default {
  border-left-color: #909399;
}
</style>

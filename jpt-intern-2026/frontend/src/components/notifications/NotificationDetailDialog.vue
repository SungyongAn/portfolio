<template>
  <el-dialog
    :model-value="visible"
    title="お知らせ詳細"
    :width="width"
    @close="emit('close')"
  >
    <div v-if="notification" class="notification-detail">
      <div class="detail-meta">
        <el-tag size="small" :type="meta.tagType" effect="light">
          {{ meta.label }}
        </el-tag>
      </div>

      <div class="detail-title">
        {{ notification.title }}
      </div>

      <div class="detail-date">
        {{ formatDate(notification.created_at) }}
      </div>

      <div class="detail-message">
        {{ notification.message }}
      </div>
    </div>

    <template #footer>
      <el-button
        v-if="notification && !notification.is_read"
        type="primary"
        @click="emit('mark-as-read', notification.id)"
      >
        既読にする
      </el-button>

      <el-button @click="emit('close')"> 閉じる </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { NotificationResponse } from "@/api/models/NotificationResponse";
import { getNotificationMeta } from "@/constants/notification";

const props = withDefaults(
  defineProps<{
    visible: boolean;
    notification: NotificationResponse | null;
    width?: string;
  }>(),
  {
    width: "520px",
  },
);

const emit = defineEmits<{
  (e: "close"): void;
  (e: "mark-as-read", notificationId: number): void;
}>();

const meta = computed(() => {
  if (!props.notification) {
    return getNotificationMeta({
      title: "",
      message: "",
    });
  }

  return getNotificationMeta(props.notification);
});

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
.notification-detail {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-meta {
  margin-bottom: 4px;
}

.detail-title {
  font-size: 16px;
  font-weight: 700;
}

.detail-date {
  font-size: 12px;
  color: #909399;
}

.detail-message {
  white-space: pre-wrap;
  line-height: 1.7;
  max-height: 50vh;
  overflow-y: auto;
}
</style>

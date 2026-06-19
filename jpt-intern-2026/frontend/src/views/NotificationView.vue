<template>
  <div class="notification-view">
    <div class="page-header">
      <div class="page-header-left">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }"
            >ダッシュボード</el-breadcrumb-item
          >
          <el-breadcrumb-item>通知一覧</el-breadcrumb-item>
        </el-breadcrumb>
        <h1 class="page-title">通知一覧</h1>
      </div>
      <el-button :disabled="unreadCount === 0" @click="handleReadAll">
        すべて既読にする
      </el-button>
    </div>

    <el-card shadow="never">
      <el-table :data="notifications" stripe v-loading="loading">
        <el-table-column label="状態" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_read ? 'info' : 'primary'" size="small">
              {{ row.is_read ? "既読" : "未読" }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="通知内容" min-width="300">
          <template #default="{ row }">
            <div>
              <strong>{{ row.title }}</strong>
            </div>
            <div class="notification-message">{{ row.message }}</div>
          </template>
        </el-table-column>

        <el-table-column label="日時" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="!row.is_read"
              size="small"
              text
              type="primary"
              @click="handleRead(row.id)"
            >
              既読にする
            </el-button>
          </template>
        </el-table-column>

        <template #empty>
          <el-empty description="通知はありません" />
        </template>
      </el-table>
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { notificationsAPI } from "@/api/notifications";
import type { NotificationResponse } from "@/api/models/NotificationResponse";

const loading = ref(false);
const notifications = ref<NotificationResponse[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);

const unreadCount = computed(
  () => notifications.value.filter((n) => !n.is_read).length,
);

const formatDateTime = (dateStr: string) => {
  return dateStr.replace("T", " ").substring(0, 16);
};

const fetchNotifications = async () => {
  loading.value = true;
  try {
    const response = await notificationsAPI.getNotifications(
      currentPage.value,
      pageSize.value,
    );
    notifications.value = response.data.items;
    total.value = response.data.total;
  } catch (error) {
    console.error("通知の取得に失敗しました", error);
  } finally {
    loading.value = false;
  }
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchNotifications();
};

const handleRead = async (notificationId: number) => {
  try {
    await notificationsAPI.markAsRead(notificationId);
    const target = notifications.value.find((n) => n.id === notificationId);
    if (target) {
      target.is_read = true;
    }
    ElMessage.success("既読にしました");
  } catch {
    ElMessage.error("処理に失敗しました");
  }
};

const handleReadAll = async () => {
  try {
    await notificationsAPI.markAllAsRead();
    await fetchNotifications(); // 再取得に変更
    ElMessage.success("すべて既読にしました");
  } catch {
    ElMessage.error("処理に失敗しました");
  }
};

onMounted(() => {
  fetchNotifications();
});
</script>

<style scoped>
.notification-view {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}
</style>

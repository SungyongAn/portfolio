<template>
  <div class="container mt-4">
    <!-- ヘッダー -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <button class="btn btn-outline-secondary" @click="backToMenu">
        <i class="fas fa-arrow-left me-2"></i>戻る
      </button>
      <h3 class="m-0 text-danger">
        <i class="fas fa-heart-pulse me-2"></i>体調不良生徒のお知らせ
      </h3>
      <button
        class="btn btn-outline-primary"
        @click="fetchNotifications"
        :disabled="isLoading"
      >
        <i class="fas fa-sync-alt me-2" :class="{ 'fa-spin': isLoading }"></i
        >更新
      </button>
    </div>

    <!-- 統計情報 -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title text-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>対象人数
            </h5>
            <h2 class="mb-0">{{ criticalCount }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title text-info">
              <i class="fas fa-clock me-2"></i>最終確認
            </h5>
            <p class="mb-0">{{ formatTime(lastCheckTime) }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title text-success">
              <i class="fas fa-calendar-day me-2"></i>対象日
            </h5>
            <p class="mb-0">{{ new Date().toLocaleDateString("ja-JP") }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- エラーメッセージ -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible">
      <i class="fas fa-exclamation-circle me-2"></i>{{ errorMessage }}
      <button
        type="button"
        class="btn-close"
        @click="errorMessage = ''"
      ></button>
    </div>

    <!-- 通知リスト -->
    <div v-if="notifications.length > 0" class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header bg-danger text-white">
            <i class="fas fa-list me-2"></i>体調不良の生徒一覧
          </div>
          <div class="list-group list-group-flush">
            <div
              v-for="entry in sortedNotifications"
              :key="entry.renrakucho_id"
              class="list-group-item list-group-item-action"
              @click="viewEntryDetail(entry)"
              style="cursor: pointer"
            >
              <div class="d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                  <h6 class="mb-1">
                    <span class="badge bg-primary me-2"
                      >{{ entry.grade }}年{{ entry.class_name }}組</span
                    >
                    {{ entry.student_name }}
                  </h6>
                  <div class="d-flex gap-3 mt-2">
                    <span>
                      <i class="fas fa-heartbeat me-1"></i>体調:
                      <span
                        :class="
                          'badge ' +
                          getStatusBadgeClass(entry.physical_condition)
                        "
                      >
                        {{ entry.physical_condition }} -
                        {{ getStatusText(entry.physical_condition) }}
                      </span>
                    </span>
                    <span>
                      <i class="fas fa-brain me-1"></i>メンタル:
                      <span
                        :class="
                          'badge ' + getStatusBadgeClass(entry.mental_state)
                        "
                      >
                        {{ entry.mental_state }} -
                        {{ getStatusText(entry.mental_state) }}
                      </span>
                    </span>
                  </div>
                </div>
                <div><i class="fas fa-chevron-right"></i></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 通知なし -->
    <div v-else class="alert alert-success text-center py-5">
      <i class="fas fa-check-circle fa-3x mb-3"></i>
      <h5>本日は対象の連絡帳はありません</h5>
      <p class="text-muted mb-0">体調またはメンタルが2以下の生徒はいません</p>
    </div>

    <!-- 詳細モーダル -->
    <div
      v-if="selectedEntry"
      class="modal d-block"
      style="background: rgba(0, 0, 0, 0.5)"
      @click.self="closeDetail"
    >
      <div
        class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable"
      >
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="fas fa-book me-2"></i>連絡帳詳細 -
              {{ selectedEntry.student_name }}
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="closeDetail"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              <strong>学年・組:</strong> {{ selectedEntry.grade }}年{{
                selectedEntry.class_name
              }}組
            </p>
            <p><strong>氏名:</strong> {{ selectedEntry.student_name }}</p>
            <div class="row">
              <div class="col-6">
                <strong>体調:</strong>
                <span
                  :class="
                    'badge ' +
                    getStatusBadgeClass(selectedEntry.physical_condition)
                  "
                >
                  {{ selectedEntry.physical_condition }} -
                  {{ getStatusText(selectedEntry.physical_condition) }}
                </span>
              </div>
              <div class="col-6">
                <strong>メンタル:</strong>
                <span
                  :class="
                    'badge ' + getStatusBadgeClass(selectedEntry.mental_state)
                  "
                >
                  {{ selectedEntry.mental_state }} -
                  {{ getStatusText(selectedEntry.mental_state) }}
                </span>
              </div>
            </div>
            <div v-if="selectedEntry.physical_mental_notes" class="mt-3">
              <strong>体調・メンタルについて:</strong>
              <p class="bg-light p-2 rounded">
                {{ selectedEntry.physical_mental_notes }}
              </p>
            </div>
            <div v-if="selectedEntry.daily_reflection" class="mt-3">
              <strong>前日の振り返り:</strong>
              <pre class="bg-light p-2 rounded" style="white-space: pre-wrap">{{
                selectedEntry.daily_reflection
              }}</pre>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeDetail"
            >
              <i class="fas fa-times me-2"></i>閉じる
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SchoolNurseDashboard",
  props: ["currentUser"],
  emits: ["back"],
  data() {
    return {
      notifications: [],
      errorMessage: "",
      selectedEntry: null,
      ws: null,
      isLoading: false,
      lastCheckTime: new Date().toISOString(),
    };
  },
  computed: {
    criticalCount() {
      return this.notifications.filter(
        (n) => n.physical_condition <= 2 || n.mental_state <= 2
      ).length;
    },
    sortedNotifications() {
      return [...this.notifications].sort((a, b) => {
        const scoreA = Math.min(a.physical_condition, a.mental_state);
        const scoreB = Math.min(b.physical_condition, b.mental_state);
        return scoreA - scoreB;
      });
    },
  },
  methods: {
    async fetchNotifications() {
      this.isLoading = true;
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/renrakucho-management/critical-entries"
        );
        if (res.data.success) {
          this.notifications = res.data.data;
          this.lastCheckTime = new Date().toISOString();
        } else {
          this.errorMessage = res.data.message || "通知取得失敗";
        }
      } catch (err) {
        console.error(err);
        this.errorMessage = "通知取得中にエラーが発生しました";
      } finally {
        this.isLoading = false;
      }
    },
    connectWebSocket() {
      if (!this.currentUser || !this.currentUser.id) return;

      const wsUrl = `ws://127.0.0.1:8000/notifications/ws/nurse/${this.currentUser.id}`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => console.log("✅ WebSocket 接続確立 (nurse)");

      this.ws.onmessage = (event) => {
        const entry = JSON.parse(event.data);
        if (!entry.student_name || !entry.grade || !entry.class_name) {
          console.warn("⚠️ 無効なWebSocketデータを受信しました:", entry);
          return;
        }
        this.notifications.push(entry);
        this.lastCheckTime = new Date().toISOString();
        this.playNotificationSound();
      };

      this.ws.onclose = (event) => {
        console.log("WebSocket 接続切断");
        if (event.code === 1000) return;
        console.log("5秒後に再接続");
        setTimeout(() => this.connectWebSocket(), 5000);
      };

      this.ws.onerror = (err) => console.error("WebSocket エラー:", err);
    },
    disconnectWebSocket() {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(
          JSON.stringify({
            type: "nurse_disconnect",
            user_id: this.currentUser.id,
          })
        );
        this.ws.close(1000, "Nurse dashboard closed");
        this.ws = null;
        console.log("✅ WebSocket disconnected (nurse dashboard)");
      }
    },
    playNotificationSound() {
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("新しい対象連絡帳", {
          body: "体調またはメンタルが低い生徒がいます",
          icon: "/icon.png",
        });
      }
    },
    requestNotificationPermission() {
      if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission();
      }
    },
    viewEntryDetail(entry) {
      this.selectedEntry = entry;
    },
    closeDetail() {
      this.selectedEntry = null;
    },
    getStatusBadgeClass(value) {
      if (value <= 1) return "bg-danger";
      if (value === 2) return "bg-warning";
      return "bg-secondary";
    },
    getStatusText(value) {
      if (value === 1) return "非常に悪い";
      if (value === 2) return "悪い";
      if (value === 3) return "普通";
      if (value === 4) return "良い";
      if (value === 5) return "非常に良い";
      return "不明";
    },
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString("ja-JP", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    backToMenu() {
      this.$emit("back");
    },
  },
  mounted() {
    this.fetchNotifications();
    this.connectWebSocket();
    this.requestNotificationPermission();
    window.addEventListener("beforeunload", this.disconnectWebSocket);
  },
  beforeUnmount() {
    this.disconnectWebSocket();
    window.removeEventListener("beforeunload", this.disconnectWebSocket);
  },
};
</script>

<style scoped>
.modal {
  z-index: 1050;
}
</style>

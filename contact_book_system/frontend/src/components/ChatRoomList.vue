<template>
  <div class="container mt-4">
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div v-if="isTeacher" class="mb-3">
      <button class="btn btn-primary" @click="openCreateModal">
        <i class="fas fa-plus me-2"></i>新しいルームを作成
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else-if="rooms.length === 0" class="alert alert-info">
      参加しているチャットルームがありません
    </div>

    <div v-else class="list-group">
      <a
        v-for="room in rooms"
        :key="room.id"
        href="#"
        class="list-group-item list-group-item-action"
        @click.prevent="openRoom(room.id)"
      >
        <div class="d-flex w-100 justify-content-between align-items-start">
          <div class="flex-grow-1">
            <h5 class="mb-1">
              {{ room.name }}

              <!-- 未読メッセージ数 -->
              <span v-if="room.unread_count > 0" class="badge bg-danger ms-2">
                {{ room.unread_count }}
              </span>
            </h5>
            <p v-if="room.last_message" class="mb-1 text-muted">
              {{ room.last_message.substring(0, 50) }}
              <span v-if="room.last_message.length > 50">...</span>
            </p>
            <small class="text-muted">
              <i class="fas fa-users me-1"></i>{{ room.participant_count }}人
              <span v-if="room.last_message_at" class="ms-2">
                <i class="fas fa-clock me-1"></i
                >{{ formatDate(room.last_message_at) }}
              </span>
            </small>
          </div>
          <i class="fas fa-chevron-right text-muted"></i>
        </div>
      </a>
    </div>

    <div
      v-if="showCreateModal"
      class="modal d-block"
      style="background: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">新しいチャットルーム</h5>
            <button
              type="button"
              class="btn-close"
              @click="showCreateModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label"
                >ルーム名 <span class="text-danger">*</span></label
              >
              <input
                type="text"
                class="form-control"
                v-model="newRoom.name"
                placeholder="例: 1年A組 連絡用"
              />
            </div>

            <div class="mb-3">
              <label class="form-label">説明（任意）</label>
              <textarea
                class="form-control"
                v-model="newRoom.description"
                rows="2"
                placeholder="ルームの用途など"
              ></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label"
                >参加者を追加 <span class="text-danger">*</span></label
              >
              <input
                type="text"
                class="form-control"
                v-model="searchQuery"
                @input="searchAccounts"
                placeholder="名前で検索"
              />

              <div v-if="searchResults.length > 0" class="list-group mt-2">
                <a
                  v-for="account in searchResults"
                  :key="account.id"
                  href="#"
                  class="list-group-item list-group-item-action"
                  @click.prevent="addParticipant(account)"
                >
                  {{ account.name }}
                  <span class="badge bg-secondary ms-2">
                    {{ account.role === "teacher" ? "教師" : "生徒" }}
                  </span>
                  <span v-if="account.grade" class="ms-1">
                    {{ account.grade }}年{{ account.class_name }}組
                  </span>
                </a>
              </div>
            </div>

            <div v-if="selectedParticipants.length > 0" class="mb-3">
              <label class="form-label"
                >選択された参加者（{{ selectedParticipants.length }}人）</label
              >
              <div class="d-flex flex-wrap gap-2">
                <span
                  v-for="participant in selectedParticipants"
                  :key="participant.id"
                  class="badge bg-primary"
                >
                  {{ participant.name }}
                  <button
                    type="button"
                    class="btn-close btn-close-white btn-sm ms-2"
                    style="font-size: 0.6rem"
                    @click="removeParticipant(participant.id)"
                  ></button>
                </span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showCreateModal = false"
            >
              キャンセル
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="createRoom"
              :disabled="
                isLoading || !newRoom.name || selectedParticipants.length === 0
              "
            >
              <span
                v-if="isLoading"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              作成
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChatRoomList",
  emits: ["navigate", "updateTitle"],
  data() {
    return {
      rooms: [],
      isLoading: false,
      errorMessage: "",
      userInfo: null,

      showCreateModal: false,
      newRoom: {
        name: "",
        description: "",
        participant_ids: [],
      },

      searchQuery: "",
      searchResults: [],
      selectedParticipants: [],
    };
  },
  computed: {
    isTeacher() {
      return (
        this.userInfo &&
        (this.userInfo.role === "teacher" || this.userInfo.role === "admin")
      );
    },
  },
  async mounted() {
    console.log("=== ChatRoomList mounted ===");

    // トークンの確認
    const token = sessionStorage.getItem("access_token");
    console.log(
      "Token in storage:",
      token ? token.substring(0, 20) + "..." : "null"
    );
    console.log(
      "Token in axios:",
      axios.defaults.headers.common["Authorization"]
    );

    // ★ トークンがない場合は設定
    if (!axios.defaults.headers.common["Authorization"] && token) {
      console.log("Setting token to axios...");
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }

    this.$emit("updateTitle", {
      title: "チャットルーム",
      icon: "fas fa-comments",
      showBackButton: true,
    });

    const storedUser = sessionStorage.getItem("currentUser");
    if (storedUser) {
      this.userInfo = JSON.parse(storedUser);
      console.log("User info:", this.userInfo);
    }

    await this.loadRooms();
  },
  methods: {
    async loadRooms() {
      this.isLoading = true;
      this.errorMessage = "";

      console.log("Loading rooms...");
      console.log("Request headers:", axios.defaults.headers.common);

      try {
        const response = await axios.get("http://127.0.0.1:8000/chat/rooms");
        console.log("Rooms loaded:", response.data);
        this.rooms = response.data;
      } catch (err) {
        console.error("Load rooms error:", err);
        console.error("Error response:", err.response?.data);
        this.errorMessage =
          "ルーム一覧の読み込みに失敗しました: " +
          (err.response?.data?.detail || err.message);
      } finally {
        this.isLoading = false;
      }
    },

    openCreateModal() {
      this.showCreateModal = true;
      this.newRoom = {
        name: "",
        description: "",
        participant_ids: [],
      };
      this.selectedParticipants = [];
    },

    async searchAccounts() {
      if (!this.searchQuery) {
        this.searchResults = [];
        return;
      }

      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/chat/accounts/search",
          { params: { query: this.searchQuery } }
        );
        this.searchResults = response.data;
      } catch (err) {
        console.error(err);
      }
    },

    addParticipant(account) {
      if (!this.selectedParticipants.find((p) => p.id === account.id)) {
        this.selectedParticipants.push(account);
      }
      this.searchQuery = "";
      this.searchResults = [];
    },

    removeParticipant(accountId) {
      this.selectedParticipants = this.selectedParticipants.filter(
        (p) => p.id !== accountId
      );
    },

    async createRoom() {
      if (!this.newRoom.name) {
        alert("ルーム名を入力してください");
        return;
      }

      if (this.selectedParticipants.length === 0) {
        alert("参加者を選択してください");
        return;
      }

      this.isLoading = true;

      try {
        const roomData = {
          name: this.newRoom.name,
          description: this.newRoom.description,
          participant_ids: this.selectedParticipants.map((p) => p.id),
        };

        await axios.post("http://127.0.0.1:8000/chat/rooms", roomData);

        this.showCreateModal = false;
        await this.loadRooms();
      } catch (err) {
        console.error(err);
        alert("ルームの作成に失敗しました");
      } finally {
        this.isLoading = false;
      }
    },

    openRoom(roomId) {
      // ❌ 修正前: this.$emit('navigate', 'chat-room', roomId);
      // ✅ 修正後: App.vueでは2つの引数を受け取れないため、別のイベントを使う
      // または、App.vueの@navigateハンドラーを修正する必要がある

      // オプション1: navigateToChatイベントを使う（App.vueに対応する@navigate-to-chatが必要）
      // this.$emit('navigateToChat', 'chat-room', roomId);

      // オプション2: App.vueのsetCurrentPageを拡張して使う（推奨）
      this.$parent.navigateToChat("chat-room", roomId);
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);

      if (diffMins < 1) return "今";
      if (diffMins < 60) return `${diffMins}分前`;
      if (diffMins < 1440) return `${Math.floor(diffMins / 60)}時間前`;

      return date.toLocaleDateString("ja-JP");
    },
  },
};
</script>

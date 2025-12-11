<template>
  <div class="container-fluid h-100 d-flex flex-column">
    <div class="row flex-grow-1">

      <!-- 左側：参加者一覧 -->
      <div class="col-3 border-end bg-light p-3 overflow-auto" style="max-height: 80vh;">
        <div class="row mb-3 align-items-center">
          <div class="col">
            <h6 class="fw-bold mb-0">
              <i class="fas fa-users me-2"></i>参加者
            </h6>
          </div>

          <div class="col-auto" v-if="isCreator">
            <button class="btn btn-sm btn-outline-primary" @click="showParticipantsModal = true">
              <i class="fas fa-user-plus me-1"></i>追加
            </button>
          </div>
        </div>

        <ul class="list-group">
          <li v-for="p in participants" :key="getParticipantId(p)" class="list-group-item">
            <div class="d-flex align-items-center">
              <i v-if="onlineUsers.includes(Number(getParticipantId(p)))" class="fas fa-circle text-success me-2" />
              <i v-else class="fas fa-circle text-muted me-2" />

              <div>
                <span :class="'badge me-2 ' + getRoleBadgeClass(p.role)">
                  {{ getRoleBadgeText(p.role) }}
                </span>
                {{ p.name }}
              </div>
            </div>
          </li>
        </ul>

        <!-- Router対応：戻るボタン -->
        <button class="btn btn-outline-secondary w-100 mt-3" @click="goBack">
          <i class="fas fa-arrow-left me-2"></i>戻る
        </button>
      </div>

      <!-- 右側：チャット -->
      <div class="col-9 d-flex flex-column">

        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

        <div ref="messagesContainer" class="flex-grow-1 overflow-auto p-3 bg-white" style="max-height: 60vh;">
          <div v-for="msg in messages" :key="msg.id"
               :class="['mb-3', isMyMessage(msg.sender_id) ? 'text-end' : 'text-start']">

            <div :class="[
                'd-inline-block','p-2','rounded',
                isMyMessage(msg.sender_id) ? 'bg-primary text-white' : 'bg-light'
              ]"
              style="max-width: 70%;">

              <div v-if="!isMyMessage(msg.sender_id)" class="small fw-bold mb-1">
                {{ msg.sender_name }}
              </div>

              <div>{{ msg.message }}</div>
              <div class="small opacity-75 mt-1">{{ formatTime(msg.sent_at) }}</div>
            </div>
          </div>

          <div v-if="typingUsersText" class="small text-muted fst-italic mt-2">
            {{ typingUsersText }}
          </div>
        </div>

        <div class="p-3 bg-white border-top">
          <div class="input-group">
            <input type="text" class="form-control"
                   v-model="newMessage"
                   @input="handleInput"
                   @keyup.enter="sendMessage"
                   :disabled="!wsConnected"
                   placeholder="メッセージを入力...">

            <button class="btn btn-primary" @click="sendMessage"
                    :disabled="!newMessage.trim() || !wsConnected">
              <i class="fas fa-paper-plane"></i>送信
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 参加者追加モーダル -->
    <div v-if="showParticipantsModal"
         class="modal fade show"
         style="display:block; background:rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">参加者を追加</h5>
            <button type="button" class="btn-close" @click="showParticipantsModal = false"></button>
          </div>

          <div class="modal-body">
            <input v-model="searchQuery" @input="searchAccounts" type="text"
                   class="form-control mb-3" placeholder="名前またはIDで検索...">

            <ul class="list-group mb-3">
              <li v-for="account in searchResults" :key="account.id"
                  class="list-group-item d-flex justify-content-between align-items-center">
                <span>{{ account.name }}</span>
                <button class="btn btn-sm btn-outline-success" @click="addParticipant(account)">追加</button>
              </li>
            </ul>

            <div v-if="selectedParticipants.length > 0">
              <h6 class="fw-bold">追加予定の参加者</h6>
              <ul class="list-group">
                <li v-for="p in selectedParticipants"
                    :key="p.id"
                    class="list-group-item">
                  {{ p.name }}
                </li>
              </ul>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showParticipantsModal = false">キャンセル</button>
            <button class="btn btn-primary" @click="saveNewParticipants">保存</button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'ChatRoom',

  data() {
    return {
      room: null,
      roomId: null,
      messages: [],
      newMessage: '',
      errorMessage: '',
      userInfo: null,
      ws: null,
      wsConnected: false,
      typingUsers: new Set(),
      onlineUsers: [],
      participants: [],
      showParticipantsModal: false,
      searchQuery: '',
      searchResults: [],
      selectedParticipants: []
    };
  },

  computed: {
    isCreator() {
      return this.room && this.userInfo && this.room.creator_id === this.userInfo.id;
    },
    typingUsersText() {
      if (this.typingUsers.size === 0) return '';
      const users = [...this.typingUsers];
      if (users.length === 1) return `${users[0]}が入力中...`;
      if (users.length === 2) return `${users[0]}と${users[1]}が入力中...`;
      return `${users[0]}ほか${users.length - 1}人が入力中...`;
    }
  },

  async mounted() {
    // router から roomId を取得
    this.roomId = Number(this.$route.params.id);

    const storedUser = sessionStorage.getItem('currentUser');
    if (storedUser) this.userInfo = JSON.parse(storedUser);

    const token = sessionStorage.getItem('access_token');
    if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    await this.loadRoomDetail();
    await this.loadInitialMessages();
    this.connectWebSocket();

    this.$nextTick(() => this.scrollToBottom());
  },

  beforeUnmount() {
    this.disconnectWebSocket();
  },

  methods: {
    goBack() {
      this.$router.back();
    },

    getParticipantId(p) {
      return p.user_id || p.id;
    },

    async loadRoomDetail() {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/chat/rooms/${this.roomId}`);
        this.room = res.data;
        this.participants = res.data.participants;
      } catch (e) {
        this.errorMessage = 'ルーム情報の取得に失敗しました。';
      }
    },

    async loadInitialMessages() {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/chat/rooms/${this.roomId}/messages`);
        this.messages = res.data;
      } catch (e) {
        console.error('Message load failed', e);
      }
    },

    connectWebSocket() {
      if (!this.userInfo) return;

      const wsUrl = `ws://127.0.0.1:8000/notifications/ws/chat/${this.roomId}/${this.userInfo.id}`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        this.wsConnected = true;
        this.onlineUsers.push(Number(this.userInfo.id));
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleWebSocketMessage(data);
      };

      this.ws.onclose = () => {
        this.wsConnected = false;
      };
    },

    disconnectWebSocket() {
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }
    },

    handleWebSocketMessage(data) {
      if (data.type === 'message') {
        this.messages.push(data);
        this.$nextTick(() => this.scrollToBottom());
      }
    },

    sendMessage() {
      if (!this.newMessage.trim()) return;

      const content = this.newMessage.trim();
      this.newMessage = '';

      this.ws.send(
        JSON.stringify({
          type: 'message',
          content
        })
      );
    },

    scrollToBottom() {
      const el = this.$refs.messagesContainer;
      if (el) el.scrollTop = el.scrollHeight;
    }
  }
};
</script>

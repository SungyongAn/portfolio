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
              <i class="fas fa-user-plus me-1"></i> 追加
            </button>
          </div>
        </div>

        <ul class="list-group">
          <li v-for="p in participants" :key="getParticipantId(p)" class="list-group-item">
            <div class="d-flex align-items-center">
              <!-- ✅ getParticipantId() を使用 -->
              <i v-if="onlineUsers.includes(Number(getParticipantId(p)))" 
                 class="fas fa-circle text-success me-2"></i>
              <i v-else class="fas fa-circle text-muted me-2"></i>

              <div>
                <span :class="'badge me-2 ' + getRoleBadgeClass(p.role)">
                  {{ getRoleBadgeText(p.role) }}
                </span>
                {{ p.name }}
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- 右側：チャット -->
      <div class="col-9 d-flex flex-column">
        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

        <div ref="messagesContainer" class="flex-grow-1 overflow-auto p-3 bg-white" style="max-height: 60vh;">
          <div v-for="msg in messages" :key="msg.id"
              :class="['mb-3', isMyMessage(msg.sender_id) ? 'text-end' : 'text-start']">
            <div :class="[
                  'd-inline-block', 'p-2', 'rounded',
                  isMyMessage(msg.sender_id) ? 'bg-primary text-white' : 'bg-light'
                ]" style="max-width: 70%;">
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
            <button class="btn btn-primary" @click="sendMessage" :disabled="!newMessage.trim() || !wsConnected">
              <i class="fas fa-paper-plane"></i> 送信
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- モーダル：参加者追加 -->
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
            <input v-model="searchQuery" @input="searchAccounts"
                   type="text" class="form-control mb-3"
                   placeholder="名前またはIDで検索...">
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
                <li v-for="p in selectedParticipants" :key="p.id" class="list-group-item">
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
import axios from 'axios'

export default {
  props: ['roomId'],
  emits: ['back', 'updateTitle'],

  data() {
    return {
      room: null,
      messages: [],
      newMessage: '',
      isLoading: false,
      isSending: false,
      errorMessage: '',
      userInfo: null,

      // WebSocket関連
      ws: null,
      wsConnected: false,
      reconnectAttempts: 0,
      maxReconnectAttempts: 5,
      reconnectDelay: 3000,

      // タイピング通知
      typingUsers: new Set(),
      typingTimeout: null,

      // オンライン状態
      onlineUsers: [],  // 配列で管理

      // 参加者追加
      showParticipantsModal: false,
      searchQuery: '',
      searchResults: [],
      selectedParticipants: [],

      // 参加者一覧
      participants: []
    };
  },

  computed: {
    isCreator() {
      return this.room && this.userInfo && this.room.creator_id === this.userInfo.id;
    },
    isTeacher() {
      return this.userInfo && (this.userInfo.role === 'teacher' || this.userInfo.role === 'admin');
    },
    typingUsersText() {
      if (this.typingUsers.size === 0) return '';
      const users = Array.from(this.typingUsers);
      if (users.length === 1) return `${users[0]}が入力中...`;
      if (users.length === 2) return `${users[0]}と${users[1]}が入力中...`;
      return `${users[0]}ほか${users.length - 1}人が入力中...`;
    }
  },

  async mounted() {
    const storedUser = sessionStorage.getItem('currentUser');
    if (storedUser) this.userInfo = JSON.parse(storedUser);

    const token = sessionStorage.getItem('access_token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      this.errorMessage = '認証トークンが見つかりません。再ログインしてください。';
      return;
    }

    await this.loadRoomDetail();
    await this.loadInitialMessages();
    // 既読機能
    await this.markAsRead();

    this.connectWebSocket();

    this.$nextTick(() => this.scrollToBottom());

    window.addEventListener('beforeunload', this.disconnectWebSocket);
  },

  beforeUnmount() {
    this.disconnectWebSocket();

    // ✅ イベントリスナーの削除
    window.removeEventListener('beforeunload', this.disconnectWebSocket);

    if (this.typingTimeout) clearTimeout(this.typingTimeout);
  },

  methods: {
    // ✅ 参加者のIDを取得するヘルパーメソッド
    getParticipantId(participant) {
      // user_id または id のどちらかを返す
      return participant.user_id || participant.id;
    },

    // WebSocket接続
    connectWebSocket() {
      if (!this.userInfo || !this.roomId) return;

      const wsUrl = `ws://127.0.0.1:8000/notifications/ws/chat/${this.roomId}/${this.userInfo.id}`;
      console.log('Connecting WebSocket:', wsUrl);

      try {
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
          console.log('✅ WebSocket connected');
          this.wsConnected = true;
          this.reconnectAttempts = 0;
          
          // 自分のIDを追加
          const myId = Number(this.userInfo.id);
          if (!this.onlineUsers.includes(myId)) {
            this.onlineUsers.push(myId);
          }
          
          console.log('📊 オンライン状態:', {
            myId: myId,
            onlineUsers: this.onlineUsers,
            participants: this.participants.map(p => ({
              name: p.name,
              id: this.getParticipantId(p)
            }))
          });
        };

        this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.handleWebSocketMessage(data);
        };

        this.ws.onclose = (event) => {
          console.log('WebSocket disconnected', event.code, event.reason);
          this.wsConnected = false;
          this.onlineUsers = [];

          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => this.connectWebSocket(), this.reconnectDelay);
          } else {
            this.errorMessage = 'WebSocket接続が切断されました。再読み込みしてください。';
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
        };

      } catch (e) {
        console.error('WebSocket init error:', e);
        this.errorMessage = 'WebSocket接続に失敗しました';
      }

    },

    getRoleBadgeText(role) {
      const roleMap = {
        'teacher': '教師',
        'student': '生徒',
        'admin': '管理者',
        'school_nurse': '養護教諭'
      };
      return roleMap[role] || '不明';
    },

    // 役割に応じた色を返す
    getRoleBadgeClass(role) {
      const classMap = {
        'teacher': 'bg-primary',      // 青
        'student': 'bg-secondary',    // グレー
        'admin': 'bg-warning text-dark', // 黄色
        'school_nurse': 'bg-success'  // 緑 ✅ 追加
      };
      return classMap[role] || 'bg-secondary';
    },

    handleWebSocketMessage(data) {
      switch (data.type) {
        case 'user_joined':
        const joinId = Number(data.user_id);
        if (!this.onlineUsers.includes(joinId)) {
          this.onlineUsers.push(joinId);
        }
        console.log(`👋 ${data.user_name} が参加しました`);
        break;

        case 'online_users':
        // バックエンドから初期オンラインユーザーを取得
        this.onlineUsers = data.user_ids.map(id => Number(id));
        const myId = Number(this.userInfo.id);
        if (!this.onlineUsers.includes(myId)) {
          this.onlineUsers.push(myId);
        }
        console.log('📊 初期オンラインユーザー:', this.onlineUsers);
        break;

        case 'user_left':
        const leftId = Number(data.user_id);
        const index = this.onlineUsers.indexOf(leftId);
        if (index > -1) {
          this.onlineUsers.splice(index, 1);
        }
        console.log(`👋 ${data.user_name} が退出しました`);
        break;

        // タイピング通知の処理
        case 'typing':
        if (data.is_typing) {
          this.typingUsers.add(data.user_name);
        } else {
          this.typingUsers.delete(data.user_name);
        }
        break;

        // 新着メッセージの処理
        case 'message':
        this.messages.push({
          id: data.message_id,
          sender_id: data.sender_id,
          sender_name: data.sender_name,
          message: data.message,
          sent_at: data.sent_at
        });
        this.$nextTick(() => this.scrollToBottom());
        break;

        default:
        console.warn('未知のメッセージタイプ:', data.type);
      }
    },

    sendWebSocketMessage(type, payload) {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        this.errorMessage = 'WebSocket接続が切断されています';
        return false;
      }
      this.ws.send(JSON.stringify({ type, ...payload }));
      return true;
    },

    async markAsRead() {
      try {
        await axios.post(
          `http://127.0.0.1:8000/chat/rooms/${this.roomId}/read`
        );
        console.log('✅ メッセージを既読にしました');
      } catch (err) {
        console.error('❌ 既読処理失敗:', err);
        // エラーは致命的ではないのでユーザーには表示しない
      }
    },

    async sendMessage() {
      if (!this.newMessage.trim()) return;
      const content = this.newMessage.trim();
      this.newMessage = '';
      this.sendWebSocketMessage('message', { content });
      this.sendTypingNotification(false);
    },

    handleInput() {
      this.sendTypingNotification(true);
      if (this.typingTimeout) clearTimeout(this.typingTimeout);
      this.typingTimeout = setTimeout(() => this.sendTypingNotification(false), 3000);
    },

    sendTypingNotification(isTyping) {
      this.sendWebSocketMessage('typing', { is_typing: isTyping });
    },

    async loadRoomDetail() {
      try {
        const res = await axios.get(`${API_BASE_URL}/chat/rooms/${this.roomId}`);
        this.room = res.data;
        this.participants = res.data.participants;
        
        console.log('✅ ルーム詳細:', {
          name: this.room.name,
          participantCount: this.participants.length,
          participants: this.participants.map(p => ({
            name: p.name,
            id: this.getParticipantId(p)
          }))
        });
        
        this.$emit('updateTitle', {
          title: this.room.name,
          icon: 'fas fa-comments',
          showBackButton: true
        });
      } catch (err) {
        console.error('❌ ルーム詳細取得失敗:', err);
        this.errorMessage = 'ルーム情報の取得に失敗しました';
      }
    },

    async loadInitialMessages() {
      try {
        const res = await axios.get(`${API_BASE_URL}/chat/rooms/${this.roomId}/messages`);
        this.messages = res.data;
      } catch (err) {
        console.error('メッセージ履歴取得失敗:', err);
      }
    },

    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) container.scrollTop = container.scrollHeight;
    },

    isMyMessage(senderId) {
      return this.userInfo && senderId === this.userInfo.id;
    },

    formatTime(ts) {
      return new Date(ts).toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' });
    },

    async searchAccounts() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        return;
      }
      try {
        const res = await axios.get(`${API_BASE_URL}/chat/accounts/search`, {
          params: { query: this.searchQuery }
        });
        this.searchResults = res.data;
      } catch (err) {
        console.error('Account search failed:', err);
      }
    },

    addParticipant(account) {
      if (!this.selectedParticipants.find(p => p.id === account.id)) {
        this.selectedParticipants.push(account);
      }
      this.searchQuery = '';
      this.searchResults = [];
    },

    async saveNewParticipants() {
      if (this.selectedParticipants.length === 0) {
        alert('追加するユーザーを選択してください');
        return;
      }
      try {
        const ids = this.selectedParticipants.map(p => p.id);
        await axios.post(
          `${API_BASE_URL}/chat/rooms/${this.roomId}/participants`,
          { user_ids: ids }
        );
        alert('参加者を追加しました');
        this.showParticipantsModal = false;
        this.selectedParticipants = [];
        await this.loadRoomDetail();
      } catch (err) {
        console.error('Add participants failed:', err);
        alert('参加者の追加に失敗しました');
      }
    },
    
    // 明示的な切断メソッド
    disconnectWebSocket() {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        // バックエンドに退出を通知
        this.sendWebSocketMessage('user_leaving', { 
          user_id: this.userInfo.id 
        });
      
        // 接続を切断
        this.ws.close(1000, 'User left room');
        this.ws = null;
        this.wsConnected = false;
        this.onlineUsers = [];
      
        console.log('✅ WebSocket disconnected (manual)');
      }
    },
  },
};
</script>

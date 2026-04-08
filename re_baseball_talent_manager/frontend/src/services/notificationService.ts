export type NotificationMessage = {
  type: string;
  message: string;
};

// モジュール状態
let socket: WebSocket | null = null;

let onMessageCallback: ((data: NotificationMessage) => void) | null = null;

let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

let isIntentionalClose: boolean = false;


// 接続
export function connectNotifications(
    token: string,
  onMessage: (data: NotificationMessage) => void
): void {
  // コールバック保存
  onMessageCallback = onMessage;

  // 既に接続中なら一度切断
  if (socket) {
    isIntentionalClose = true;
    socket.close();
    socket = null;
  }

  const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const wsBase = apiBase.replace(/^http/, "ws");
  const url = `${wsBase}/ws/notifications?token=${token}`;

  socket = new WebSocket(url);

  // 接続成功
  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  // メッセージ受信
  socket.onmessage = (event) => {
    try {
      const data: NotificationMessage = JSON.parse(event.data);

      if (onMessageCallback) {
        onMessageCallback(data);
      }
    } catch (e) {
      console.error("Failed to parse message", e);
    }
  };

  // 切断時（再接続）
  socket.onclose = () => {
    console.log("WebSocket disconnected");

    if (isIntentionalClose) {
      isIntentionalClose = false; // フラグをリセット
      return; // 意図的な切断なので再接続しない
    }

    reconnectTimer = setTimeout(() => {
      console.log("Reconnecting WebSocket...");
      if (onMessageCallback) {
        connectNotifications(token, onMessageCallback);
      }
    }, 3000);
  };

  // エラー時
  socket.onerror = (err) => {
    console.error("WebSocket error", err);
  };
}

// 切断
export function disconnectNotifications(): void {
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }

  if (socket) {
    isIntentionalClose = true;
    socket.close();
    socket = null;
  }

  onMessageCallback = null;

  console.log("WebSocket manually disconnected");
}

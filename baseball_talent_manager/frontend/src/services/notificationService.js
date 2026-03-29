let socket = null;
let onMessageCallback = null;
let reconnectTimer = null;

export function connectNotifications(token, onMessage) {
  // コールバック保存
  onMessageCallback = onMessage;

  // 既に接続中なら一度切断
  if (socket) {
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
      const data = JSON.parse(event.data);

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

    // 自動再接続（3秒後）
    reconnectTimer = setTimeout(() => {
      console.log("Reconnecting WebSocket...");
      connectNotifications(token, onMessageCallback);
    }, 3000);
  };

  // エラー時
  socket.onerror = (err) => {
    console.error("WebSocket error", err);
  };
}

export function disconnectNotifications() {
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }

  if (socket) {
    socket.close();
    socket = null;
  }

  onMessageCallback = null;

  console.log("WebSocket manually disconnected");
}

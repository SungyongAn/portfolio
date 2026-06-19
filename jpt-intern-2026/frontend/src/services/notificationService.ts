/**
 * notificationService.ts
 * WebSocket接続の管理・通知受信・再接続ロジックを担うサービス
 */

import { ref } from "vue";

export type WsNotification = {
  type: "notification";
  title: string;
  message: string;
  project_id: number;
};

// 未読バッジ数（AppHeader.vueからreactiveに参照する）
export const unreadCount = ref(0);

// 最後に受信した通知（トースト表示用）
export const latestNotification = ref<WsNotification | null>(null);

const WS_BASE = import.meta.env.VITE_WS_URL ?? "ws://158.101.148.143";
console.log("WS_BASE:", WS_BASE);
const RECONNECT_INTERVAL_MS = 5000;
const MAX_RECONNECT = 10;

let ws: WebSocket | null = null;
let reconnectCount = 0;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
let stopped = false;

/**
 * WebSocket接続を開始する。
 * ログイン後に一度だけ呼び出す。
 */
export function startNotificationWs(
  accessToken: string,
  initialUnread: number,
): void {
  if (
    ws &&
    (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)
  ) {
    return;
  }

  stopped = false;
  unreadCount.value = initialUnread;
  _connect(accessToken);
}

/**
 * WebSocket接続を切断する（ログアウト時）。
 */
export function stopNotificationWs(): void {
  stopped = true;
  reconnectCount = 0;
  if (reconnectTimer !== null) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
  if (ws) {
    ws.close();
    ws = null;
  }
}

function _connect(token: string): void {
  if (stopped) return;

  if (
    ws &&
    (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)
  ) {
    return;
  }

  const url = `${WS_BASE}/api/notifications/ws?token=${encodeURIComponent(token)}`;
  ws = new WebSocket(url);

  ws.onopen = () => {
    reconnectCount = 0;
  };

  ws.onmessage = (event: MessageEvent) => {
    try {
      const data = JSON.parse(event.data) as WsNotification;
      if (data.type === "notification") {
        unreadCount.value += 1;
        latestNotification.value = data;
      }
    } catch {
      // JSONパース失敗は無視
    }
  };

  ws.onclose = (event: CloseEvent) => {
    // 4001: 認証エラーは再接続しない
    if (event.code === 4001 || stopped) return;
    _scheduleReconnect(token);
  };

  ws.onerror = () => {
    ws?.close();
  };
}

function _scheduleReconnect(token: string): void {
  if (stopped || reconnectCount >= MAX_RECONNECT) return;
  reconnectCount += 1;
  reconnectTimer = setTimeout(() => {
    _connect(token);
  }, RECONNECT_INTERVAL_MS);
}

# notification_api.md

# 通知API設計

## 1. 概要

本ドキュメントは、`re_quest1` における通知APIおよびWebSocket通知設計を定義する。

通知機能では、案件承認・却下・着手・完了・タスク割当などのイベントをユーザーへ通知する。

第1段階では、既存 `quest_1` の通知仕様を維持し、
React + ASP.NET Core 版で同等の通知表示・既読処理・リアルタイム通知を再現する。

---

## 2. 対象機能

- 通知一覧取得
- 未読件数表示
- 通知詳細表示
- 既読処理
- 全件既読処理
- WebSocket通知

---

## 3. 通知一覧取得API

## Endpoint

```text
GET /api/notifications
```

---

## 認証

必要。

```text
Authorization: Bearer <token>
```

---

## Response

```json
[
  {
    "id": 1,
    "user_id": 2,
    "project_id": 1,
    "type": "APPROVAL_REQUEST",
    "title": "承認依頼",
    "message": "新しい案件の承認依頼があります。",
    "is_read": false,
    "created_at": "2026-05-01T10:00:00"
  }
]
```

---

## 4. 既読API

## Endpoint

```text
POST /api/notifications/{id}/read
```

---

## Path Parameter

| 項目 | 型   | 説明   |
| ---- | ---- | ------ |
| id   | long | 通知ID |

---

## Response

```json
{
  "success": true
}
```

---

## 5. 全件既読API

## Endpoint

```text
POST /api/notifications/read-all
```

---

## Response

```json
{
  "success": true
}
```

---

## 6. WebSocket通知

## Endpoint

```text
/api/notifications/ws
```

---

## 接続方針

ログイン後、フロントエンドからWebSocketへ接続する。

```text
ws://localhost:5000/api/notifications/ws
```

---

## 送信データ例

```json
{
  "type": "APPROVAL_REQUEST",
  "title": "承認依頼",
  "message": "新しい案件の承認依頼があります。",
  "project_id": 1
}
```

---

## 7. 通知種別

| 種別              | 内容       |
| ----------------- | ---------- |
| APPROVAL_REQUEST  | 承認依頼   |
| APPROVED          | 承認完了   |
| REJECTED          | 却下       |
| PROJECT_STARTED   | 案件着手   |
| PROJECT_COMPLETED | 案件完了   |
| TASK_ASSIGNED     | タスク割当 |

---

## 8. 通知発行タイミング

| イベント   | 通知種別                    |
| ---------- | --------------------------- |
| 案件申請   | APPROVAL_REQUEST            |
| 部門承認   | APPROVAL_REQUEST / APPROVED |
| 本部承認   | APPROVED                    |
| 却下       | REJECTED                    |
| 案件着手   | PROJECT_STARTED             |
| 案件完了   | PROJECT_COMPLETED           |
| タスク割当 | TASK_ASSIGNED               |

---

## 9. 認可方針

通知はログインユーザー自身に紐づくもののみ取得・更新可能とする。

## 取得可能

```text
notification.user_id == current_user.id
```

---

## 既読可能

```text
notification.user_id == current_user.id
```

---

## 他ユーザー通知

他ユーザー宛て通知にはアクセス不可。

```text
403 Forbidden
```

---

## 10. IDOR対策

通知IDを直接指定された場合も、必ず通知先ユーザーを確認する。

```text
Notification取得
 ↓

notification.user_id == current_user.id を確認
 ↓

許可
または
403
```

---

## 11. Controller

```text
NotificationController
```

---

## 12. Service

```text
NotificationService
PermissionService
```

---

## 13. Repository

```text
NotificationRepository
```

---

## 14. WebSocket管理

ASP.NET Coreでは、通知用WebSocket接続を管理する。

## 想定クラス

```text
NotificationWebSocketManager
```

---

## 主な責務

- ユーザーごとの接続管理
- 通知イベント送信
- 接続解除処理
- 切断時のクリーンアップ

---

## 15. フロントエンド連携

React側では、通知ストアで通知状態を管理する。

## 想定Store

```text
notificationStore
```

---

## 管理する状態

- notifications
- unreadCount
- selectedNotification
- isOpen
- websocketConnection

---

## 主な処理

- fetchNotifications
- markAsRead
- markAllAsRead
- connectWebSocket
- disconnectWebSocket

---

## 16. UI表示方針

既存Vue版の通知UIを維持する。

## PC

- Sidebarから通知Popoverを表示
- 通知一覧を表示
- 通知詳細はDialogで表示

---

## モバイル

- Headerから通知Drawerを表示
- 通知一覧を表示
- 通知詳細はDialogで表示

---

## 共通

- 未読件数表示
- 既読処理
- 全件既読処理
- WebSocketによる新着通知反映

---

## 17. エラーレスポンス

## 権限不足

```json
{
  "detail": "Forbidden"
}
```

Status:

```text
403 Forbidden
```

---

## データなし

```json
{
  "detail": "Notification not found"
}
```

Status:

```text
404 Not Found
```

---

## 未認証

```json
{
  "detail": "Unauthorized"
}
```

Status:

```text
401 Unauthorized
```

---

## 18. 第1段階方針

既存PoCの通知仕様を維持する。

変更しない内容

- APIパス
- 通知種別
- 既読処理
- 全件既読処理
- WebSocket通知
- PC / モバイルの通知表示方針
- IDOR対策

---

## 19. 今後の改善候補

移植完了後、以下を検討する。

- 通知テンプレート管理
- 通知種別の細分化
- 通知の未読戻し
- 通知検索
- 通知カテゴリ
- 通知保存期間設定
- WebSocket再接続処理の強化
- SignalR導入検討

---

## 20. まとめ

通知APIでは、ユーザーごとの通知取得・既読処理・リアルタイム通知を管理する。

第1段階では既存PoCの通知仕様を維持し、
React + ASP.NET Core 版で同等の通知機能を再現する。

# state_management.md

# 状態管理設計

## 1. 概要

本ドキュメントは、`re_quest1` の React フロントエンドにおける状態管理設計を定義する。

状態管理には Zustand を使用する。

第1段階では、既存Vue版で Pinia が担当していた状態管理を、React版では Zustand に移植する。

---

# 2. 使用技術

```text
Zustand
```

---

# 3. 基本方針

## 方針

- グローバルに必要な状態のみStoreで管理する
- 画面内だけで使う状態は `useState` で管理する
- API取得処理は必要に応じてStoreまたはHooksに分離する
- 認証状態は `authStore` に集約する
- 通知状態は `notificationStore` に集約する
- ダッシュボード状態は `dashboardStore` に集約する

---

# 4. Store一覧

| Store             | 役割                   |
| ----------------- | ---------------------- |
| authStore         | 認証状態管理           |
| dashboardStore    | ダッシュボード状態管理 |
| notificationStore | 通知状態管理           |

---

# 5. authStore

## 役割

認証状態を管理する。

---

## 管理する状態

| 状態            | 型      | 概要       |
| --------------- | ------- | ---------- | ------------------- |
| accessToken     | string  | null       | JWTアクセストークン |
| currentUser     | User    | null       | ログインユーザー    |
| isAuthenticated | boolean | 認証済みか |
| role            | Role    | null       | ロール              |
| departmentId    | number  | null       | 所属部門ID          |

---

## 主な処理

| 処理           | 概要             |
| -------------- | ---------------- |
| login          | ログイン処理     |
| logout         | ログアウト処理   |
| setCurrentUser | ユーザー情報設定 |
| clearAuth      | 認証情報削除     |

---

## 使用箇所

- LoginPage
- ProtectedRoute
- RoleRoute
- apiClient
- Sidebar
- Header

---

# 6. dashboardStore

## 役割

ダッシュボード表示状態を管理する。

---

## 管理する状態

| 状態           | 型               | 概要         |
| -------------- | ---------------- | ------------ | -------------- |
| summary        | DashboardSummary | null         | サマリ情報     |
| projects       | Project[]        | 表示対象案件 |
| selectedFilter | string           | null         | 選択中フィルタ |
| activePanel    | string           | 表示中パネル |
| loading        | boolean          | 読み込み中か |

---

## 主な処理

| 処理              | 概要                     |
| ----------------- | ------------------------ |
| fetchDashboard    | ダッシュボード情報取得   |
| setSelectedFilter | フィルタ設定             |
| setActivePanel    | 表示パネル設定           |
| clearDashboard    | ダッシュボード状態初期化 |

---

## 使用箇所

- DashboardPage
- ApplicantDashboard
- DeptManagerDashboard
- HqManagerDashboard
- TaskMemberDashboard
- SummaryCards
- ProjectListPanel

---

# 7. notificationStore

## 役割

通知状態を管理する。

---

## 管理する状態

| 状態                 | 型             | 概要           |
| -------------------- | -------------- | -------------- | ------------- |
| notifications        | Notification[] | 通知一覧       |
| unreadCount          | number         | 未読件数       |
| isOpen               | boolean        | 通知UI表示状態 |
| selectedNotification | Notification   | null           | 選択中通知    |
| socket               | WebSocket      | null           | WebSocket接続 |

---

## 主な処理

| 処理                    | 概要          |
| ----------------------- | ------------- |
| fetchNotifications      | 通知一覧取得  |
| markAsRead              | 既読処理      |
| markAllAsRead           | 全件既読      |
| connectWebSocket        | WebSocket接続 |
| disconnectWebSocket     | WebSocket切断 |
| setSelectedNotification | 通知詳細選択  |

---

## 使用箇所

- Sidebar
- Header
- NotificationPopover
- NotificationDrawer
- NotificationDetailDialog

---

# 8. 画面内状態

画面内でのみ使用する状態は、Storeではなく `useState` で管理する。

## 例

| 状態            | 使用箇所               |
| --------------- | ---------------------- |
| Dialog開閉      | 各Dialogコンポーネント |
| Drawer開閉      | ProjectCreateDrawer    |
| Form入力値      | 各Form                 |
| Table選択状態   | 各Table                |
| Loading補助状態 | 各Page                 |

---

# 9. API取得方針

## 第1段階

第1段階では、StoreまたはHooksからAPIを呼び出す。

```text
Page
 ↓

Store / Hook
 ↓

api
 ↓

apiClient
```

---

## 将来方針

移植完了後、React Query導入を検討する。

```text
Page
 ↓

useQuery / useMutation
 ↓

api
 ↓

apiClient
```

---

# 10. Vue PiniaからZustandへの対応

| Pinia          | Zustand                  |
| -------------- | ------------------------ |
| defineStore    | create                   |
| state          | state                    |
| getters        | selector / derived state |
| actions        | functions                |
| storeToRefs    | selector                 |
| persist plugin | persist middleware       |

---

# 11. 永続化方針

## 第1段階

既存PoCと同様に、アクセストークンをフロントエンド側で保持する。

候補：

```text
memory
localStorage
sessionStorage
```

---

## 注意点

- XSSリスクを考慮する
- 本格運用時は HttpOnly Cookie 化を検討する
- 第1段階では既存PoC再現を優先する

---

# 12. 初期化処理

アプリ起動時に以下を行う。

```text
authStore初期化
 ↓

認証状態確認
 ↓

必要に応じてdashboard取得
 ↓

通知WebSocket接続
```

---

# 13. ログアウト処理

ログアウト時に以下を行う。

```text
accessToken削除
 ↓

currentUser削除
 ↓

dashboardStore初期化
 ↓

notificationStore初期化
 ↓

WebSocket切断
 ↓

/loginへ遷移
```

---

# 14. 第1段階方針

第1段階では、状態管理を複雑化しない。

## 方針

- Store数を増やしすぎない
- 画面内状態はStore化しない
- APIキャッシュは行わない
- 既存PoCの挙動再現を優先する

---

# 15. 今後の改善候補

移植完了後、以下を検討する。

- React Query導入
- Zustand Slice化
- persist middleware導入
- Store責務の再整理
- Form状態管理の専用化
- エラー状態管理の共通化
- Loading状態管理の共通化

---

# 16. まとめ

React版では Zustand を使用し、認証・ダッシュボード・通知の状態を中心に管理する。

第1段階では状態管理を複雑化せず、既存Vue版のPinia相当の役割を再現する。

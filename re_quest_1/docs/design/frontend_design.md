# frontend_design.md

# フロントエンド設計書

## 1. 概要

本ドキュメントは、`re_quest1` におけるフロントエンド設計の概要を定義する。

既存の `quest_1` で実装した Vue 3 + TypeScript 版を基準とし、React + TypeScript による再実装を行う。

第1段階では、UI改善や仕様変更は行わず、既存版と同等の画面構成・操作・表示内容を再現する。

---

## 2. 使用技術

| 種別                 | 技術         |
| -------------------- | ------------ |
| フレームワーク       | React        |
| 言語                 | TypeScript   |
| ビルドツール         | Vite         |
| ルーティング         | React Router |
| 状態管理             | Zustand      |
| UIライブラリ         | MUI          |
| HTTP通信             | fetch        |
| 通知リアルタイム通信 | WebSocket    |

---

## 3. 基本方針

第1段階では、既存Vue版の仕様を維持する。

### 変更しない内容

- 画面構成
- URL設計
- 操作導線
- 表示項目
- API呼び出し仕様
- ロール別表示制御
- Drawer / Dialog / Popover の役割
- 通知表示方式
- ダッシュボード表示内容

### 後回しにする内容

- UIデザイン刷新
- コンポーネントの大幅再設計
- 状態管理の高度化
- React Query 導入
- フォームライブラリ導入
- スマホUI改善
- 新機能追加

---

## 4. 詳細設計

詳細は以下のファイルを参照する。

| ファイル                          | 内容                             |
| --------------------------------- | -------------------------------- |
| `frontend/directory_structure.md` | フロントエンドのディレクトリ構成 |
| `frontend/routing_design.md`      | ルーティング設計                 |
| `frontend/state_management.md`    | Zustandによる状態管理設計        |
| `frontend/component_design.md`    | コンポーネント設計               |
| `frontend/ui_policy.md`           | UI方針・画面表示方針             |

---

## 5. 画面構成

| 画面              | 概要                   |
| ----------------- | ---------------------- |
| LoginPage         | ログイン画面           |
| DashboardPage     | ロール別ダッシュボード |
| ProjectDetailPage | 案件詳細画面           |
| ApprovalPage      | 承認画面               |
| BudgetListPage    | 予算一覧画面           |
| TaskFormPage      | タスク登録・編集画面   |

---

## 6. 状態管理方針

状態管理には Zustand を使用する。

主なStoreは以下とする。

| Store             | 役割                       |
| ----------------- | -------------------------- |
| authStore         | 認証状態管理               |
| dashboardStore    | ダッシュボード表示状態管理 |
| notificationStore | 通知状態管理               |

詳細は `frontend/state_management.md` を参照する。

---

## 7. API通信方針

API通信は `src/utils/apiClient.ts` に集約する。

### 方針

- fetch を使用する
- Authorization Header を共通付与する
- 401発生時はログイン画面へ遷移する
- エラーレスポンスを共通処理する
- APIごとの処理は `src/api/` 配下に分離する

---

## 8. ロール別表示制御

フロントエンドでは表示制御を行うが、最終的な権限制御はAPI側で行う。

### 方針

- メニュー表示はロールに応じて切り替える
- 画面遷移もロールに応じて制御する
- APIアクセス制御はバックエンドで必ず実施する
- フロントエンド制御のみを信頼しない

---

## 9. 第1段階方針

第1段階では、既存Vue版の画面構成・操作導線・API連携を維持する。

変更しない内容

- 画面構成
- URL構成
- ロール別表示
- API連携
- 通知UI
- 案件申請Drawer
- ガントチャート表示

---

## 10. 今後の改善候補

移植完了後、以下を検討する。

- React Query の導入
- React Hook Form の導入
- Zod によるバリデーション
- コンポーネント分割の最適化
- カスタムHooksの整理
- 状態管理の見直し
- UIデザイン改善
- レスポンシブ対応強化
- テストコード追加
- Storybook導入

---

## 11. まとめ

第1段階では、既存Vue版の画面構成・操作導線・API連携を維持し、React + TypeScript で同等の機能を再現する。

Reactらしい設計改善は、移植完了後の第2段階で実施する。

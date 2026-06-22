# development_plan.md

# re_quest1 開発計画書

---

# 1. 概要

本ドキュメントは、`re_quest1` の開発計画および進捗管理を目的とする。

第1段階では既存 `quest_1` の機能・画面・API・DB設計を維持したまま、

- React + TypeScript
- ASP.NET Core Web API
- Entity Framework Core

へ移植する。

---

# 2. 開発方針

## Phase 1

既存PoCの完全移植

### 目標

既存の Vue + FastAPI 版と同等の操作が可能な状態にする。

### 制約

以下は変更しない。

- 画面構成
- URL構成
- API仕様
- DB構造
- ロール設計
- ステータス設計
- 通知仕様

---

## Phase 2

移植完了後の改善

対象

- UI改善
- 認証改善
- テスト強化
- CI/CD
- パフォーマンス改善

---

# 3. マイルストーン

| No  | マイルストーン         | 状態 |
| --- | ---------------------- | ---- |
| M1  | 設計書作成完了         | ☐    |
| M2  | 開発環境構築完了       | ☐    |
| M3  | DB構築完了             | ☐    |
| M4  | 認証機能移植完了       | ☐    |
| M5  | 案件管理移植完了       | ☐    |
| M6  | 承認機能移植完了       | ☐    |
| M7  | タスク管理移植完了     | ☐    |
| M8  | 予算管理移植完了       | ☐    |
| M9  | 通知機能移植完了       | ☐    |
| M10 | ダッシュボード移植完了 | ☐    |
| M11 | 権限制御移植完了       | ☐    |
| M12 | 総合テスト完了         | ☐    |
| M13 | Phase1完了             | ☐    |

---

# 4. フェーズ別作業

---

# Phase 0

## 設計

### ドキュメント

- [ ] migration_policy.md
- [ ] feature_list.md
- [ ] README.md
- [ ] system_design.md
- [ ] database_design.md
- [ ] api_design.md
- [ ] frontend_design.md
- [ ] backend_design.md
- [ ] development_plan.md

---

# Phase 1

## 開発環境構築

### Backend

- [ ] ASP.NET Core Web API作成
- [ ] EF Core導入
- [ ] MySQL接続
- [ ] Migration実行

### Frontend

- [ ] React作成
- [ ] React Router導入
- [ ] Zustand導入
- [ ] MUI導入
- [ ] fetch共通化

### Docker

- [ ] Backendコンテナ
- [ ] Frontendコンテナ
- [ ] MySQLコンテナ
- [ ] docker-compose作成

---

# Phase 2

## DB移植

### departments

- [ ] Entity作成
- [ ] Migration確認

### users

- [ ] Entity作成
- [ ] Migration確認

### projects

- [ ] Entity作成
- [ ] Migration確認

### project_budgets

- [ ] Entity作成
- [ ] Migration確認

### tasks

- [ ] Entity作成
- [ ] Migration確認

### worklogs

- [ ] Entity作成
- [ ] Migration確認

### expenses

- [ ] Entity作成
- [ ] Migration確認

### notifications

- [ ] Entity作成
- [ ] Migration確認

---

# Phase 3

## 認証機能

### Backend

- [ ] UserRepository
- [ ] AuthService
- [ ] AuthController
- [ ] JWT設定

### Frontend

- [ ] LoginPage
- [ ] AuthStore
- [ ] ProtectedRoute

### 動作確認

- [ ] ログイン成功
- [ ] ログイン失敗
- [ ] 認証ガード

---

# Phase 4

## 案件管理

### Backend

- [ ] ProjectRepository
- [ ] ProjectService
- [ ] ProjectController

### Frontend

- [ ] ProjectTable
- [ ] ProjectDetail
- [ ] ProjectCreateDrawer

### 動作確認

- [ ] 一覧取得
- [ ] 詳細取得
- [ ] 登録
- [ ] 更新

---

# Phase 5

## 承認機能

### Backend

- [ ] ApprovalService
- [ ] ApprovalController

### Frontend

- [ ] ApprovalPage
- [ ] ApprovalDialog

### 動作確認

- [ ] 部門承認
- [ ] 本部承認
- [ ] 却下

---

# Phase 6

## タスク管理

### Backend

- [ ] TaskRepository
- [ ] TaskService
- [ ] TaskController

### Frontend

- [ ] TaskTable
- [ ] TaskForm
- [ ] GanttChart

### 動作確認

- [ ] タスク作成
- [ ] タスク更新
- [ ] ガント表示

---

# Phase 7

## 予算管理

### Backend

- [ ] BudgetRepository
- [ ] BudgetService
- [ ] BudgetController

### Frontend

- [ ] BudgetSummary
- [ ] BudgetTable
- [ ] WorklogForm
- [ ] ExpenseForm

### 動作確認

- [ ] 工数登録
- [ ] 経費登録
- [ ] 消化率表示

---

# Phase 8

## 通知機能

### Backend

- [ ] NotificationRepository
- [ ] NotificationService
- [ ] WebSocket実装

### Frontend

- [ ] NotificationPopover
- [ ] NotificationDrawer
- [ ] NotificationDialog

### 動作確認

- [ ] 通知表示
- [ ] 既読
- [ ] 全件既読
- [ ] リアルタイム通知

---

# Phase 9

## ダッシュボード

### Backend

- [ ] DashboardService
- [ ] DashboardController

### Frontend

- [ ] ApplicantDashboard
- [ ] DeptManagerDashboard
- [ ] HqManagerDashboard
- [ ] TaskMemberDashboard

### 動作確認

- [ ] KPI表示
- [ ] フィルタ切替
- [ ] アラート表示

---

# Phase 10

## 権限制御

### Backend

- [ ] PermissionService
- [ ] Role制御
- [ ] Department制御
- [ ] IDOR対策

### テスト

- [ ] APPLICANT
- [ ] DEPT_MANAGER
- [ ] HQ_MANAGER
- [ ] TASK_MEMBER

---

# Phase 11

## 総合テスト

### 認証

- [ ] Login

### 案件

- [ ] CRUD

### 承認

- [ ] Approve
- [ ] Reject

### タスク

- [ ] CRUD

### 予算

- [ ] CRUD

### 通知

- [ ] Notification

### 権限制御

- [ ] Role
- [ ] Department
- [ ] IDOR

---

# 5. 完了条件

以下を満たした場合、Phase1完了とする。

- [ ] 全主要機能が動作する
- [ ] ロール別表示が動作する
- [ ] 権限制御が動作する
- [ ] API仕様が一致する
- [ ] DB構造が一致する
- [ ] feature_list.md が完了状態になっている

---

# 6. 改善候補管理

移植中に見つかった改善案はここでは実装しない。

別途管理する。

候補例

- React Query導入
- FluentValidation導入
- Cookie認証
- Refresh Token
- Serilog
- OpenTelemetry
- CQRS
- MediatR

---

# 7. 備考

第1段階では改善よりも再現を優先する。

既存PoCとの差分を最小限に抑えながら、
React + ASP.NET Core への移植を完了させる。

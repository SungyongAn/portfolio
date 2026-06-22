# dashboard_api.md

# ダッシュボードAPI設計

## 1. 概要

本ドキュメントは、`re_quest1` におけるダッシュボードAPIを定義する。

ダッシュボードAPIでは、ログインユーザーのロールに応じて、
表示対象となる集計情報・案件情報・タスク情報を返却する。

第1段階では、既存 `quest_1` のダッシュボード表示仕様を維持する。

---

## 2. ダッシュボード情報取得API

## Endpoint

```text
GET /api/dashboard
```

---

## 認証

必要。

```text
Authorization: Bearer <token>
```

---

## Request

なし。

---

## Response

```json
{
  "role": "HQ_MANAGER",
  "summary": {}
}
```

---

## Response項目

| 項目    | 型     | 概要                     |
| ------- | ------ | ------------------------ |
| role    | string | ログインユーザーのロール |
| summary | object | ロール別サマリ情報       |

---

## 3. ロール別レスポンス方針

## APPLICANT

申請者向けの情報を返却する。

### 主な内容

- 自分が申請した案件数
- 承認待ち案件数
- 進行中案件数
- 完了案件数
- 自分が申請した案件一覧

---

## DEPT_MANAGER

部門管理者向けの情報を返却する。

### 主な内容

- 自部門案件数
- 部門承認待ち案件数
- 進行中案件数
- リスク案件数
- 自部門案件一覧

---

## HQ_MANAGER

本部管理者向けの情報を返却する。

### 主な内容

- 全案件数
- 全体予算
- 全体実績
- 本部承認待ち案件数
- 部門別集計
- 全社リスク案件一覧

---

## TASK_MEMBER

担当者向けの情報を返却する。

### 主な内容

- 自分のタスク数
- 本日のタスク
- 期限超過タスク
- 担当案件一覧

---

## 4. 処理フロー

```text
Dashboard Request
 ↓

DashboardController
 ↓

Current User取得
 ↓

DashboardService
 ↓

Role判定
 ↓

Role別集計
 ↓

Dashboard Response
```

---

## 5. Controller

```text
DashboardController
```

---

## 6. Service

```text
DashboardService
```

---

## 7. Repository

利用想定

```text
ProjectRepository
TaskRepository
BudgetRepository
NotificationRepository
```

---

## 8. 認可方針

ダッシュボードAPIは、ログインユーザーのロールに応じて取得範囲を制御する。

| ロール       | 取得範囲                   |
| ------------ | -------------------------- |
| APPLICANT    | 自分が申請した案件         |
| DEPT_MANAGER | 自部門案件                 |
| HQ_MANAGER   | 全案件                     |
| TASK_MEMBER  | 自分が担当するタスク・案件 |

---

## 9. エラーレスポンス

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

## 10. フロントエンド連携

フロントエンドでは、ログイン後にダッシュボードAPIを呼び出す。

```text
GET /api/dashboard
```

取得した `role` に応じて表示コンポーネントを切り替える。

---

## 11. React側表示コンポーネント

| ロール       | コンポーネント       |
| ------------ | -------------------- |
| APPLICANT    | ApplicantDashboard   |
| DEPT_MANAGER | DeptManagerDashboard |
| HQ_MANAGER   | HqManagerDashboard   |
| TASK_MEMBER  | TaskMemberDashboard  |

---

## 12. 第1段階方針

第1段階では既存PoCの仕様を維持する。

変更しない内容

- APIパス
- ロール別表示方針
- 集計対象
- レスポンスの基本構造
- 権限制御

---

## 13. 今後の改善候補

移植完了後、以下を検討する。

- レスポンス型の整理
- ロール別API分離
- 集計SQLの最適化
- キャッシュ導入
- ダッシュボード表示項目の追加
- KPI定義の見直し

---

## 14. まとめ

ダッシュボードAPIでは、ログインユーザーのロールに応じた情報を返却する。

第1段階では既存PoCの表示内容を維持し、
React + ASP.NET Core 版で同等のダッシュボード表示を再現する。

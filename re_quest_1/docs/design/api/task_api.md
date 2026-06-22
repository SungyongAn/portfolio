# task_api.md

# タスクAPI設計

## 1. 概要

本ドキュメントは、`re_quest1` におけるタスク管理APIを定義する。

タスクAPIでは、案件に紐づくタスクの作成・取得・更新・削除を行う。

第1段階では、既存 `quest_1` のタスク管理仕様を維持し、
React + ASP.NET Core 版で同等の挙動を再現する。

---

## 2. 対象機能

- タスク一覧取得
- タスク作成
- タスク更新
- タスク削除
- タスク進捗更新
- タスクステータス変更
- ガントチャート表示用データ取得

---

## 3. タスク一覧取得

## Endpoint

```text
GET /api/projects/{id}/tasks
```

---

## Path Parameter

| 項目 | 型   | 説明   |
| ---- | ---- | ------ |
| id   | long | 案件ID |

---

## Response

```json
[
  {
    "id": 1,
    "project_id": 1,
    "assignee_id": 3,
    "title": "要件整理",
    "description": "要件定義内容を整理する",
    "status": "IN_PROGRESS",
    "progress": 50,
    "start_date": "2026-05-01",
    "due_date": "2026-05-10"
  }
]
```

---

# 4. タスク作成

## Endpoint

```text
POST /api/projects/{id}/tasks
```

---

## Path Parameter

| 項目 | 型   | 説明   |
| ---- | ---- | ------ |
| id   | long | 案件ID |

---

## Request

```json
{
  "title": "設計書作成",
  "description": "基本設計書を作成する",
  "assignee_id": 3,
  "status": "TODO",
  "progress": 0,
  "start_date": "2026-05-01",
  "due_date": "2026-05-10"
}
```

---

## Response

```json
{
  "id": 1
}
```

---

# 5. タスク更新

## Endpoint

```text
PUT /api/tasks/{id}
```

---

## Path Parameter

| 項目 | 型   | 説明     |
| ---- | ---- | -------- |
| id   | long | タスクID |

---

## Request

```json
{
  "title": "設計書作成",
  "description": "基本設計書を作成する",
  "assignee_id": 3,
  "status": "IN_PROGRESS",
  "progress": 40,
  "start_date": "2026-05-01",
  "due_date": "2026-05-10"
}
```

---

## Response

```json
{
  "success": true
}
```

---

# 6. タスク削除

## Endpoint

```text
DELETE /api/tasks/{id}
```

---

## Path Parameter

| 項目 | 型   | 説明     |
| ---- | ---- | -------- |
| id   | long | タスクID |

---

## Response

```json
{
  "success": true
}
```

---

# 7. タスクステータス

| 値          | 説明       |
| ----------- | ---------- |
| TODO        | 未着手     |
| IN_PROGRESS | 進行中     |
| IN_REVIEW   | レビュー中 |
| DONE        | 完了       |

---

# 8. ステータス遷移

```text
TODO
 ↓

IN_PROGRESS
 ↓

IN_REVIEW
 ↓

DONE
```

---

# 9. バリデーション

## タスク作成・更新

| 項目       | 条件                 |
| ---------- | -------------------- |
| title      | 必須                 |
| progress   | 0〜100               |
| status     | TaskStatusのいずれか |
| start_date | due_date以前         |
| due_date   | start_date以降       |

---

# 10. 認可方針

## APPLICANT

- 自分が申請した案件のタスクを参照可能
- 原則としてタスク更新は不可

---

## DEPT_MANAGER

- 自部門案件のタスクを参照可能
- 自部門案件のタスクを管理可能

---

## HQ_MANAGER

- 全案件のタスクを参照可能
- 必要に応じて全案件のタスクを管理可能

---

## TASK_MEMBER

- 自分が担当するタスクを参照可能
- 自分が担当するタスクを更新可能
- 他担当者のタスク更新は不可

---

# 11. IDOR対策

タスク操作時は、必ず対象タスクが属する案件へのアクセス権限を確認する。

```text
Task取得
 ↓

Project取得
 ↓

PermissionService
 ↓

権限確認
 ↓

許可
または
403
```

---

# 12. Controller

```text
TaskController
```

---

# 13. Service

```text
TaskService
PermissionService
```

---

# 14. Repository

```text
TaskRepository
ProjectRepository
```

---

# 15. ガントチャート連携

タスク一覧APIのレスポンスを利用し、フロントエンド側でガントチャートを表示する。

## 使用項目

| 項目        | 用途             |
| ----------- | ---------------- |
| title       | タスク名         |
| start_date  | ガント開始位置   |
| due_date    | ガント終了位置   |
| progress    | 進捗表示         |
| status      | 表示色・状態判定 |
| assignee_id | 担当者表示       |

---

# 16. 通知連携

タスク作成・担当者変更時に通知を発行する。

## 通知種別

```text
TASK_ASSIGNED
```

---

# 17. エラーレスポンス

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
  "detail": "Task not found"
}
```

Status:

```text
404 Not Found
```

---

## バリデーションエラー

```json
{
  "detail": "Validation Error"
}
```

Status:

```text
422 Validation Error
```

---

# 18. 第1段階方針

既存PoCのタスク管理仕様を維持する。

変更しない内容

- APIパス
- タスクステータス
- 進捗率の扱い
- ガント表示用データ
- 権限制御
- IDOR対策

---

# 19. 今後の改善候補

移植完了後、以下を検討する。

- タスク依存関係の追加
- タスク粒度ルールの追加
- タスク履歴管理
- 進捗コメント
- 担当者変更履歴
- ガントチャート操作性改善

---

# 20. まとめ

タスクAPIでは、案件に紐づくタスクの管理を行う。

第1段階では既存PoCの仕様を維持し、
React + ASP.NET Core 版で同等のタスク管理・ガントチャート表示を再現する。

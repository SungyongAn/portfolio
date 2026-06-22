# project_api.md

# 案件API設計

## 1. 概要

本ドキュメントは、案件管理に関するAPIを定義する。

対象機能

- 案件一覧
- 案件詳細
- 案件作成
- 案件更新
- 案件削除
- 承認
- 却下
- 案件着手
- 案件完了

---

# 2. 案件一覧取得

## Endpoint

```text
GET /api/projects
```

---

## Query Parameter

| 項目          | 型     | 必須 | 説明               |
| ------------- | ------ | ---- | ------------------ |
| page          | int    | ×    | ページ番号         |
| limit         | int    | ×    | 件数               |
| status        | string | ×    | ステータス絞り込み |
| keyword       | string | ×    | キーワード検索     |
| department_id | long   | ×    | 部門絞り込み       |
| sort_by       | string | ×    | ソート項目         |

---

## Response

```json
{
  "items": [],
  "total": 100
}
```

---

# 3. 案件詳細取得

## Endpoint

```text
GET /api/projects/{id}
```

---

## Path Parameter

| 項目 | 型   |
| ---- | ---- |
| id   | long |

---

## Response

```json
{
  "id": 1,
  "name": "案件A",
  "status": "IN_PROGRESS"
}
```

---

# 4. 案件作成

## Endpoint

```text
POST /api/projects
```

---

## Request

```json
{
  "name": "案件A",
  "description": "案件説明",
  "department_id": 1,
  "budget_amount": 1000000,
  "planned_months": 6
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

# 5. 案件更新

## Endpoint

```text
PUT /api/projects/{id}
```

---

## Request

```json
{
  "name": "案件A更新",
  "description": "更新内容"
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

# 6. 案件削除

## Endpoint

```text
DELETE /api/projects/{id}
```

---

## Response

```json
{
  "success": true
}
```

---

# 7. 部門承認

## Endpoint

```text
POST /api/projects/{id}/approve-dept
```

---

## Request

```json
{
  "comment": "承認します"
}
```

---

## 処理内容

```text
PENDING_DEPT
 ↓
PENDING_HQ
```

---

# 8. 本部承認

## Endpoint

```text
POST /api/projects/{id}/approve-hq
```

---

## Request

```json
{
  "comment": "本部承認"
}
```

---

## 処理内容

```text
PENDING_HQ
 ↓
APPROVED
```

---

# 9. 却下

## Endpoint

```text
POST /api/projects/{id}/reject
```

---

## Request

```json
{
  "comment": "予算超過のため却下"
}
```

---

## 処理内容

```text
PENDING_DEPT
または
PENDING_HQ

 ↓

REJECTED
```

---

# 10. 案件着手

## Endpoint

```text
POST /api/projects/{id}/start
```

---

## 処理内容

```text
APPROVED
 ↓
IN_PROGRESS
```

---

# 11. 案件完了

## Endpoint

```text
POST /api/projects/{id}/complete
```

---

## 処理内容

```text
IN_PROGRESS
 ↓
COMPLETED
```

---

# 12. 案件ステータス

| 値           | 説明         |
| ------------ | ------------ |
| DRAFT        | 下書き       |
| PENDING_DEPT | 部門承認待ち |
| PENDING_HQ   | 本部承認待ち |
| APPROVED     | 承認済み     |
| IN_PROGRESS  | 進行中       |
| COMPLETED    | 完了         |
| REJECTED     | 却下         |

---

# 13. 認可方針

## APPLICANT

可能

- 自案件作成
- 自案件参照

不可

- 承認
- 却下

---

## DEPT_MANAGER

可能

- 自部門案件参照
- 部門承認

---

## HQ_MANAGER

可能

- 全案件参照
- 本部承認

---

## TASK_MEMBER

可能

- 担当案件参照

不可

- 承認
- 案件編集

---

# 14. IDOR対策

案件取得時は必ず権限確認を行う。

```text
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

# 15. Controller

```text
ProjectController
ApprovalController
```

---

# 16. Service

```text
ProjectService
ApprovalService
PermissionService
```

---

# 17. 主な通知発行

案件API実行時に通知を発行する。

| イベント | 通知              |
| -------- | ----------------- |
| 承認依頼 | APPROVAL_REQUEST  |
| 部門承認 | APPROVED          |
| 本部承認 | APPROVED          |
| 却下     | REJECTED          |
| 着手     | PROJECT_STARTED   |
| 完了     | PROJECT_COMPLETED |

---

# 18. エラーレスポンス

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
  "detail": "Project not found"
}
```

Status:

```text
404 Not Found
```

---

# 19. 第1段階方針

既存PoCの案件管理仕様を維持する。

変更しない内容

- ステータス遷移
- 承認フロー
- APIパス
- 権限制御
- 通知仕様

---

# 20. まとめ

案件APIは本システムの中心機能である。

第1段階では既存PoCの案件管理・承認フロー・通知連携を維持し、
ASP.NET Coreで同等の動作を再現する。

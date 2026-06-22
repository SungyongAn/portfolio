# statuses.md

# ステータス設計

## 1. 概要

本ドキュメントは、`re_quest1` における案件ステータスおよびタスクステータスを定義する。

第1段階では、既存 `quest_1` のステータス設計を維持する。

---

# 2. 案件ステータス

## 一覧

| ステータス   | 説明         |
| ------------ | ------------ |
| DRAFT        | 下書き       |
| PENDING_DEPT | 部門承認待ち |
| PENDING_HQ   | 本部承認待ち |
| APPROVED     | 承認済み     |
| IN_PROGRESS  | 進行中       |
| COMPLETED    | 完了         |
| REJECTED     | 却下         |

---

# 3. 案件ステータス遷移

```text
DRAFT
 ↓

PENDING_DEPT
 ↓

PENDING_HQ
 ↓

APPROVED
 ↓

IN_PROGRESS
 ↓

COMPLETED
```

---

## 却下パターン

```text
PENDING_DEPT
 ↓

REJECTED
```

```text
PENDING_HQ
 ↓

REJECTED
```

---

# 4. ステータス別説明

## DRAFT

### 状態

申請前の下書き状態。

### 操作可能

- 編集
- 削除
- 申請

---

## PENDING_DEPT

### 状態

部門管理者の承認待ち。

### 操作可能

- 承認
- 却下

---

## PENDING_HQ

### 状態

本部管理者の承認待ち。

### 操作可能

- 承認
- 却下

---

## APPROVED

### 状態

承認済み。

### 操作可能

- 案件着手

---

## IN_PROGRESS

### 状態

案件進行中。

### 操作可能

- タスク管理
- 工数管理
- 経費管理
- 完了

---

## COMPLETED

### 状態

案件完了。

### 操作可能

- 参照のみ

---

## REJECTED

### 状態

却下済み。

### 操作可能

- 参照のみ

---

# 5. タスクステータス

## 一覧

| ステータス  | 説明       |
| ----------- | ---------- |
| TODO        | 未着手     |
| IN_PROGRESS | 進行中     |
| IN_REVIEW   | レビュー中 |
| DONE        | 完了       |

---

# 6. タスクステータス遷移

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

# 7. タスクステータス説明

## TODO

### 状態

未着手。

### 進捗率

```text
0%
```

---

## IN_PROGRESS

### 状態

作業中。

### 進捗率

```text
1〜99%
```

---

## IN_REVIEW

### 状態

レビュー待ち。

### 進捗率

```text
90〜99%
```

---

## DONE

### 状態

完了。

### 進捗率

```text
100%
```

---

# 8. タスク担当者制御

TASK_MEMBERは、自分の担当タスクのみ更新可能とする。

---

## 制御内容

```text
task.assignee_id
==
current_user.id
```

---

## 違反時

```text
403 Forbidden
```

---

# 9. 通知との連携

案件ステータス変更時は通知を発行する。

---

## 発行例

| イベント | 通知              |
| -------- | ----------------- |
| 案件申請 | APPROVAL_REQUEST  |
| 部門承認 | APPROVAL_REQUEST  |
| 本部承認 | APPROVED          |
| 却下     | REJECTED          |
| 案件着手 | PROJECT_STARTED   |
| 案件完了 | PROJECT_COMPLETED |

---

# 10. ダッシュボードとの連携

ステータスごとに集計を行う。

---

## 例

### APPLICANT

- 承認待ち案件数
- 進行中案件数
- 完了案件数

---

### DEPT_MANAGER

- 部門承認待ち件数
- リスク案件数

---

### HQ_MANAGER

- 本部承認待ち件数
- 全案件数

---

### TASK_MEMBER

- TODO件数
- IN_PROGRESS件数
- IN_REVIEW件数
- DONE件数

---

# 11. DB保存方針

第1段階では文字列として保存する。

---

## ProjectStatus

```text
DRAFT
PENDING_DEPT
PENDING_HQ
APPROVED
IN_PROGRESS
COMPLETED
REJECTED
```

---

## TaskStatus

```text
TODO
IN_PROGRESS
IN_REVIEW
DONE
```

---

# 12. C#実装方針

第1段階では文字列維持とする。

将来的にEnum化を検討する。

---

## 候補

```csharp
public enum ProjectStatus
{
    Draft,
    PendingDept,
    PendingHq,
    Approved,
    InProgress,
    Completed,
    Rejected
}
```

---

# 13. 第1段階方針

既存PoCのステータス設計を維持する。

変更しない内容

- ステータス値
- ステータス遷移
- 通知連携
- 集計条件

---

# 14. 今後の改善候補

移植完了後に検討する。

- Enum正式導入
- ステータス履歴管理
- 承認履歴管理
- ワークフローエンジン導入
- 状態遷移制御の共通化

---

# 15. まとめ

本システムでは、

```text
ProjectStatus
TaskStatus
```

の2種類のステータスを利用する。

第1段階では既存PoCの状態遷移を維持し、React + ASP.NET Core版へ移植する。

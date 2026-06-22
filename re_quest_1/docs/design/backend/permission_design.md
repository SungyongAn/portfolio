# permission_design.md

# 認可・IDOR対策設計

## 1. 概要

本ドキュメントは、`re_quest1` における認可設計およびIDOR対策を定義する。

本システムでは、フロントエンドによる表示制御だけでなく、API側で必ず認可判定を実施する。

第1段階では、既存 `quest_1` で実装した PermissionService を維持する。

---

# 2. 目的

以下の問題を防ぐことを目的とする。

---

## 不正アクセス

例

```text
/projects/1
 ↓

/projects/999
```

---

## 他部門データ参照

例

```text
プロダクト開発部
 ↓

カスタマーソリューション部案件参照
```

---

## 他担当者タスク更新

例

```text
自分のタスク
 ↓

他人のタスクID指定
```

---

# 3. PermissionService

認可処理は PermissionService に集約する。

---

## 責務

```text id="qjv1kz"
案件アクセス判定
タスクアクセス判定
予算アクセス判定
通知アクセス判定
部門判定
ロール判定
```

---

# 4. ロール一覧

| ロール       | 説明       |
| ------------ | ---------- |
| APPLICANT    | 申請者     |
| DEPT_MANAGER | 部門管理者 |
| HQ_MANAGER   | 本部管理者 |
| TASK_MEMBER  | 担当者     |

---

# 5. 案件アクセス制御

## APPLICANT

許可条件

```text id="ldo4eg"
project.applicant_id
==
current_user.id
```

---

## DEPT_MANAGER

許可条件

```text id="lp8t5x"
project.department_id
==
current_user.department_id
```

---

## HQ_MANAGER

許可条件

```text id="xqjlwm"
全案件許可
```

---

## TASK_MEMBER

許可条件

```text id="l1xgt1"
担当タスクが存在する
```

---

# 6. タスクアクセス制御

## TASK_MEMBER

許可条件

```text id="zjlwmz"
task.assignee_id
==
current_user.id
```

---

## 違反時

```text id="wnyivh"
403 Forbidden
```

---

# 7. 予算アクセス制御

予算単体ではなく案件経由で判定する。

---

## 判定

```text id="4hyvhh"
Budget
 ↓

Project
 ↓

PermissionService
```

---

# 8. 通知アクセス制御

通知は本人のみ参照可能。

---

## 判定

```text id="4txh5i"
notification.user_id
==
current_user.id
```

---

# 9. 部門制御

部門管理者は自部門のみアクセス可能。

---

## 判定

```text id="ck7a9m"
project.department_id
==
current_user.department_id
```

---

# 10. IDOR対策対象

以下は必ずPermissionServiceを通す。

| 対象         | 必須 |
| ------------ | ---- |
| Project      | ○    |
| Task         | ○    |
| Budget       | ○    |
| Worklog      | ○    |
| Expense      | ○    |
| Notification | ○    |

---

# 11. IDOR対策フロー

```text id="8zc91f"
Request
 ↓

Controller
 ↓

Service
 ↓

PermissionService
 ↓

対象確認
 ↓

許可
または
403
```

---

# 12. 実装例

## Project

```csharp
PermissionService.CheckProjectAccess(
    currentUser,
    project
);
```

---

## Task

```csharp
PermissionService.CheckTaskAccess(
    currentUser,
    task
);
```

---

## Notification

```csharp
PermissionService.CheckNotificationAccess(
    currentUser,
    notification
);
```

---

# 13. フロントエンド制御との違い

## フロントエンド

目的

```text id="u5g8gi"
UX向上
```

---

## バックエンド

目的

```text id="n6ph1j"
セキュリティ
```

---

## 重要

```text id="8n2up0"
フロントエンド制御だけを信用しない
```

---

# 14. 例外処理

権限不足時

```text id="u4rwbo"
ForbiddenException
```

---

## レスポンス

```json id="b91r9s"
{
  "detail": "Forbidden"
}
```

---

## Status

```text id="fq0jzn"
403 Forbidden
```

---

# 15. テスト方針

認可テストを実施する。

---

## 確認項目

```text id="qwd0qa"
他部門案件参照不可
他部門予算参照不可
他担当者タスク更新不可
他人通知参照不可
```

---

# 16. 第1段階方針

既存PoCの認可方式を維持する。

変更しない内容

- PermissionService
- ロール制御
- 部門制御
- IDOR対策
- 403レスポンス

---

# 17. 今後の改善候補

移植完了後に検討する。

- Policy Based Authorization
- Resource Based Authorization
- 権限マトリクス管理
- カスタムAuthorize属性
- 動的権限制御

---

# 18. まとめ

認可処理は PermissionService に集約する。

第1段階では既存PoCで実装したロール制御・部門制御・IDOR対策を維持し、ASP.NET Core版へ移植する。

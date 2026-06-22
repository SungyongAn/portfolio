# service_design.md

# Service設計

## 1. 概要

本ドキュメントは、`re_quest1` の ASP.NET Core Web API における Service 層の設計を定義する。

Serviceは本システムの業務ロジックを担当する。

Controllerから呼び出され、Repositoryや他Serviceを利用して処理を実行する。

---

# 2. Service層の責務

## 行うこと

- 業務ロジック
- ステータス変更
- 権限判定呼出
- KPI計算
- 通知生成
- トランザクション管理
- DTO生成

---

## 行わないこと

- HTTP処理
- SQL実行
- Entity Framework直接操作
- UI制御

---

# 3. Service一覧

```text
Services/
├─ AuthService.cs
├─ DashboardService.cs
├─ ProjectService.cs
├─ ApprovalService.cs
├─ TaskService.cs
├─ BudgetService.cs
├─ WorklogService.cs
├─ ExpenseService.cs
├─ NotificationService.cs
├─ AlertService.cs
└─ PermissionService.cs
```

---

# 4. AuthService

## 役割

認証処理を担当する。

---

## 主な処理

```text
ログイン
JWT生成
パスワード検証
```

---

## 利用Repository

```text
UserRepository
```

---

# 5. DashboardService

## 役割

ダッシュボード集計を担当する。

---

## 主な処理

```text
ロール判定
KPI集計
案件集計
リスク案件抽出
```

---

## 利用Repository

```text
ProjectRepository
TaskRepository
BudgetRepository
```

---

## 利用Service

```text
AlertService
```

---

# 6. ProjectService

## 役割

案件管理を担当する。

---

## 主な処理

```text
案件作成
案件更新
案件削除
案件取得
案件検索
```

---

## 利用Repository

```text
ProjectRepository
```

---

## 利用Service

```text
PermissionService
NotificationService
```

---

# 7. ApprovalService

## 役割

承認処理を担当する。

---

## 主な処理

```text
部門承認
本部承認
却下
案件着手
案件完了
```

---

## 利用Repository

```text
ProjectRepository
```

---

## 利用Service

```text
PermissionService
NotificationService
```

---

# 8. TaskService

## 役割

タスク管理を担当する。

---

## 主な処理

```text
タスク作成
タスク更新
タスク削除
進捗更新
```

---

## 利用Repository

```text
TaskRepository
ProjectRepository
```

---

## 利用Service

```text
PermissionService
NotificationService
```

---

# 9. BudgetService

## 役割

予算管理を担当する。

---

## 主な処理

```text
予算取得
予算更新
消化率計算
```

---

## 利用Repository

```text
BudgetRepository
ProjectRepository
```

---

## 利用Service

```text
PermissionService
```

---

# 10. WorklogService

## 役割

工数管理を担当する。

---

## 主な処理

```text
工数登録
工数更新
工数削除
実績人月集計
```

---

## 利用Repository

```text
WorklogRepository
BudgetRepository
```

---

# 11. ExpenseService

## 役割

経費管理を担当する。

---

## 主な処理

```text
経費登録
経費更新
経費削除
経費集計
```

---

## 利用Repository

```text
ExpenseRepository
BudgetRepository
```

---

# 12. NotificationService

## 役割

通知管理を担当する。

---

## 主な処理

```text
通知作成
通知取得
既読処理
全件既読
WebSocket送信
```

---

## 利用Repository

```text
NotificationRepository
```

---

# 13. AlertService

## 役割

アラート判定を担当する。

---

## 主な処理

```text
SPI計算
CPI計算
Warning判定
Danger判定
```

---

## 判定対象

```text
進捗率
経過率
予算消化率
期限超過タスク
```

---

# 14. PermissionService

## 役割

権限制御を担当する。

---

## 主な処理

```text
案件アクセス判定
タスクアクセス判定
予算アクセス判定
通知アクセス判定
```

---

## 利用箇所

```text
ProjectService
TaskService
BudgetService
NotificationService
ApprovalService
```

---

# 15. Service間依存

```text
DashboardService
 ↓
AlertService

ProjectService
 ↓
NotificationService

TaskService
 ↓
NotificationService

ApprovalService
 ↓
NotificationService

全Service
 ↓
PermissionService
```

---

# 16. トランザクション方針

複数テーブル更新時はトランザクションを利用する。

---

## 例

```text
案件承認
 ↓

案件更新
 +
通知作成
```

---

## 例

```text
工数登録
 ↓

Worklog登録
 +
Budget再計算
```

---

# 17. 例外処理方針

Serviceで業務例外を発生させる。

---

## 例

```text
NotFoundException
ForbiddenException
ValidationException
BusinessException
```

---

## Controller

例外を捕捉しない。

---

## Middleware

共通変換する。

```json
{
  "detail": "Error Message"
}
```

---

# 18. FastAPI版との対応

| FastAPI                 | ASP.NET Core        |
| ----------------------- | ------------------- |
| auth_service.py         | AuthService         |
| project_service.py      | ProjectService      |
| dashboard_service.py    | DashboardService    |
| permission_service.py   | PermissionService   |
| notification_service.py | NotificationService |

---

# 19. 第1段階方針

既存PoCのService構成を維持する。

変更しない内容

- PermissionService
- NotificationService
- DashboardService
- AlertService
- 業務ロジック配置

---

# 20. 今後の改善候補

移植完了後に検討する。

- CQRS
- MediatR
- Domain Service
- UseCase層
- Event駆動通知
- Sagaパターン

---

# 21. まとめ

Service層は本システムの業務ロジックの中心である。

第1段階では既存FastAPI版の責務分離を維持し、業務ロジックをServiceへ集約する。

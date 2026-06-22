# repository_design.md

# Repository設計

## 1. 概要

本ドキュメントは、`re_quest1` の ASP.NET Core Web API における Repository 層の設計を定義する。

RepositoryはDBアクセスを担当し、Entity Framework Core を利用してデータ取得・登録・更新・削除を行う。

---

# 2. Repository層の責務

## 行うこと

- Entity取得
- Entity登録
- Entity更新
- Entity削除
- 条件検索
- 集計用クエリ
- Includeによる関連データ取得

---

## 行わないこと

- 業務判断
- 権限判定
- ステータス遷移判断
- 通知生成
- Response DTO生成

---

# 3. Repository一覧

```text
Repositories/
├─ UserRepository.cs
├─ DepartmentRepository.cs
├─ ProjectRepository.cs
├─ TaskRepository.cs
├─ BudgetRepository.cs
├─ WorklogRepository.cs
├─ ExpenseRepository.cs
└─ NotificationRepository.cs
```

---

# 4. UserRepository

## 役割

ユーザー情報の取得を担当する。

## 主な処理

```text
GetById
GetByEmail
GetByRole
GetByDepartment
```

## 利用Service

```text
AuthService
PermissionService
```

---

# 5. DepartmentRepository

## 役割

部門情報の取得を担当する。

## 主な処理

```text
GetById
GetList
```

## 利用Service

```text
DashboardService
ProjectService
```

---

# 6. ProjectRepository

## 役割

案件情報のDBアクセスを担当する。

## 主な処理

```text
GetById
GetList
GetByDepartment
GetByApplicant
GetByOwner
Create
Update
Delete
```

## 利用Service

```text
ProjectService
ApprovalService
DashboardService
PermissionService
```

---

# 7. TaskRepository

## 役割

タスク情報のDBアクセスを担当する。

## 主な処理

```text
GetById
GetByProjectId
GetByAssigneeId
GetOverdueTasks
Create
Update
Delete
```

## 利用Service

```text
TaskService
DashboardService
AlertService
PermissionService
```

---

# 8. BudgetRepository

## 役割

予算情報のDBアクセスを担当する。

## 主な処理

```text
GetByProjectId
Create
Update
Recalculate
```

## 利用Service

```text
BudgetService
DashboardService
AlertService
```

---

# 9. WorklogRepository

## 役割

工数情報のDBアクセスを担当する。

## 主な処理

```text
GetById
GetByBudgetId
GetByTaskId
Create
Update
Delete
SumActualMonths
```

## 利用Service

```text
WorklogService
BudgetService
DashboardService
```

---

# 10. ExpenseRepository

## 役割

経費情報のDBアクセスを担当する。

## 主な処理

```text
GetById
GetByBudgetId
Create
Update
Delete
SumExpenseCost
```

## 利用Service

```text
ExpenseService
BudgetService
DashboardService
```

---

# 11. NotificationRepository

## 役割

通知情報のDBアクセスを担当する。

## 主な処理

```text
GetById
GetByUserId
GetUnreadCount
Create
MarkAsRead
MarkAllAsRead
```

## 利用Service

```text
NotificationService
DashboardService
```

---

# 12. Query方針

## 一覧取得

一覧取得では、検索条件・ページング・ソートを扱う。

対象例：

```text
ProjectRepository.GetList
TaskRepository.GetByProjectId
NotificationRepository.GetByUserId
```

---

## 集計処理

ダッシュボードやアラート判定で利用する集計は、Repositoryで必要なデータを取得し、Serviceで業務的な判定を行う。

---

# 13. Include方針

関連データが必要な場合のみ `Include` を使用する。

## 例

```csharp
_context.Projects
    .Include(p => p.Department)
    .Include(p => p.Applicant)
    .Include(p => p.ProjectBudget)
```

---

## 注意点

- 不要なIncludeを避ける
- N+1問題に注意する
- 一覧取得では必要最小限のデータにする

---

# 14. Entity Framework Core方針

## DbContext

Repositoryは `AppDbContext` を利用する。

```text
AppDbContext
```

---

## 非同期処理

DBアクセスは原則として非同期で行う。

例：

```csharp
await _context.Projects.ToListAsync();
```

---

# 15. トランザクション方針

複数Repositoryをまたぐ処理はService側でトランザクションを管理する。

## 例

```text
ApprovalService
 ↓

ProjectRepository.Update
NotificationRepository.Create
```

---

# 16. FastAPI版との対応

| FastAPI            | ASP.NET Core |
| ------------------ | ------------ |
| query_service      | Repository   |
| SQLAlchemy Session | AppDbContext |
| models             | Entities     |
| response_service   | DTO変換      |

---

# 17. 第1段階方針

既存PoCのDBアクセス方針を維持する。

変更しない内容

- テーブル構造
- リレーション
- 検索条件
- 集計対象
- 権限判定に必要な取得項目

---

# 18. 今後の改善候補

移植完了後に検討する。

- Repository不要箇所の見直し
- CQRS導入
- Query専用Repository
- ReadModel作成
- パフォーマンス計測
- キャッシュ導入

---

# 19. まとめ

Repository層はDBアクセスに責務を限定する。

第1段階では既存PoCのデータ取得・集計方針を維持し、ASP.NET Core / Entity Framework Core で同等の挙動を再現する。

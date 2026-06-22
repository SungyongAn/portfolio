# controller_design.md

# Controller設計

## 1. 概要

本ドキュメントは、`re_quest1` の ASP.NET Core Web API における Controller 設計を定義する。

ControllerはHTTPリクエストの受付を担当し、業務ロジックはServiceへ委譲する。

---

# 2. Controllerの責務

## 行うこと

- Request受取
- Path Parameter受取
- Query Parameter受取
- Request DTO受取
- Validation結果の確認
- Service呼出
- Response返却

---

## 行わないこと

- SQL実行
- 業務ロジック
- 集計処理
- 権限制御の詳細実装
- Entityの直接返却

---

# 3. Controller一覧

```text
Controllers/
├─ AuthController.cs
├─ DashboardController.cs
├─ ProjectController.cs
├─ ApprovalController.cs
├─ TaskController.cs
├─ BudgetController.cs
├─ WorklogController.cs
├─ ExpenseController.cs
└─ NotificationController.cs
```

---

# 4. AuthController

## 役割

認証処理を担当する。

## Endpoint

```text
POST /api/auth/login
```

## 呼び出しService

```text
AuthService
```

---

# 5. DashboardController

## 役割

ロール別ダッシュボード情報を返却する。

## Endpoint

```text
GET /api/dashboard
```

## 呼び出しService

```text
DashboardService
```

---

# 6. ProjectController

## 役割

案件管理を担当する。

## Endpoint

```text
GET    /api/projects
GET    /api/projects/{id}
POST   /api/projects
PUT    /api/projects/{id}
DELETE /api/projects/{id}
```

## 呼び出しService

```text
ProjectService
```

---

# 7. ApprovalController

## 役割

案件承認・却下を担当する。

## Endpoint

```text
POST /api/projects/{id}/approve-dept
POST /api/projects/{id}/approve-hq
POST /api/projects/{id}/reject
```

## 呼び出しService

```text
ApprovalService
```

---

# 8. TaskController

## 役割

タスク管理を担当する。

## Endpoint

```text
GET    /api/projects/{id}/tasks
POST   /api/projects/{id}/tasks
PUT    /api/tasks/{id}
DELETE /api/tasks/{id}
```

## 呼び出しService

```text
TaskService
```

---

# 9. BudgetController

## 役割

案件予算情報を担当する。

## Endpoint

```text
GET /api/projects/{id}/budget
PUT /api/projects/{id}/budget
```

## 呼び出しService

```text
BudgetService
```

---

# 10. WorklogController

## 役割

工数情報を担当する。

## Endpoint

```text
POST   /api/worklogs
PUT    /api/worklogs/{id}
DELETE /api/worklogs/{id}
```

## 呼び出しService

```text
WorklogService
```

---

# 11. ExpenseController

## 役割

経費情報を担当する。

## Endpoint

```text
POST   /api/expenses
PUT    /api/expenses/{id}
DELETE /api/expenses/{id}
```

## 呼び出しService

```text
ExpenseService
```

---

# 12. NotificationController

## 役割

通知情報を担当する。

## Endpoint

```text
GET  /api/notifications
POST /api/notifications/{id}/read
POST /api/notifications/read-all
```

## 呼び出しService

```text
NotificationService
```

---

# 13. Response方針

## 成功時

```json
{
  "data": {}
}
```

または既存PoCに合わせた形式を返却する。

---

## エラー時

```json
{
  "detail": "Error Message"
}
```

---

# 14. Validation方針

Controllerでは、Request DTOのValidation結果を確認する。

## 例

```text
Required
Range
StringLength
```

詳細な業務バリデーションはServiceで行う。

---

# 15. 認証・認可

## 認証

Controllerには認証必須属性を設定する。

```text
[Authorize]
```

---

## 例外

ログインAPIは認証不要。

```text
[AllowAnonymous]
```

---

## 認可

詳細な権限制御はService内でPermissionServiceを呼び出して行う。

---

# 16. Controller実装方針

## 方針

- Controllerを薄く保つ
- Serviceを呼ぶだけに近い形にする
- Entityを直接返さない
- DTOを使用する
- 例外処理はMiddlewareへ任せる

---

# 17. 第1段階方針

既存FastAPI版のAPI仕様を維持する。

変更しない内容

- URL
- HTTPメソッド
- Request形式
- Response形式
- ステータスコード

---

# 18. 今後の改善候補

移植完了後に検討する。

- API Versioning
- Controller分割見直し
- Minimal API化検討
- OpenAPI定義強化
- Filterによる共通処理整理

---

# 19. まとめ

ControllerはHTTPリクエストの入口として機能する。

第1段階では既存API仕様を維持し、Controllerには業務ロジックを持たせず、Serviceへ処理を委譲する。

# directory_structure.md

# バックエンドディレクトリ構成設計

## 1. 概要

本ドキュメントは、`re_quest1` の ASP.NET Core Web API におけるディレクトリ構成を定義する。

第1段階では、既存 FastAPI 版の責務分離を維持しながら、ASP.NET Core の一般的な構成へ移植する。

---

# 2. ディレクトリ構成

```text
backend/
│
├─ Controllers/
│
├─ Services/
│
├─ Repositories/
│
├─ Entities/
│
├─ DTOs/
│
├─ Data/
│
├─ Middleware/
│
├─ WebSockets/
│
├─ Extensions/
│
├─ Common/
│
├─ Program.cs
│
└─ appsettings.json
```

---

# 3. Controllers

## 役割

HTTPリクエストを受け付ける。

---

## 構成例

```text
Controllers/
├─ AuthController.cs
├─ DashboardController.cs
├─ ProjectController.cs
├─ TaskController.cs
├─ BudgetController.cs
└─ NotificationController.cs
```

---

## 責務

- Request受取
- DTO受取
- Service呼出
- Response返却

---

# 4. Services

## 役割

業務ロジックを管理する。

---

## 構成例

```text
Services/
├─ AuthService.cs
├─ DashboardService.cs
├─ ProjectService.cs
├─ TaskService.cs
├─ BudgetService.cs
├─ NotificationService.cs
├─ AlertService.cs
└─ PermissionService.cs
```

---

## 責務

- 業務ロジック
- KPI計算
- 通知生成
- 権限制御呼出

---

# 5. Repositories

## 役割

DBアクセスを管理する。

---

## 構成例

```text
Repositories/
├─ UserRepository.cs
├─ ProjectRepository.cs
├─ TaskRepository.cs
├─ BudgetRepository.cs
└─ NotificationRepository.cs
```

---

## 責務

- CRUD
- 検索
- 集計クエリ

---

# 6. Entities

## 役割

DBテーブルを表現する。

---

## 構成例

```text
Entities/
├─ Department.cs
├─ User.cs
├─ Project.cs
├─ ProjectBudget.cs
├─ Task.cs
├─ Worklog.cs
├─ Expense.cs
└─ Notification.cs
```

---

# 7. DTOs

## 役割

API入出力を管理する。

---

## 構成例

```text
DTOs/
├─ Requests/
└─ Responses/
```

---

## Requests

```text
Requests/
├─ LoginRequest.cs
├─ ProjectCreateRequest.cs
├─ TaskCreateRequest.cs
└─ BudgetUpdateRequest.cs
```

---

## Responses

```text
Responses/
├─ LoginResponse.cs
├─ DashboardResponse.cs
├─ ProjectResponse.cs
├─ TaskResponse.cs
├─ BudgetResponse.cs
└─ NotificationResponse.cs
```

---

# 8. Data

## 役割

Entity Framework Core管理。

---

## 構成例

```text
Data/
├─ AppDbContext.cs
├─ DataSeeder.cs
└─ Migrations/
```

---

## AppDbContext

責務

- Entity登録
- リレーション定義
- Index定義

---

## DataSeeder

責務

- 初期データ投入
- テストデータ生成

---

# 9. Middleware

## 役割

共通処理を管理する。

---

## 構成例

```text
Middleware/
├─ ExceptionMiddleware.cs
├─ JwtMiddleware.cs
└─ LoggingMiddleware.cs
```

---

# 10. WebSockets

## 役割

リアルタイム通知を管理する。

---

## 構成例

```text
WebSockets/
├─ NotificationWebSocketManager.cs
└─ NotificationWebSocketHandler.cs
```

---

# 11. Extensions

## 役割

DI登録や設定処理を管理する。

---

## 構成例

```text
Extensions/
├─ ServiceCollectionExtensions.cs
├─ AuthenticationExtensions.cs
└─ SwaggerExtensions.cs
```

---

# 12. Common

## 役割

共通定義を管理する。

---

## 構成例

```text
Common/
├─ Constants/
├─ Enums/
├─ Exceptions/
└─ Helpers/
```

---

# 13. FastAPI版との対応

| FastAPI      | ASP.NET Core            |
| ------------ | ----------------------- |
| routers      | Controllers             |
| services     | Services                |
| repositories | Repositories            |
| schemas      | DTOs                    |
| models       | Entities                |
| database     | Data                    |
| dependencies | Middleware / Extensions |

---

# 14. 第1段階方針

既存PoCの責務分離を維持する。

変更しない内容

- Service中心構成
- Repository利用
- PermissionService
- NotificationService
- AlertService

---

# 15. 今後の改善候補

移植完了後に検討する。

- Clean Architecture化
- CQRS化
- Domain層追加
- Application層追加
- Infrastructure層追加
- Shared Kernel導入

---

# 16. まとめ

ASP.NET Core版では、

```text
Controllers
Services
Repositories
Entities
DTOs
Data
```

を中心とした構成を採用する。

第1段階では既存FastAPI版の責務分離を維持しながら移植を行う。

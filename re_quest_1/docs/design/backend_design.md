# backend_design.md

# バックエンド設計書

## 1. 概要

本ドキュメントは、`re_quest1` におけるバックエンド設計の概要を定義する。

既存の FastAPI + SQLAlchemy 構成を参考にしながら、ASP.NET Core Web API + Entity Framework Core で再実装を行う。

第1段階では、既存PoCと同等の機能・API・権限制御を再現することを目的とする。

---

## 2. 使用技術

| 種別           | 技術                  |
| -------------- | --------------------- |
| 言語           | C#                    |
| Framework      | ASP.NET Core Web API  |
| ORM            | Entity Framework Core |
| Database       | MySQL                 |
| Authentication | JWT                   |
| RealTime       | WebSocket             |
| Validation     | DataAnnotations       |
| Migration      | EF Core Migrations    |

---

## 3. アーキテクチャ概要

採用する構成は以下とする。

```text
Controller
 ↓

Service
 ↓

Repository
 ↓

Entity Framework Core
 ↓

MySQL
```

---

## 4. 詳細設計

詳細は以下のファイルを参照する。

| ファイル                         | 内容               |
| -------------------------------- | ------------------ |
| `backend/architecture.md`        | アーキテクチャ設計 |
| `backend/directory_structure.md` | ディレクトリ構成   |
| `backend/controller_design.md`   | Controller設計     |
| `backend/service_design.md`      | Service設計        |
| `backend/repository_design.md`   | Repository設計     |
| `backend/permission_design.md`   | 認可・IDOR対策設計 |
| `backend/validation_design.md`   | Validation設計     |
| `backend/error_handling.md`      | 例外処理設計       |

---

## 5. 主要構成要素

| 要素              | 役割               |
| ----------------- | ------------------ |
| Controller        | HTTPリクエスト受付 |
| Service           | 業務ロジック       |
| Repository        | DBアクセス         |
| Entity            | DBテーブル表現     |
| DTO               | API入出力          |
| PermissionService | 権限制御           |
| Middleware        | 共通処理           |
| WebSocket         | リアルタイム通知   |

---

## 6. 認証方式

認証方式はJWT認証とする。

```text
Authorization: Bearer <token>
```

---

## 7. 認可方式

認可処理は `PermissionService` に集約する。

主な制御は以下とする。

- ロール制御
- 部門制御
- 案件アクセス制御
- タスクアクセス制御
- 予算アクセス制御
- 通知アクセス制御
- IDOR対策

---

## 8. Entity設計方針

EntityはDBテーブルと1対1対応とする。

主なEntityは以下とする。

```text
Department
User
Project
ProjectBudget
Task
Worklog
Expense
Notification
```

---

## 9. DTO設計方針

APIとの入出力にはDTOを使用する。

### Request DTO

```text
LoginRequest
ProjectCreateRequest
TaskCreateRequest
BudgetUpdateRequest
```

### Response DTO

```text
LoginResponse
ProjectResponse
DashboardResponse
TaskResponse
BudgetResponse
NotificationResponse
```

---

## 10. Migration方針

EF Core Migrationsを使用する。

```bash
dotnet ef migrations add InitialCreate
dotnet ef database update
```

---

## 11. 第1段階方針

第1段階では既存FastAPI版の挙動を維持する。

変更しない内容は以下とする。

- APIパス
- HTTPメソッド
- DB構造
- ロール設計
- ステータス設計
- 権限制御
- 通知仕様
- アラート判定

---

## 12. 今後の改善候補

移植完了後、以下を検討する。

- CQRS導入
- MediatR導入
- FluentValidation導入
- Refresh Token
- Cookie認証
- Redisキャッシュ
- BackgroundService通知
- OpenTelemetry
- Serilog

---

## 13. まとめ

第1段階では既存 FastAPI版の挙動を維持し、ASP.NET Core Web API に移植する。

Controller・Service・Repository・Entity の責務を明確に分離し、既存PoCで得た知見である PermissionService・IDOR対策・Validation強化を最初から組み込む。

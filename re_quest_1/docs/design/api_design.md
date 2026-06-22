# api_design.md

# API設計書

## 1. 概要

本ドキュメントは、`re_quest1` におけるAPI設計の概要を定義する。

第1段階では既存 `quest_1` の FastAPI 実装を基準とし、
ASP.NET Core Web API に移植する。

---

## 2. API基本方針

## ベースURL

```text
/api
```

---

## 認証方式

```text
JWT
```

APIリクエスト時は、Authorization Header にアクセストークンを付与する。

```text
Authorization: Bearer <token>
```

---

## 3. レスポンス形式

## 成功時

```json
{
  "data": {}
}
```

---

## エラー時

```json
{
  "detail": "Error Message"
}
```

---

## 4. 詳細設計

詳細は以下のファイルを参照する。

| ファイル                  | 内容                          |
| ------------------------- | ----------------------------- |
| `api/auth_api.md`         | 認証API                       |
| `api/dashboard_api.md`    | ダッシュボードAPI             |
| `api/project_api.md`      | 案件API・承認API・案件進行API |
| `api/task_api.md`         | タスクAPI                     |
| `api/budget_api.md`       | 予算API・工数API・経費API     |
| `api/notification_api.md` | 通知API・WebSocket            |

---

## 5. HTTPステータス

## 成功

| Status | 内容       |
| ------ | ---------- |
| 200    | OK         |
| 201    | Created    |
| 204    | No Content |

---

## エラー

| Status | 内容                  |
| ------ | --------------------- |
| 400    | Bad Request           |
| 401    | Unauthorized          |
| 403    | Forbidden             |
| 404    | Not Found             |
| 422    | Validation Error      |
| 500    | Internal Server Error |

---

## 6. 認可方針

## APPLICANT

- 自案件のみ参照可能

## DEPT_MANAGER

- 自部門案件のみ参照可能

## HQ_MANAGER

- 全案件参照可能

## TASK_MEMBER

- 担当案件のみ操作可能

---

## 7. セキュリティ方針

API側で以下を実施する。

- JWT認証
- ロール制御
- 部門制御
- IDOR対策
- 入力値検証

---

## 8. ASP.NET Core実装方針

## Controller

例：

```text
AuthController
DashboardController
ProjectController
TaskController
BudgetController
NotificationController
```

---

## Service

例：

```text
AuthService
DashboardService
ProjectService
TaskService
BudgetService
NotificationService
PermissionService
```

---

## Repository

例：

```text
ProjectRepository
TaskRepository
BudgetRepository
NotificationRepository
```

---

## 9. 第1段階の方針

既存 FastAPI のAPI仕様を維持する。

変更しない項目

- URL
- HTTPメソッド
- Request
- Response
- 権限制御
- ステータスコード

---

## 10. 今後の改善候補

移植完了後、以下を検討する。

- API Versioning
- Refresh Token
- Cookie認証
- OpenAPI自動生成
- レート制限
- 監査ログAPI
- GraphQL対応検討

---

## 11. まとめ

第1段階では既存PoCのAPI仕様を維持し、
ASP.NET Core Web APIで同等の挙動を実現する。

# architecture.md

# バックエンドアーキテクチャ設計

## 1. 概要

本ドキュメントは、`re_quest1` の ASP.NET Core Web API におけるバックエンドアーキテクチャを定義する。

既存 `quest_1` の FastAPI 構成を参考にしながら、Controller / Service / Repository の責務を分離した構成で再実装する。

---

# 2. 採用アーキテクチャ

採用する基本構成は以下とする。

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

# 3. 各層の責務

## Controller

HTTPリクエストの受付を担当する。

### 主な責務

- Request受取
- DTO受取
- Validation実行
- Service呼出
- Response返却

### 行わないこと

- SQL実行
- 業務ロジック
- 権限制御ロジックの詳細実装
- 集計処理

---

## Service

業務ロジックを担当する。

### 主な責務

- 案件作成
- 承認処理
- ステータス更新
- 予算計算
- 通知生成
- 権限確認呼び出し
- ダッシュボード集計

---

## Repository

DBアクセスを担当する。

### 主な責務

- Entity取得
- Entity登録
- Entity更新
- Entity削除
- 条件検索
- 集計用クエリ

### 行わないこと

- 業務判断
- ロール判定
- レスポンス整形

---

## Entity

DBテーブルを表現する。

### 主な責務

- テーブル構造の表現
- リレーションの表現

---

## DTO

API入出力を表現する。

### 主な責務

- Request形式の定義
- Response形式の定義
- Entityを直接外部に返さないための境界

---

# 4. 処理フロー

## 基本フロー

```text
Request
 ↓

Controller
 ↓

Service
 ↓

Repository
 ↓

DbContext
 ↓

MySQL
 ↓

Repository
 ↓

Service
 ↓

Controller
 ↓

Response
```

---

# 5. 認証フロー

```text
Login Request
 ↓

AuthController
 ↓

AuthService
 ↓

UserRepository
 ↓

Password Verification
 ↓

JWT Generate
 ↓

Login Response
```

---

# 6. 認可フロー

```text
Request
 ↓

Controller
 ↓

Service
 ↓

PermissionService
 ↓

Role / Department / Ownership Check
 ↓

許可
または
403 Forbidden
```

---

# 7. 通知フロー

```text
業務イベント発生
 ↓

Service
 ↓

NotificationService
 ↓

NotificationRepository
 ↓

DB保存
 ↓

WebSocket送信
```

---

# 8. ダッシュボード集計フロー

```text
Dashboard Request
 ↓

DashboardController
 ↓

DashboardService
 ↓

Role判定
 ↓

Repositoryで必要データ取得
 ↓

集計
 ↓

DashboardResponse
```

---

# 9. 依存方向

依存方向は上位から下位へ向ける。

```text
Controller
 ↓
Service
 ↓
Repository
 ↓
Data
```

## 方針

- ControllerはServiceに依存する
- ServiceはRepositoryに依存する
- RepositoryはDbContextに依存する
- RepositoryがControllerに依存しない
- EntityがControllerに依存しない

---

# 10. ASP.NET Coreでの登録方針

DIコンテナにService / Repositoryを登録する。

## 例

```csharp
builder.Services.AddScoped<IProjectService, ProjectService>();
builder.Services.AddScoped<IProjectRepository, ProjectRepository>();
builder.Services.AddScoped<IPermissionService, PermissionService>();
```

---

# 11. 第1段階方針

第1段階では、既存FastAPI版の設計思想を維持する。

## 維持する内容

- Service層分離
- PermissionService
- Query処理の分離
- Response整形
- Validation
- 例外処理

---

# 12. 今後の改善候補

移植完了後に検討する。

- Clean Architecture化
- CQRS導入
- MediatR導入
- Domain Service分離
- UseCase層追加
- Repository不要箇所の見直し
- Unit of Work整理

---

# 13. まとめ

バックエンドでは、Controller / Service / Repository の責務を明確に分離する。

第1段階では既存PoCの挙動再現を優先し、移植完了後にASP.NET Coreらしい設計改善を検討する。

# migration_policy.md

# re_quest1 移行方針書

## 1. 目的

既存の `quest_1` で開発した「開発案件予実可視化アプリケーション」を、React + TypeScript および C# / ASP.NET Core を用いて再実装する。

本移行では、まず既存システムと同等の機能・画面・挙動を再現することを最優先とし、設計改善や機能追加は移植完了後に実施する。

---

## 2. 移行対象

### 現行構成

```text
quest_1/
├─ frontend/   # Vue 3 + TypeScript
└─ backend/    # FastAPI + Python
```

### 新構成

```text
re_quest1/
├─ frontend/   # React + TypeScript
├─ backend/    # ASP.NET Core Web API
├─ docs/
└─ README.md
```

---

## 3. 基本方針

### 第1段階：完全移植

以下の内容は原則変更しない。

- 画面構成
- URL構成
- API仕様
- DB設計
- ロール設計
- 承認フロー
- 通知仕様
- アラート判定
- シードデータ

目標は、

> 「既存の Vue + FastAPI 版と同じ操作ができる状態」

を実現することである。

---

## 4. 技術スタック

### フロントエンド

| 現行         | 移行後       |
| ------------ | ------------ |
| Vue 3        | React        |
| TypeScript   | TypeScript   |
| Vue Router   | React Router |
| Pinia        | Zustand      |
| Element Plus | MUI          |
| Vite         | Vite         |

### バックエンド

| 現行       | 移行後                |
| ---------- | --------------------- |
| FastAPI    | ASP.NET Core Web API  |
| SQLAlchemy | Entity Framework Core |
| Alembic    | EF Core Migration     |
| Pydantic   | DTO + Validation      |
| JWT        | JWT                   |
| MySQL      | MySQL                 |

---

## 5. 移行順序

### フェーズ1

- プロジェクト作成
- React環境構築
- ASP.NET Core環境構築
- DB接続確認

### フェーズ2

- 認証機能
- ユーザー管理
- 部門管理

### フェーズ3

- 案件管理
- 承認機能
- タスク管理
- 予算管理

### フェーズ4

- 通知機能
- ダッシュボード
- ロール別画面

### フェーズ5

- 権限制御
- テスト
- デプロイ

---

## 6. ロール設計

既存システムと同一とする。

- APPLICANT
- DEPT_MANAGER
- HQ_MANAGER
- TASK_MEMBER

---

## 7. ステータス設計

### ProjectStatus

- DRAFT
- PENDING_DEPT
- PENDING_HQ
- APPROVED
- IN_PROGRESS
- COMPLETED
- REJECTED

### TaskStatus

- TODO
- IN_PROGRESS
- IN_REVIEW
- DONE

---

## 8. セキュリティ方針

既存システムで実装した内容を維持する。

### 認証

- JWT認証

### 認可

- ロール別アクセス制御
- 部門単位アクセス制御
- IDOR対策

---

## 9. 第1段階で実施しない内容

以下は移植完了後に検討する。

- UI刷新
- API再設計
- DB再設計
- Cookie認証化
- Refresh Token導入
- CSRF対策
- CI/CD改善
- 新機能追加

---

## 10. 完了条件

以下を満たした時点で移植完了とする。

- React版で全主要画面が表示できる
- ASP.NET Core版で主要APIが動作する
- 既存システムと同等の操作が可能
- 権限制御が再現できている
- シードデータで動作確認できる
- 既存版との差異を説明できる

---

## 11. 将来計画

移植完了後に以下を検討する。

- React向け設計改善
- ASP.NET Core向け設計改善
- 認証強化
- テスト拡充
- UI/UX改善
- 運用監視機能追加
- CI/CD構築

まずは「改善」ではなく「再現」を優先する。

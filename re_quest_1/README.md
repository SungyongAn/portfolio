# re_quest1

開発案件予実可視化アプリケーション（Rebuild Version）

---

# 概要

本プロジェクトは、開発案件の申請・承認・進捗管理・予算管理を一元管理するWebアプリケーションです。

既存の `quest_1` にて作成した PoC（Proof of Concept）をベースに、技術スタックを刷新しながら再構築を行います。

---

# プロジェクト目的

本プロジェクトの目的は以下の3点です。

- React + TypeScript によるフロントエンド再構築
- ASP.NET Core Web API によるバックエンド再構築
- 既存PoCの機能・設計を維持した状態での移植

第1段階では機能追加や設計変更は行わず、既存システムと同等の挙動を再現することを目標とします。

---

# 移行元プロジェクト

```text
quest_1
```

## 既存構成

```text
Frontend
Vue 3 + TypeScript

Backend
FastAPI + Python

Database
MySQL
```

---

# 移行後構成

```text
Frontend
React + TypeScript

Backend
ASP.NET Core Web API

Database
MySQL
```

---

# 技術スタック

## Frontend

- React
- TypeScript
- Vite
- React Router
- Zustand
- MUI
- fetch API

---

## Backend

- C#
- ASP.NET Core Web API
- Entity Framework Core
- JWT Authentication
- WebSocket

---

## Database

- MySQL 8

---

# システム構成

```text
Browser
   │
   ▼

React Frontend
   │
   ▼

ASP.NET Core Web API
   │
   ▼

MySQL
```

---

# ロール一覧

| ロール       | 説明       |
| ------------ | ---------- |
| APPLICANT    | 申請者     |
| DEPT_MANAGER | 部門管理者 |
| HQ_MANAGER   | 本部管理者 |
| TASK_MEMBER  | 担当者     |

---

# 主な機能

## 認証

- ログイン
- JWT認証

---

## 案件管理

- 案件作成
- 案件編集
- 案件一覧
- 案件詳細

---

## 承認機能

- 部門承認
- 本部承認
- 却下

---

## タスク管理

- タスク作成
- タスク更新
- ガントチャート

---

## 予算管理

- 予算管理
- 工数管理
- 経費管理

---

## 通知機能

- 通知一覧
- 既読管理
- WebSocket通知

---

## ダッシュボード

- KPI表示
- リスク案件表示
- ロール別ダッシュボード

---

# ディレクトリ構成

```text
re_quest1/
│
├─ README.md
│
├─ docs/
│  ├─ migration_policy.md
│  ├─ feature_list.md
│  │
│  └─ design/
│      ├─ README.md
│      ├─ system_design.md
│      ├─ database_design.md
│      ├─ api_design.md
│      ├─ frontend_design.md
│      └─ backend_design.md
│
├─ frontend/
│
└─ backend/
```

---

# ドキュメント一覧

## プロジェクト管理

| ファイル                 | 内容     |
| ------------------------ | -------- |
| docs/migration_policy.md | 移行方針 |
| docs/feature_list.md     | 機能一覧 |

---

## 設計書

| ファイル           | 内容               |
| ------------------ | ------------------ |
| system_design.md   | システム全体設計   |
| database_design.md | DB設計             |
| api_design.md      | API設計            |
| frontend_design.md | フロントエンド設計 |
| backend_design.md  | バックエンド設計   |

---

# 開発方針

## 第1段階

既存PoCの完全移植を行う。

変更しない項目

- 画面構成
- API仕様
- DB設計
- ロール設計
- 承認フロー
- 通知仕様
- アラート判定

---

## 第2段階

移植完了後に改善を検討する。

候補

- UI改善
- 認証強化
- HttpOnly Cookie
- Refresh Token
- CSRF対策
- React Query
- FluentValidation
- CI/CD

---

# 開発ルール

## 基本方針

- 既存PoCとの差分を最小限にする
- 第1段階では設計改善を行わない
- まずは同等機能を再現する
- 改善案は別途記録する

---

## ドキュメント更新

以下の変更を行った場合はドキュメントを更新する。

- 機能追加
- API変更
- DB変更
- 権限制御変更
- 設計変更

---

# 開発フロー

```text
要件確認
 ↓

設計書更新
 ↓

実装
 ↓

動作確認
 ↓

テスト
 ↓

CHANGELOG更新
```

---

# 今後の予定

## Phase 1

- React環境構築
- ASP.NET Core環境構築
- 認証移植
- 案件管理移植
- 承認機能移植
- タスク管理移植
- 予算管理移植
- 通知移植
- ダッシュボード移植

---

## Phase 2

- 設計改善
- セキュリティ強化
- テスト拡充
- 運用改善

---

# ライセンス

Personal Portfolio Project

---

# 備考

本プロジェクトは学習およびポートフォリオ用途を目的として開発しています。

第1段階では既存PoCの再現を最優先とし、その後段階的な改善を実施します。

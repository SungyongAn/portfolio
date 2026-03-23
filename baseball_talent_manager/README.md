# Baseball Talent Manager（PoC）

## 概要
本リポジトリは、部活動における測定結果管理業務を対象とした  
PoC（Proof of Concept）プロジェクトです。

本PoCでは以下を検証対象とします。

- ロール別の業務フローをシステム化できるか
- 測定結果の入力・承認・閲覧フローの実現可能性
- Webアプリとしての基本構成の成立性

※本プロジェクトは本番運用を目的としたものではなく、
PoCとして最小構成で検証を行うものです。

---

## 開発状況

現在は **フェーズE：課題2実装中** です。

### 完了
- 課題精査
- ユースケース整理（docs/usecase.md）
- PoC機能決定（docs/functions.md）
- 画面設計（docs/screens.md）
- API設計（docs/api.md）
- 認証設計（docs/auth_design.md）
- ロール権限マトリクス（docs/role_matrix.md）
- ER図・テーブル設計（docs/er.md）
- Docker環境構築
  - docker-compose.yml
  - docker-compose.dev.yml
  - mysql/Dockerfile・my.cnf
  - backend/Dockerfile
  - frontend/Dockerfile.dev
  - scripts/wait_for_db.py
- Alembic環境構築・マイグレーション実行
  - usersテーブル
  - measurementsテーブル
- バックエンド環境構築
  - backend/app/db.py
- モックUI実装（課題1）
  - dummyData.js
  - router/index.js
  - 各コンポーネント実装済み（下記参照）

### 実装済み画面（課題1：モックUI）

#### マネージャー
- [x] `views/manager/DashboardView.vue`（ダッシュボード）
- [x] `views/manager/MeasurementResultSubmit.vue`（測定結果の入力）
- [x] `views/manager/MeasurementStatusList.vue`（承認ステータス一覧）

#### 部員・コーチ・監督共通
- [x] `views/shared/DashboardView.vue`（ダッシュボード）

#### 共通コンポーネント
- [x] `components/AppHeader.vue`（共通ヘッダー）
- [x] `components/MeasurementResultReview.vue`（測定記録の承認・否認）
- [x] `components/MeasurementResultList.vue`（測定記録の閲覧）
- [x] `components/MemberManagement.vue`（部員管理メニュー）
- [x] `components/MemberCreate.vue`（部員作成）
- [x] `components/MemberRetire.vue`（退部・引退処理）

### 次の予定
- 課題2実装
  - EChartsによる可視化ダッシュボード
  - 重複登録防止
  - スマートフォン対応
  - 提案書作成（proposal_ux.md・proposal_system.md・proposal_technical.md）
---

## 設計ドキュメント

設計関連ドキュメントは docs フォルダに格納しています。

- ユースケース整理：`docs/usecase.md`
- PoC機能一覧：`docs/functions.md`
- 画面設計：`docs/screens.md`
- API設計：`docs/api.md`
- 認証設計：`docs/auth_design.md`
- ロール権限マトリクス：`docs/role_matrix.md`
- ER図・テーブル設計：`docs/er.md`

---

## 参考資料

課題資料・検討用ファイルは以下に格納しています。
`docs/reference_materials/`

---

## ディレクトリ構成（主要部分）
```
baseball_talent_manager/
├── docker-compose.yml
├── docker-compose.dev.yml
├── mysql/
│   ├── Dockerfile
│   └── conf.d/
│       └── my.cnf
├── backend/app/
│   ├── db.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── measurement.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── measurement.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── security.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── measurement_service.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       └── measurements.py
├── frontend/
│   ├── Dockerfile.dev
│   ├── Dockerfile.prod
│   ├── nginx.conf
│   ├── .env.production
│   └── src/
│       ├── services/
│       │   ├── api.js
│       │   ├── authService.js
│       │   ├── measurementService.js
│       │   └── userService.js
│       ├── components/
│       │   ├── AppHeader.vue
│       │   ├── MeasurementResultReview.vue
│       │   ├── MeasurementResultList.vue
│       │   ├── MemberManagement.vue
│       │   ├── MemberCreate.vue
│       │   └── MemberRetire.vue
│       ├── views/
│       │   ├── LoginView.vue
│       │   ├── shared/
│       │   │   └── DashboardView.vue
│       │   └── manager/
│       │       ├── DashboardView.vue
│       │       ├── MeasurementResultSubmit.vue
│       │       └── MeasurementStatusList.vue
│       ├── router/
│       │   └── index.js
│       ├── stores/
│       │   └── auth.js
│       └── dummyData.js
├── scripts/
│   └── wait_for_db.py
└── docs/
```

## 技術スタック

### Frontend
- Vue 3
- Vite
- Vue Router
- Pinia

### Backend
- FastAPI
- SQLAlchemy
- Alembic

### Database
- MySQL 8.0

### 認証
- メール＋パスワード認証
- Argon2（パスワードハッシュ）
- JWT認証（Access Token + Refresh Token）

### 開発環境
- Docker / docker-compose

---

## 起動方法（開発環境）
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

### マイグレーション実行
```bash
cd backend
alembic upgrade head
```

## 起動方法（本番環境）
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### マイグレーション実行
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend alembic upgrade head
```

### 初期データ投入
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec db mysql -uroot -proot baseball_talent_manager < seed.sql
```

### アクセス
- フロントエンド：`http://<サーバーIP>/`
- APIドキュメント：`http://<サーバーIP>/api/docs`（開発確認用）

---

## 備考

本リポジトリは段階的に設計→プロトタイプ実装→改善の順で進めます。
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

現在は **フェーズB：プロトタイプ実装フェーズ** です。

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
- モックUI作成開始
  - dummyData.js作成
  - router/index.js作成中
  - 各コンポーネント（空ファイル）作成

### 進行中
- フェーズB：プロトタイプ実装
- router/index.js修正・完成
- stores/auth.js作成
- components/AppHeader.vue作成
- 各画面コンポーネント実装

### 次の予定
- バックエンド実装（FastAPI）
- フロントエンド実装（Vue.js）
- seed.sql作成
- 動作確認

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
├── backend/
│   ├── Dockerfile
│   ├── .env
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       ├── 001_create_users.py
│   │       └── 002_create_measurements.py
│   └── app/
│       └── db.py
├── frontend/
│   ├── Dockerfile.dev
│   └── src/
├── scripts/
│   └── wait_for_db.py
└── docs/
```

---

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

### DBのみ起動（現在の状態）
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d db
```

### 全サービス起動（フロント・バックエンド実装完了後）
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

### マイグレーション実行
```bash
cd backend
alembic upgrade head
```


## 備考

本リポジトリは段階的に設計→プロトタイプ実装→改善の順で進めます。
# Changelog

## 2026/01/15

## Changed
- init.sql とマイグレーションの役割を整理し、テーブル定義の重複を解消
- テストデータ投入専用として seed.sql を新規作成
- 表記上の問題で ER図.pdf を削除、er_diagram.mmd に変更

## Fixed
- seed.sql 実行時に発生していた外部キー制約エラーを修正
- AUTO_INCREMENT ID の直指定を廃止し、サブクエリによる参照方式に変更
- MySQLコンテナの文字コード設定を修正
  - seed.sql実行時の文字化けを解消するため、MySQL設定ファイル(my.cnf)でutf8mb4を指定
  - `mysql/Dockerfile`と`mysql/conf.d/my.cnf`を新規作成
  - `docker-compose.yml`のdbサービスをbuild方式に変更
  - ※現在もseed.sql実行時に文字化けが発生しており、原因調査中

## 2026/01/14

#### Changed
- Docker 開発環境において Frontend のホットリロードが機能していなかったため、
  Vite のファイル監視方式をポーリングに変更する設定を `vite.config.js` に追加

### Frontend
- 管理者用コンポーネントの作成を開始
    - `UsersView.vue` `UserCreateView.vue` を作成
    - 空ファイルの　`UserEditView.vue` `GradesView.vue` `ClassesView.vue` を作成
    - `UserManagementView.vue` を削除
    - `api.js` `index.js` を更新

## 2026/01/09

#### Changed
- Dockerコンテナ起動時に DB の起動を待って backend を起動するように `docker-compose.yml` を更新
  - DB 起動確認用のスクリプト `/backend/wait_for_db.py` を作成

- `docker-compose.yml` を開発環境用、本番用と分けてコンテナ化できるように分割
  - `docker-compose.dev.yml` `docker-compose.prod.yml` を作成

### Frontend
- 本番環境用の `Dockerfile` を仮作成

## 2026/01/08

#### Changed
- Docker を用いた開発環境でホットリロードを適用するため、`docker-compose.yml` を更新
  - フロントエンドとバックエンド間の通信設定を整理
  - 環境変数（API URL 等）の設定方法を見直し、開発時の疎通を安定化

- `READEME.md` を更新

## 2026/01/07

### Frontend
#### Changed
- ログイン後の画面遷移設計を見直し
  - LoginView.vue からロール依存の遷移処理を削除
  - ログイン成功時は `/` へ遷移し、画面振り分けを Router に集約
- Vue Router のルーティング設計を改善
  - `/` をロール別リダイレクト用のハブルートとして定義
  - `beforeEach` ナビゲーションガードでユーザーロールに応じた初期遷移を制御
    - admin → `/admin/users`
    - teacher → `/teacher/dashboard`
    - student → `/student/dashboard`
- 管理者ログイン時に `/admin/dashboard` が存在せず 404 になる問題を修正

### Backend
- 再びPython 3.12 環境において passlib + bcrypt の組み合わせで発生していた認証エラーを確認したため修正
  - ハッシュ化を bcrypt から argon2 に変更

## 2026/01/06

### Backend
#### Changed
- 仮想環境の作成方法を `python -m venv venv` から `uv venv .venv` に変更


## 2025/12/30

- API通信の基盤整備
  - `src/services/api.js`: Axios設定、APIエンドポイント定義
  - リクエストインターセプター（JWTトークン自動付与）
  - レスポンスインターセプター（401エラー時の自動ログアウト）
- 状態管理の実装
  - `src/stores/auth.js`: Pinia認証ストアを作成
  - ログイン/ログアウト処理
  - LocalStorageとの連携
- ルーティングの実装
  - `src/router/index.js`: Vue Routerの設定
  - 認証ガード（ロール別アクセス制御）
  - 生徒/教師/管理者ごとのルート定義
- UI実装
  - `src/views/LoginView.vue`: ログイン画面の作成
    - Bootstrapによるレスポンシブデザイン
    - パスワード表示/非表示トグル
    - ローディング状態の表示
    - エラーメッセージ表示
  - 各ロール用の仮ダッシュボード作成
    - `src/views/student/DashboardView.vue`: 生徒用
    - `src/views/teacher/DashboardView.vue`: 教師用
    - `src/views/admin/UserManagementView.vue`: 管理者用
  - その他のビューファイル作成
    - `src/views/student/SubmitView.vue`: 連絡帳提出
    - `src/views/student/HistoryView.vue`: 履歴表示
    - `src/views/teacher/SubmissionsView.vue`: 提出状況
    - `src/views/teacher/UnreadView.vue`: 未読一覧
    - `src/views/NotFoundView.vue`: 404ページ
- 環境変数設定（`.env`ファイル作成、`VITE_API_URL`設定）
- フロントエンド・バックエンド連携の動作確認完了
  - ログイン → トークン取得 → ダッシュボード遷移の動作確認

### Fixed

- `requirements.txt`の不足パッケージを追加
  - `uvicorn[standard]`: サーバー起動に必須
  - `pymysql`: MySQLドライバ
  - `email-validator`: Pydanticのメールバリデーション
  - `python-multipart`: FastAPIのフォーム処理
- Viteの import エラーを解決（ビューファイルの不足を修正）

## 2025/12/24

### Backend

- `requirements.txt` を重複や不足を確認したため、更新

- ターミナルからのログイン認証が成功しないため、パスワードハッシュおよび認証処理の調査を実施中。

## Fixed

- Python 3.12 環境において passlib + bcrypt の組み合わせで発生していた認証エラーを修正
- Python バージョンを 3.11 に変更
- bcrypt を 3.2.2、passlib を 1.7.4 に固定し、互換性問題を解消

## 2025/12/23

### Backend

- `email-validator` の導入時のエラーを対処

  - `pip install email-validator` の再実行で解決

- Pydantic モデルを集約し、import を簡潔にしつつ、パッケージの公開インターフェースを明確にするため、`app/` 配下にある `__init__.py` を全て更新
- `models` 配下の `journal.py` `user.py` を更新、 `class_model.py` を作成
- `schemas` 配下の `journal.py` `user.py` を更新
- `routers` 配下の `journal.py` `user.py` を更新、 `teachers.py` `users.py` を作成
- `services` 配下の `journal_service.py` `user_service.py` を更新、 `teacher_service.py` `user_service.py` を作成
- `app` 配下の `db.py` `dependencies.py` `main.py` を更新

## 2025/12/22

### Backend

- 初期 admin アカウント登録のため、 `4cd0c6be197e_add_initial_admin_user.py` を作成の上、反映
- `init.sql` にて作成した `renrakucho_db` を削除
- admin アカウント情報 メールアドレス:`admin@school.ac.jp` パスワード: `password123`
- `models` 配下に `journal.py` `user.py` を作成
- `schemas` 配下に `journal.py` `user.py` を作成
- `routers` 配下に `journal.py` `user.py` を作成
- `services` 配下に `journal_service.py` `user_service.py` を作成
- `app` 配下に `db.py` `dependencies.py` を作成、`main.py` を更新
- `email-validator` の導入を開始
  - 12/22 現在、以下のエラーが表示される状態で原因調査中
    ImportError: email-validator is not installed, run `pip install pydantic[email]`

## 2025/12/20

### Added

- 連絡帳システムを新規プロジェクトとして再構築

### Backend

- FastAPI をベースとしたバックエンド初期構成を作成
- `app/` 配下に以下のレイヤ構造を定義
  - `models`：ORM モデル管理用ディレクトリ
  - `schemas`：Pydantic スキーマ管理用ディレクトリ
  - `routers`：API ルーティング管理用ディレクトリ
  - `services`：ビジネスロジック分離用ディレクトリ
- DB 接続管理用 `db.py` を追加
- アプリケーションエントリポイントとして `main.py` を追加
- Python 仮想環境（venv）および `requirements.txt` を導入

#### Database / Migration

- Alembic を導入し、データベーススキーマのマイグレーション管理のため、 Alembic の学習を開始

### Frontend

- Vite + Vue.js によるフロントエンド初期構成を作成
- `src/` 配下に以下を配置
  - `router`：Vue Router 管理
  - `stores`：状態管理（Pinia 想定）
  - `App.vue`：ルートコンポーネント
  - `main.js`：アプリケーションエントリポイント
- ESLint / Prettier を導入し、コード整形ルールを統一
- Vite 設定ファイル `vite.config.js` を追加

### Infrastructure

- Docker Compose による開発環境定義を追加
- DB 初期化用 `init.sql` を追加

### Docs

- プロジェクトルートおよびフロントエンドに README.md を配置
- 変更履歴管理のため `CHANGELOG.md` を追加
- `docs/` 配下に `ER図.png` を追加

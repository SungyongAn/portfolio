# Changelog

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

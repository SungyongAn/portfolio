# Changelog

## 2026/01/24

## Changed
- 認証処理を interceptor による 401 ハンドリング中心の構成へ移行
- トークン更新をタイマー方式からレスポンス起点方式に変更
- refresh API の再帰呼び出し防止処理を追加

## 2026/01/23

### Frontend
- ログイン後に全画面で共有される共通ヘッダー／フッターを実装
  - ユーザーロール（student / teacher / admin）に応じたナビゲーション表示を追加
  - 未読件数・ユーザー情報表示の土台を実装（API連携は今後対応）
  - `/src/components/AppHeader.vue` `/src/components/AppFooter.vue` を新規作成
  - 共通レイアウト適用のため `App.vue` `router/index.js` を更新

### Backend
- 教師の担当情報管理ロジック改善に伴い、関連モデルを更新
  - 教師・学年・クラス・教科の関係を明確化
  - DBスキーマ変更に対応するため `/models/user.py` `/models/class_model.py` を修正

## Changed
- 認証設計の見直し
  - 特定画面での挙動調査を通じて、トークン更新処理の役割を整理
  - interceptor による 401 ハンドリングを中心とした構成方針を採用
  - auth store 内の token refresh timer は不要と判断し、将来的に削除予定

## 2026/01/22

## Added
- 教師の教科担当を正規化するため `subjects` テーブルを追加
  - 教科名（name）の一意制約を設定
  - 有効／無効を管理するため `is_active` カラムを追加

## Changed
- 教師の担当情報管理を改善
  - `teacher_assignments` テーブルに `subject_id` を追加
  - 教科情報を `subjects` テーブル参照に変更
- 教科名の文字列管理を廃止
  - `teacher_assignments.subject_name` カラムを削除
  - 教科情報はマスタテーブル（subjects）で一元管理する設計に変更

## Design
- 教師の担当種別（homeroom / subject / grade_head / administrator）ごとの
  必須項目制御は DB 制約ではなく、バックエンドのサービス層バリデーションで行う方針を明確化
- 学年（grades）・クラス（classes）は、生徒・教師で共通利用する設計とした
- ER 図とは別に、役割（role / assignment_type）ごとのバリテーション設計をドキュメント化

## Migration
- Alembic による差分マイグレーションを追加
  - subjects テーブル作成
  - teacher_assignments の教科管理方式変更

## 2026/01/21

## Fixed
- classes 初期データ登録処理の改善
  - 初期登録情報が残っており、文字化けしていたため修正

## 2026/01/20

### Backend
- `get_admin_user_list` API のユーザー一覧取得ロジックを修正
  - 教師の `role` を `assignment_type` に基づき担任、副担任、学年主任、教科担当などに変換して返すよう変更
- `AdminUserListResponse` スキーマの `role` フィールドを `str` に修正

### Frontend
- ユーザー一覧表示で `role` をそのまま表示するよう修正
- 不要となった `getRoleLabel` 関数を削除
- 教師の表示が `teacher` から適切なラベル（担任・副担任等）になるよう変更

## 2026/01/16

## Changed
- **ログイン期間管理機能の実装（アクセストークン / リフレッシュトークン）**
  - アクセストークンはメモリに保持、リフレッシュトークンは HttpOnly Cookie で管理
  - フロントエンドから直接アクセス不可となり、XSS 攻撃に対して安全性が向上

### Frontend
- 認証ストア（Pinia）を更新し、アクセストークンをメモリ上で管理
- `auth.js` / `api.js` を更新
  - `refreshToken` の localStorage 保存を削除
  - axios の `withCredentials` を設定し、Cookie 経由でリフレッシュトークンを送信
- `main.js` / `LoginView.vue` を更新

### Backend
- `auth_service.py` を更新し、アクセストークンおよびリフレッシュトークンを発行
- 認証ルーター（`auth.py`）を更新
  - ログイン時に refresh_token を HttpOnly Cookie に設定
  - ログアウト時に refresh_token Cookie を削除
- `user.py`（ユーザーモデル）関連を更新
  - リフレッシュトークン対応に伴うアクセストークン生成ロジックを修正

## Fixed
- MySQLコンテナの文字コード設定を修正
  - PowerShell の `Get-Content` で UTF-8 BOM付き出力した場合の文字化けを回避
  - 初期データ投入コマンド：
    ```cmd
    docker compose exec -T db mysql -u root -proot --default-character-set=utf8mb4 journal_system < seed.sql
    ```

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

# 2026/02/06までの統合されてたCHANGELOG

# Changelog

## 2026/02/06

### Changed
- ログインレスポンス設計を整理し、教師ユーザー向けに以下の情報構造を明確化
  - 教師の全割当情報（ `teacher_assignments` ）
  - 一覧表示用の代表割当（ `primary_assignment` ）を分離
- `LoginResponse` / `AdminUserListResponse` に `primary_assignment` を追加し、一覧表示用と詳細編集用の責務を分離
- 教師割当の代表選択ロジックを `resolve_teacher_primary_assignment` に集約し、ロール判定や表示ロジックの重複を解消

### Fixed
- 教師ログイン時に発生していた以下のエラーを修正
  - `tuple` / `dict` / `Schema` が混在していたことによる
    `AttributeError: 'tuple' object has no attribute 'assignment_type'`
- 教師割当取得処理を `TeacherAssignmentSummary`（ `Schema` ）に統一し、service 層から生データ（ `tuple` / `dict` ）を返さない設計に変更
- 割当が存在しない教師ユーザーに対しても安全に処理できるよう、空配列チェックを追加

### Refactored
- 教師割当関連のデータ整形責務を service 層に集約
  - `get_teacher_assignment_summaries`
  - `resolve_teacher_primary_assignment`
- ログイン処理 ( `login_user` ) を「取得 → 整形 → レスポンス返却」の単純な構造に整理
  - 認証レスポンスにおけるロール分岐の可読性を向上

### Notes
- フロントエンド（Pinia / auth store）側の修正は不要
  + 既存の `primary_assignment` / `teacher_assignments` 利用設計と整合
- 今後、管理者ユーザー一覧（ `AdminUserList` ）でも `resolve_teacher_primary_assignment` を共通利用可能な設計とした

## 2026/02/05

### Changed
- ログアウト処理の責務を `authStore.logout()` に集約
  - `authService.logout()` は API 通信のみを担当するよう整理
  - Store 側で以下の処理を一元管理する設計に変更
    - 認証状態（accessToken / user 情報）の初期化
    - 無操作タイマー（inactivityTimer）の解除
    - ログイン画面へのルーティング遷移
- 無操作タイムアウト時のログアウト処理を `authStore.logout()` 経由に統一
  - ログアウト時の副作用（状態リセット・タイマー解除・遷移）が確実に実行されるよう改善

- 管理者向けユーザー一覧取得ロジックを再設計
  - 教師の複数割当（担任・学年主任・教科担当など）に対応
  - DB の結合結果を user_id 単位で集約する `aggregate_admin_user_rows()` を追加
  - 教師割当を一覧表示用データと内部判断用データに分離

- 教師割当の責務分離を実施
  - `TeacherAssignmentSummary`
    - 教師が持つ各割当の事実データ（複数件）を表現
  - `UserPrimaryAssignment`
    - 複数割当の中から優先度に基づき代表1件を決定する表示・判定用モデル
  - 一覧表示・権限制御でのロジック簡略化を実現

- 教師の代表割当決定ロジックを service 層に集約
  - `resolve_teacher_primary_assignment()` を追加
  - 割当種別・主担当フラグに基づく優先順位ルールを明示化
  - フロントエンド側に割当解釈ロジックを持たせない設計に変更

- `AdminUserListResponse` のレスポンス構造を拡張
  - `primary_assignment` を追加し、ユーザー一覧での役割表示を安定化
  - `teacher_assignments` は詳細・管理用途として保持
  - 生徒・教師・管理者でレスポンス構造が破綻しないよう条件分岐を整理

- outer join 結果における `None` 値を考慮したデータ構築処理を改善
  - クラス未紐付けの教師割当でも Pydantic バリデーションエラーが発生しないよう調整

## 2026/02/04

### Added
- `scripts/create_journal_via_api.py` を作成
  - API 経由で日誌を作成するスクリプトを追加

- `docker-compose.dev.yml` を更新
  - 開発環境コンテナでルート直下の `scripts/` を認識できるよう `volumes` にマウントを追加

- `backend/requirements.txt` に `requests>=2.31.0` を追記
  - Python スクリプトで HTTP リクエストを利用可能に

### Changed
- ログイン時に返却するユーザー情報の設計を見直し、ロール（生徒 / 教師）ごとに取得すべき学年・クラス情報を明確化
  - 生徒ログイン時：現在所属している学年・クラス情報を取得する想定
  - 教師ログイン時：`teacher_assignments` を基に担当学年・クラス情報を取得する設計とした

### Design
- `teacher_assignments` は 常に list として扱い、未割当時は空配列を返却する設計とした
  - `list[...] | None `は使用せず、フロントエンド側での分岐を簡略化

- バックエンドから値が取得できない場合でも、空リストを返却することでレスポンス構造を固定化する方針を確認

### Refactor / Consideration
- ログイン時のユーザー情報集約処理について、既存の `build_admin_user_list` / `resolve_teacher_display_role` の実装を参考にし、認証処理（`auth_service`）とユーザー情報集約ロジック（user_service）の責務分離を検討

- 将来的な拡張（複数担任・学年主任・教科担当）を見据えつつ、現状は「1ユーザーにつき1つの `teacher_assignment` を主に扱う」前提で設計を進める方針を整理

### Notes
- 本変更は設計・方針整理段階であり、`auth_service.login_user` への実装反映は次工程で対応予定

## 2026/02/03

### Added
- 連絡帳（Journal）機能のフロントエンド画面を追加
  - 状態管理: `stores/journal.js`
  - API 呼び出し: `journalService.js`

### Changed
- 連絡帳関連フロントエンドの構成を整理
  - 既存バックエンド API を利用する形で画面設計を調整
  - 連絡帳取得・提出処理をサービス層経由で呼び出す構成に変更
  - 表示用データ構造を API レスポンスに合わせて調整
  - 生徒向け連絡帳提出画面 `SubmitView.vue` を更新
  - 生徒向け連絡帳履歴表示画面 `HistoryView.vue` を更新

- 開発環境におけるデータ投入方針を整理
  - テーブル定義・マスタ構造とテストデータを分離する方針を明確化
  - `seed.sql` は「DB初期化に必要な最小構成」に限定
  - 日付依存・増加前提のデータは `seed.sql` に含めない方針とした

- `seed.sql` を修正
  - DB 再作成前提とし、`DELETE文` を削除
  - `subjects` の登録はマイグレーション側で管理する前提に変更
  - 学年・クラス・ユーザー・教師割当・生徒割当の初期サンプルデータ構成を整理

### Fixed
- `teacher_assignments` 登録時に `grade_id` が `NULL` になる問題を修正
  - `class_id` から `grade_id` を明示的に取得する形に修正
  - 担任・教科担当・学年主任それぞれの割当構造を ER 図 と整合させた

### Docs
- 開発環境における以下の考え方を整理
  - `seed.sql` とテストデータの役割の違い
  - 日付を持つデータを `seed` に含めない理由
  - 開発中におけるテストデータ運用の考え方（再投入・破棄前提）

## 2026/02/02

### Changed
- `__init__.py` をすべて空ファイルに変更
  - モジュール再 export による循環 import を防止するため、明示的 import のみに統一

- 認証関連の責務分離を実施
  - `routers/auth.py` からビジネスロジックを分離し、`services/auth_service.py` に集約
  - 認証依存関係（ログインユーザー取得・トークン検証）を `dependencies/` 配下へ分離
  - 共通処理を `utils/` 配下へ整理

- トークン関連処理の再構成
  - `dependencies.py` を廃止し、トークン処理を新規作成した `utils/token_utils.py` に統合
  - トークン生成・検証ロジックを一元管理する構成へ変更

## 2026/02/01

### Changed
- 認証初期化処理（initAuth）の設計を改善
  - アプリ起動時のアクセストークンリフレッシュ処理を整理
  - 未ログイン状態では refresh API の失敗をエラーとして扱わないように変更
  - 認証状態に応じた初期化フローを明確化

- 管理者向けユーザー一覧取得処理（get_admin_user_list）の内部構造を整理
  - ユーザー単位での集約処理を関数化し、SQL結果の責務を明確化
  - 教師ロール判定（担任・副担任・学年主任等）の業務ロジックを分離
  - 表示用レスポンス生成処理を切り出し、可読性・保守性を向上

## 2026/01/28

### Changed
- 認証まわりのリクエスト制御を改善
  - アクセストークン refresh 処理において発生していた無限ループの問題を修正
  - ログイン画面表示時にはトークン refresh 処理を実行しないよう挙動を変更
- フロントエンドの service 構成を見直し
  - `services/api.js` に集約されていた処理を責務ごとに分割
  - `adminService.js`、`authService.js` を新設し、運用を開始

## 2026/01/26

### Docs
- CHANGELOG の分割・整理を実施
  - 設計判断・設計方針に関する記載を Design ドキュメントへ移動
  - 認証設計に関する詳細を `docs/design/auth-design.md` に整理
  - 教師担当割当設計に関する詳細を `docs/design/teacher-assignment-design.md` に整理
  - CHANGELOG には「変更事実と参照先」を記載する方針に統一

### Changed
- 認証方式を interceptor による 401 ハンドリング中心の構成へ変更
  - アクセストークンはメモリ管理、リフレッシュトークンは HttpOnly Cookie 管理へ移行
  - フロントエンドでのリフレッシュトークン保持を廃止
  - 無操作ログアウト処理を認証ストアに集約
  - 認証初期化処理を refresh API ベースで再設計
  - 詳細設計は `docs/design/auth-design.md` を参照

### Database
- Alembic マイグレーション `d29c0dfc9e24` を作成・実行
  - `subjects` テーブルに初期教科データを登録
    - 国語、社会、数学、理科、音楽、美術、保健体育、技術・家庭、英語
  - 既存データが存在する場合も安全に挿入（`INSERT IGNORE` 使用）
  - `downgrade` 実行時には該当データを削除

## 2026/01/24

## Changed
- 認証処理を interceptor による 401 ハンドリング中心の構成へ移行
  ※ docs/design/auth-design.md を参照

## 2026/01/23

### Design
- 認証設計の見直し  
  ※ docs/design/auth-design.md を参照

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

## 2026/01/22

### Added
- subjects テーブル追加

### Changed
- 教師担当情報の正規化  
  ※ docs/design/teacher-assignment-design.md を参照

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
- トークン管理方式をアクセストークン／リフレッシュトークン構成に変更  
  ※ docs/design/auth-design.md を参照

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

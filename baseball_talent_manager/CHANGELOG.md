# CHANGELOG

## 2026-03-23

## [デプロイ] Oracle Cloud本番環境構築・デプロイ設定追加

### Added
- `frontend/Dockerfile.prod` を作成
  - マルチステージビルド（node:20-alpineでビルド → nginx:alpineで配信）
  - `npm run build` で生成した静的ファイルをnginxで配信
- `frontend/nginx.conf` を作成
  - Vue Router対応（`try_files $uri $uri/ /index.html`）
  - `/api/` へのリクエストをbackendコンテナにプロキシ
- `frontend/.env.production` を作成
  - `VITE_API_URL=`（空文字）に設定
  - 本番ビルド時にaxiosのbaseURLを相対パスにするための設定
- `docker-compose.prod.yml` を作成
  - backendの`--reload`を除いた本番用起動コマンドに変更
  - frontendをnginx（80番ポート）で配信する設定に変更

### Changed
- `frontend/src/services/api.js`
  - `baseURL`のフォールバック演算子を`||`から`??`に変更
  - 空文字（`VITE_API_URL=`）を有効な値として扱うための修正

### Infrastructure
- Oracle Cloud Always Free（Ubuntu 22.04）にデプロイ環境を構築
  - VCN・パブリックサブネット・インターネットゲートウェイ・ルート表を設定
  - VMインスタンス（VM.Standard.E2.1.Micro）を作成（IP: 168.138.193.7）
  - Docker 29.3.0 / Docker Compose v5.1.1 をインストール
  - OCIセキュリティリストで80番・22番ポートを開放
  - UFWで22番・80番ポートを許可

### Technical Notes
- 本番環境はdocker-compose.yml + docker-compose.prod.ymlの2ファイル構成
  - `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
- nginxがフロントエンド配信とAPIプロキシを兼務するため、8000番ポートの外部開放は不要
- `VITE_API_URL`が空文字の場合、axiosのbaseURLが空文字になり`/api/...`の相対パスでリクエストが送られる

## [課題2] 測定結果閲覧画面の改善

### Changed
- `frontend/src/components/MeasurementResultList.vue`
  - 部員名から学年を分離して独立した列として表示（staffのみ）
  - ヘッダークリック式ソートをドロップダウン形式に変更
    - タイトル横にソート項目選択（`<select>`）と昇順・降順切り替えボタンを追加
    - ソート対象：計測日・部員名・学年・各測定項目（11項目）
    - 部員名・学年のソート選択肢はstaffのみ表示
  - 全`<th>`に`white-space: nowrap`を追加（ヘッダー折り返し防止）
  - 絞り込み機能を追加
    - 部員名テキスト検索（大文字小文字を無視）
    - 学年選択（全て・1年・2年・3年）
    - 計測日選択（登録済みデータから年月を動的生成）
  - ページネーション機能を追加
    - 表示件数切り替え（10件・20件・50件）
    - ページ送りボタン（←・→）
    - 総ページ数表示
  - フィルタ・ソート条件をURLクエリパラメータに同期
  - リセットボタンを追加（条件未設定時は無効化）
  - `compareValues`関数を分離してソートロジックを整理
  - computedの依存関係を整理（measurements → availableDates → filteredMeasurements → sortedMeasurements → paginatedMeasurements）

## [バグ修正] AppHeader.vueのログアウト処理を修正

### Fixed
- `frontend/src/components/AppHeader.vue`
  - `handleLogout()`に`router.push("/login")`を追加
  - `useRouter`のimportを追加
  - 修正前：ログアウト後にログイン画面へ遷移しない不具合があった
  - 修正後：ログアウト後に正常にログイン画面へ遷移するようになった

## 2026-03-19

## [動作確認・バグ修正] seed.sql適用・各機能の動作確認

### Added
- `seed.sql` を作成（プロジェクトルート）
  - ユーザー：マネージャー2名・コーチ1名・監督1名・部員15名（各学年5名）
  - 測定記録：過去3回分（2025-08・10・12月）全部員approved
  - 第4回測定（2026-02月）：approved・pending_coach・pending_member・rejected・draft混在
- `docs/proposal.md` を作成
  - 課題2提案内容・運用ルール整備をまとめた
- `scripts/generate_hash.py` を作成（Argon2ハッシュ生成用）

### Changed
- `docker-compose.yml`
  - `networks` 設定を追加（app-network）
  - `backend` に `depends_on: db` を追加
- `backend/alembic/env.py`
  - `config.set_main_option("sqlalchemy.url", DATABASE_URL)` のコメントアウトを解除
- `docker-compose.dev.yml`
  - `- ./scripts:/app/scripts` のボリューム設定を削除
- `backend/app/schemas/auth.py`
  - `TokenRefreshResponse` にユーザー情報（user_id・name・grade・role）を追加
- `backend/app/schemas/user.py`
  - `UserListItem` に `status` を追加
- `backend/app/services/auth_service.py`
  - `refresh_access_token()` をDBからユーザー情報を取得して返す形に変更
- `backend/app/services/user_service.py`
  - `get_user_list()` に `User.status` を追加
- `backend/app/routers/auth.py`
  - `refresh` エンドポイントに `db` 引数を追加
- `frontend/src/services/api.js`
  - レスポンスインターセプターに `/api/auth/refresh` が401の場合のループ防止処理を追加
- `frontend/src/views/LoginView.vue`
  - ログイン失敗時のエラーメッセージをエラー種別（401・422・ERR_NETWORK）で出し分け
  - テストアカウントのメールアドレスをseed.sqlと一致させるよう修正
- `frontend/src/stores/auth.js`
  - `refreshAccessToken()` にユーザー情報（role・userId・userName・member_grade）の復元処理を追加
  - `login()` / `refreshAccessToken()` で `sessionStorage` に `tokenExpiry` を保存
  - `logout()` で `sessionStorage` の `tokenExpiry` を削除
  - `maybeLoggedIn` が `sessionStorage` の `tokenExpiry` も参照するよう変更
  - `initAuth()` で `sessionStorage` から `tokenExpiry` を復元する処理を追加

### Technical Notes
- ページリロード時の認証状態維持はRefresh Token（HttpOnly Cookie）+ sessionStorage（tokenExpiry）の組み合わせで実現
- accessTokenはセキュリティ上メモリ保存のまま維持

## 2026-03-13

## [フロントエンド] API接続実装

### Added
- `frontend/.env` を作成
  - `VITE_API_URL=http://localhost:8000`
- `frontend/src/services/api.js` を作成
  - axiosインスタンス設定
  - リクエストインターセプター（Access Token自動付与）
  - レスポンスインターセプター（401エラー時のRefresh Token自動更新）
- `frontend/src/services/authService.js` を作成
  - `login()` / `refreshAccessToken()` / `logout()`
- `frontend/src/services/measurementService.js` を作成
  - `createMeasurement()` / `getMeasurements()` / `submitMeasurement()` / `memberApprove()` / `coachApprove()`
- `frontend/src/services/userService.js` を作成
  - `createUser()` / `getUsers()` / `updateUserStatus()`

### Changed
- `frontend/src/stores/auth.js` を更新
  - `auth.full.js` の内容に差し替え
  - `tokenExpiry` によるトークン有効期限管理
  - `startInactivityTimer()` による無操作時自動ログアウト（30分）
  - `initAuth()` をRefresh Token対応に更新
- `frontend/src/components/AppHeader.vue` を更新
  - 未使用の `useRouter` を削除
- `frontend/src/views/manager/MeasurementResultSubmit.vue` を更新
  - `dummyMembers` → `getUsers()` APIに変更
  - `handleSubmit` を `createMeasurement()` + `submitMeasurement()` に接続
  - `MEASUREMENT_FIELDS` のキー名をスネークケースに統一
- `frontend/src/views/manager/MeasurementStatusList.vue` を更新
  - `dummyMeasurements` → `getMeasurements()` APIに変更
- `frontend/src/components/MeasurementResultReview.vue` を更新
  - `dummyMeasurements` → `getMeasurements()` APIに変更
  - `handleApprove()` / `handleReject()` を `memberApprove()` / `coachApprove()` に接続
- `frontend/src/components/MeasurementResultList.vue` を更新
  - `dummyMeasurements` → `getMeasurements()` APIに変更
- `frontend/src/components/MemberCreate.vue` を更新
  - `handleRegister()` を `createUser()` APIに接続
- `frontend/src/components/MemberRetire.vue` を更新
  - `dummyMembers` → `getUsers()` APIに変更
  - `handleProcess()` を `updateUserStatus()` APIに接続

### Backend Changed
- `backend/app/schemas/user.py`
  - `UserStatusUpdateRequest` を追加
- `backend/app/services/user_service.py`
  - `update_user_status()` を追加
- `backend/app/routers/users.py`
  - `PATCH /api/users/{user_id}/status` エンドポイントを追加
- `docs/api.md`
  - セクション4.3「部員ステータス更新」を追加

### Changed
- `.gitignore` を更新
  - Python関連・`.env` の除外設定を追加
- `frontend/.gitignore` を削除（プロジェクトルートに統一）
- `frontend/package.json`
  - `axios` を追加

## 2026-03-12

## [バックエンド] サービス層・ルーター実装完了

### Added
- `backend/app/services/measurement_service.py` を作成
  - `create_measurement()` - 測定記録登録
  - `get_measurements()` - 測定記録取得（ロール別分岐）
  - `get_measurement_by_id()` - measurement_idによる測定記録取得
  - `submit_measurement()` - 承認フロー発行
  - `member_approve()` - 部員による承認・否認
  - `coach_approve()` - コーチによる最終承認・否認
- `backend/app/routers/measurements.py` を作成
  - `POST /api/measurements` - 測定記録登録（manager）
  - `GET /api/measurements` - 測定記録取得（全ロール）
  - `POST /api/measurements/{measurement_id}/submit` - 承認フロー発行（manager）
  - `PATCH /api/measurements/{measurement_id}/member-approve` - 部員承認・否認（member）
  - `PATCH /api/measurements/{measurement_id}/coach-approve` - コーチ承認・否認（coach）
- `backend/app/main.py` を作成
  - FastAPIアプリケーション設定
  - CORSミドルウェア設定
  - ルーター登録（auth・users・measurements）
- `backend/requirements.txt` を作成

### Changed
- `backend/app/schemas/measurement.py`
  - `MeasurementSubmitResponse` を追加
  - `MeasurementListResponse` を追加

### Technical Notes
- `get_measurements()` はJOINでUserの`name`・`grade`を取得
- 承認フローのステータス遷移：draft → pending_member → pending_coach → approved（rejected）
- `requirements.txt` は `pipreqs` で生成

### Next
- フロントエンド実装（モックUIからAPI接続への移行）
  - 画面骨格
  - ルーティング
  - API接続
  - 状態管理
  - UI改善

## 2026-03-11

## [バックエンド] サービス層・ルーター実装

### Added
- `backend/app/schemas/user.py` を作成
  - `UserCreateRequest` / `UserResponse` / `UserListItem` / `UserListResponse` を定義
- `backend/app/schemas/measurement.py` を作成
  - `MeasurementCreateRequest` / `MeasurementCreateResponse` / `MeasurementItem` / `ApproveRequest` / `ApproveResponse` を定義
- `backend/app/schemas/auth.py` を更新
  - `TokenRefreshResponse` を追加
- `backend/app/utils/security.py` を作成
  - パスワードハッシュ化・検証（Argon2）
  - Access Token / Refresh Token 生成・デコード（JWT）
- `backend/app/dependencies/__init__.py` を作成
- `backend/app/dependencies/auth.py` を作成
  - `get_current_user` / `require_roles` を定義
- `backend/app/services/__init__.py` を作成
- `backend/app/services/auth_service.py` を作成
  - `login_user` / `refresh_access_token` / `authenticate_user` を定義
- `backend/app/services/user_service.py` を作成
  - `create_user` / `get_user_by_email` / `get_user_list` を定義
- `backend/app/routers/__init__.py` を作成
- `backend/app/routers/auth.py` を作成
  - `POST /api/auth/login` / `POST /api/auth/refresh` / `POST /api/auth/logout`
- `backend/app/routers/users.py` を作成
  - `POST /api/users` / `GET /api/users`

### Changed
- `backend/.env`
  - `DATABASE_URL` のDB名を `journal_system` から `baseball_talent_manager` に修正
  - `ACCESS_TOKEN_EXPIRE_MINUTES` を `1440` から `30` に変更
  - `REFRESH_TOKEN_EXPIRE_DAYS=7` を追加
- `.gitignore`
  - Python関連（`__pycache__/` / `.venv/` など）と `.env` の除外設定を追加

### Technical Notes
- `expires_in` は秒単位で統一（`ACCESS_TOKEN_EXPIRE_MINUTES * 60`）
- `services/` にビジネスロジック + DBアクセスを記述、`crud/` への分割は課題2で対応予定
- メールアドレスは登録・検索時に `lower()` で小文字統一

## 2026-03-10


## [リファクタリング] モックUIコンポーネントのcomputed統一

### Changed
- `MeasurementResultSubmit.vue`
  - `members`を`ref`から定数`MEMBERS`に変更
  - 測定項目のキー名をスネークケースに統一（例：`sprint50m` → `sprint_50m`）
- `MeasurementStatusList.vue`
  - `measurements`を`ref`から定数に変更
  - `hasMeasurements`を`computed`で実装
  - `getStatus`関数を追加（不明なステータスのフォールバック対応）
- `MeasurementResultReview.vue`
  - `measurements`を`ref`+`onMounted`から`computed`ベースに変更
  - `APPROVE_STATUS`オブジェクトでロール別の承認後ステータスを管理
- `MemberRetire.vue`
  - `members`の`ref`を削除し`dummyMembers`を直接参照
  - `activeMembers`を`computed`に変更

### Technical Notes
- `ref`は「ユーザー操作で変化する値」（showModal・successMessageなど）にのみ使用
- `computed`は「既存データから派生する値」（フィルタリング結果など）に使用
- 変更されない値（dummyDataのimport・定数など）は`ref`・`computed`不要

## [バックエンド] モデル・スキーマ実装開始

### Added
- `backend/app/models/__init__.py` を作成
- `backend/app/models/user.py` を作成
  - `User` モデル（usersテーブル対応）
  - `Measurement` との双方向 `relationship` を定義
- `backend/app/models/measurement.py` を作成
  - `Measurement` モデル（measurementsテーブル対応）
  - `user_id` に `index=True` を追加（検索頻度が高いため）
  - `User` との双方向 `relationship` を定義
- `backend/app/schemas/__init__.py` を作成
- `backend/app/schemas/auth.py` を作成
  - `LoginRequest` / `LoginResponse` を定義

### Changed
- `backend/alembic/versions/001_create_users.py`
  - `updated_at` の `onupdate=sa.func.now()` を削除
- `backend/alembic/versions/002_create_measurements.py`
  - `updated_at` の `onupdate=sa.func.now()` を削除
  - `ix_measurements_user_id` インデックスを追加

### Technical Notes
- `created_at` / `updated_at` をPython側（`datetime.now(timezone.utc)`）で統一管理
  - `onupdate=sa.func.now()` はMySQLで効かないケースがあるため
  - DBサーバーのタイムゾーン設定に依存しないようUTCを明示

## 2026-03-09

## [課題1] モックUI実装完了

### Added
- `views/LoginView.vue` - ログイン画面
- `views/shared/DashboardView.vue` - 部員・コーチ・監督共通ダッシュボード
- `views/manager/DashboardView.vue` - マネージャー専用ダッシュボード
- `views/manager/MeasurementResultSubmit.vue` - 測定結果入力フォーム
  - バリデーション（未入力チェック）
  - 測定項目を走力・肩力・打力・筋力のカードでグループ化
  - 送信時のローディングフラグ・成功メッセージ表示
- `views/manager/MeasurementStatusList.vue` - 承認ステータス一覧
  - ステータスバッジ（approved/pending_member/pending_coach/rejected）
- `components/AppHeader.vue` - 共通ヘッダー
- `components/MeasurementResultReview.vue` - 測定結果の承認・否認
  - 部員：自身のpending_memberレコードを表示
  - コーチ：全部員のpending_coachレコードを表示
- `components/MeasurementResultList.vue` - 測定記録閲覧
  - 全ロール共通コンポーネント（computedベースでロール別フィルタリング）
  - 部員：自身のapprovedレコードのみ表示
  - スタッフ（manager/coach/director）：全部員のapprovedレコードを表示
- `components/MemberManagement.vue` - 部員管理メニュー
- `components/MemberCreate.vue` - 部員作成フォーム
  - バリデーション（未入力・メール形式チェック）
  - 確認モーダルによる登録フロー
- `components/MemberRetire.vue` - 部員退部・引退処理
  - 退部（withdrawn）・引退（retired）の別ステータス管理
  - 確認モーダルによる処理フロー
  - 処理後はcomputedにより一覧から自動除外

### Changed
- `router/index.js`
  - ナビゲーションガードを`next()`から`return`ベースに修正（Vue Router非推奨警告対応）
  - コーチ・監督ルートに部員管理・部員作成・退部引退処理を追加
- `vite.config.js`
  - `server.watch.usePolling: true` を追加（Docker環境でのホットリロード有効化）

### Technical Notes
- `MeasurementResultList.vue` より `computed` ベースの reactivity パターンを採用
- 課題1完了後に既存コンポーネント（`MeasurementResultSubmit`・`MeasurementStatusList`・`MeasurementResultReview`）を`computed`ベースへリファクタリング予定
- 重複チェック等のバックエンドバリデーションは課題2で実装予定

### Deferred to 課題2
- 検索・ソート機能
- チーム全体の傾向可視化ダッシュボード
- スマートフォン対応レイアウト
- `MeasurementResultList.vue` のロール別コンポーネント分割
- 複数部員の一括登録・一括引退処理

## 2026-03-04

### Added
- views/manager/MeasurementResultSubmit.vue作成
  - 測定結果入力フォーム（部員選択・計測日・走力・肩力・打力・筋力）
  - バリデーション（未入力項目の赤枠表示）
  - 送信処理（成功メッセージ表示）
- views/manager/MeasurementStatusList.vue作成
  - 承認フローステータス一覧（テーブル形式）
  - ステータスバッジ色分け表示

### Changed
- vite.config.jsにserver設定追加（usePolling: trueによるホットリロード有効化）

## 2026-03-03

### Added
- モックUI作成を継続
  - services/authService.js を作成（モックUI用仮実装）
    - dummyUsersからメールアドレスで検索してAPIレスポンスを模倣
    - refreshAccessToken・logout の仮実装
  - stores/auth.js を作成（モックUI用）
    - stores/auth.full.js にフロントエンド実装用を保存
  - components/AppHeader.vue を作成
    - ロール別ナビゲーションメニュー
    - パンくずリスト表示
    - ユーザー名・ロールアイコン表示
    - ログアウトボタン
  - views/LoginView.vue を作成
    - メールアドレス・パスワード入力フォーム
    - テストアカウント一覧表示
  - views/shared/DashboardView.vue を作成
    - ロール別カード表示（測定結果確認・測定記録閲覧・部員管理）

- ESLint v9（Flat Config: eslint.config.js）を導入
- eslint-plugin-vue を追加し、Vue 3 対応のLintルールを適用
- Prettier を導入し、コードフォーマットを統一
- eslint-plugin-prettier / eslint-config-prettier を追加（ESLint主導構成）
- npm scripts を追加
  - lint
  - lint:fix
- .prettierrc を作成（改行コードを LF に統一）

### Changed
- router/index.js を更新
  - MemberList.vue のルートを追加（coach・director）
  - members/create・members/retire のbreadcrumbsを部員管理画面に変更
  - パス名を修正
    - submit → record（測定結果の入力）
    - statuslist → status（ステータス確認）
    - resultreview → review（測定結果の確認と承認）
    - userscreate/usersretire → members/create・members/retire
- フォーマット方式を「Prettier単体実行」から「ESLint主導の自動修正方式」に変更
- VSCode設定を変更
  - editor.formatOnSave: false
  - editor.codeActionsOnSave.source.fixAll.eslint: true
- 改行コードを CRLF から LF に統一

### Fixed
- 改行コード不一致（CRLF/LF）による全行エラー表示を解消
- 未使用変数（no-unused-vars）エラーを修正
  - 未使用の ref / router を削除
  - 未使用引数に _ を付与
  - catch 内の未使用変数を修正
- バックアップファイル（AppHeader copy.vue）によるLintエラーを解消
- Vite起動時の500エラーを解消
  - 原因：pinia・vue-routerがコンテナ内にインストールされていなかった
  - 対策：Dockerfile.dev と docker-compose.dev.yml のボリューム設定を調整し
          node_modules が上書きされないよう修正
- プロジェクト内importエラーを解消
  - 原因：Viteが @/stores/auth や @/components/ を解決できなかった
  - 対策：vite.config.js に resolve.alias を追加
          src配下のファイルパスの存在確認と大文字小文字の修正

### Notes
- Docker + Vite環境ではホスト側ソースマウントとnode_modulesの上書きに注意
- エイリアス @ は vite.config.js で明示的に指定することでimportエラーを防止
- 今回の修正でフロントエンドの開発環境が安定して起動可能になった

## 2026-03-02

### Added
- Docker環境を構築
  - docker-compose.yml を作成
  - docker-compose.dev.yml を作成
  - mysql/Dockerfile を作成
  - mysql/conf.d/my.cnf を作成
  - backend/Dockerfile を作成
  - frontend/Dockerfile.dev を作成
  - scripts/wait_for_db.py を作成

- Alembic環境を構築
  - alembic.ini を作成
  - alembic/env.py を作成
  - alembic/versions/001_create_users.py を作成
  - alembic/versions/002_create_measurements.py を作成

- バックエンド環境を構築
  - backend/app/db.py を作成
  - backend/.env を作成

- モックUI作成を開始
  - frontend/src/dummyData.js を作成
    - 仮ユーザーデータ（manager・member・coach・director）
    - 仮部員一覧データ
    - 仮測定記録データ（approved・pending_member・rejected を混在）
  - frontend/src/router/index.js を作成中
    - 課題1の画面ルートを定義
    - ロール別ルート構成（manager・member・coach・director）
    - メタ情報（requiresAuth・role・title・breadcrumbs）を定義

- 画面一覧サマリの記載内容に合わせて各コンポーネント（空ファイル）を作成

### Changed
- マイグレーションを実行
  - usersテーブルを作成
  - measurementsテーブルを作成
- frontend/src/main.js を更新
  - stores/auth のインポートをコメントアウト（モックUI段階のため）
- frontend/src/App.vue を更新
  - AppHeader コンポーネントの組み込み
  - ログイン画面・404画面ではヘッダーを非表示にする処理を追加


## 2026-03-01

### Added
- 認証設計書を追加
  - docs/auth_design.md を作成
- ロール権限マトリクスを追加
  - docs/role_matrix.md を作成

### Changed
- api.md を更新
  - 5.2 測定記録取得の備考にロール別返却データ制御を追記
    - member：自身の測定記録のみ返す
    - manager | coach | director：全部員の測定記録を返す
    - バックエンドでJWTトークンのロールを検証して制御する

## 2026-02-28

### Added
- 承認依頼ステータス確認画面を追加
  - MeasurementStatusList.vue を新規追加（課題1）
  - manager/DashboardView.vue の遷移先に追加
  - MeasurementResultSubmit.vue の遷移先に追加
- APIドキュメントを追加
  - docs/api.md を作成

### Changed
- screens.md を更新
  - MeasurementRejection.vue を削除
    - 否認後の再作成は MeasurementResultSubmit.vue で対応
  - MeasurementResultList.vue に再作成ボタンの遷移先を追加
    - rejected ステータスのみ再作成ボタンを表示
    - 再作成ボタン押下で MeasurementResultSubmit.vue へ遷移
  - MeasurementResultGraph.vue を課題2へ変更
  - 各画面に課題1 / 課題2の区分を追加
  - MeasurementStatusList.vue のファイル構成を整理
    - manager/ 配下の独立したファイルとして記載
- usecase.md を更新
  - 各ユースケースに課題1 / 課題2の区分を追加
  - マネージャーの測定結果入力を1名ずつ入力する仕様に変更（課題1）
  - 複数部員一括入力をページネーション対応と共に課題2へ移動
  - 3年生一括引退処理を課題2へ移動
- api.md を更新
  - 認証系API（ログイン・トークン再発行・ログアウト）を定義
  - 承認フロー管理APIを定義
  - 部員管理APIを定義
  - 測定記録管理APIを定義

## 2026-02-26

### Added
- ユースケース整理ドキュメントを追加
  - docs/usecase.md を作成

- PoC機能一覧ドキュメントを追加
  - docs/functions.md を作成

- 画面一覧ドキュメントを追加
  - docs/screens.md を作成

### Changed
- usecase.md を更新
  - グラフ表示の備考に「表示方法は項目別のみ（項目混合は対象外）」を追記
  
## 2026-02-24

### Added
- PoC機能一覧ドキュメントを追加
  - docs/functions.md を作成

- 画面設計ドキュメントを追加
  - docs/screens.md を作成

- 参考資料フォルダを追加
  - docs/reference_materials/ を作成
  - 課題PDF・記録ファイルを格納

- フロントエンド雛形を作成
  - Viteプロジェクトを初期化
  - App.vue / main.js を作成
  - 基本構成をセットアップ

### Changed
- READMEを更新
  - 開発状況を記載
  - 設計ドキュメント一覧を追加
  - ディレクトリ構成を追加
  - 参考資料説明を追加
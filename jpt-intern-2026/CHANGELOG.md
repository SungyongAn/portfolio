# CHANGELOG

## [docs/update-design-documents] - 2026-06-22

### Changed

#### ER設計・ステータス設計の更新

- `doc/db/er_design.md`
  - `ExpenseType` の `EQUIPMENT` の説明を「機材費」→「機器・備品」に修正（実装コメントに統一）

- `doc/db/status_design.md`
  - 操作権限テーブルの「着手」の実行可能ロールを「全ロール」→「APPLICANT / DEPT_MANAGER / HQ_MANAGER」に修正（TASK_MEMBERは着手不可）

#### テーブル定義の更新

- `doc/db/tables/expenses.md`
  - 経費種別定義の `EQUIPMENT` の表示名を「機材費」→「機器・備品」に修正

#### API設計の更新

- `doc/design/api_design.md`
  - ユーザーAPIの対象ロールを修正
    - `GET /users`・`GET /users/{user_id}`・`POST /users` を `HQ_MANAGER` のみに変更
    - `POST /users`（ユーザー作成）・`GET /users/{user_id}`（ユーザー詳細取得）を追記
    - `GET /users` のクエリパラメータセクションを削除（実装に存在しないため）
  - 部門APIに `GET /departments/{department_id}/tasks`（部門内タスク一覧取得）を追加

#### 機能一覧の更新

- `doc/design/functions.md`
  - `F-TSK-01` タスク登録・削除の対象ロールを「APPLICANT / DEPT_MANAGER」→「APPLICANT / DEPT_MANAGER / HQ_MANAGER」に修正
  - `F-TSK-02` タスク更新の対象ロールを「APPLICANT / DEPT_MANAGER / TASK_MEMBER」→「APPLICANT / TASK_MEMBER」に修正
  - `F-BDG-02` 直接経費入力の説明を「機材費」→「機器費」に修正

#### ロール権限マトリクスの更新

- `doc/design/role_matrix.md`
  - 機能別権限マトリクスの「タスクの登録・削除」本部管理者を `❌` → `✅` に修正
  - 機能別権限マトリクスの「タスクの更新」部門管理者を `✅` → `❌` に修正
  - 補足・設計判断の記載を実装に合わせて修正
    - 「部門管理者・本部管理者は進捗・予算の編集は行わず」→「タスク更新は申請者・担当者のみ実行可能」に変更
    - 「タスク登録・削除は申請者・部門管理者・本部管理者が実行可能」を追記

#### 画面一覧・画面遷移の更新

- `doc/design/screens/screen-list.md`
  - `S-APP-02` 案件申請画面の説明に「Drawer表示」を追記
  - `S-APP-03` 案件詳細画面の関連機能IDから `F-TSK-02` を削除（タスク更新はインラインDialogのため）
  - `S-TSK-01` のタイトルを「タスク登録・更新画面」→「タスク登録画面」に修正
  - `S-BDG-04` 予算管理一覧画面（DEPT_MANAGER / HQ_MANAGER）を追加
  - `S-MBR-01` メンバータスク状況画面（DEPT_MANAGER）を追加
  - `TASK_MEMBER` ロールをロール定義に追加
  - 設計方針にタスク更新はインラインDialogで完結する旨を追記
  - ファイル構成の `budget.md` に `S-BDG-04` を追加

- `doc/design/screens/navigation.md`
  - 案件申請Drawer（`/?action=create-project`）の導線を追記
  - タスク更新Dialog（インライン表示）を追記
  - 予算管理一覧画面（S-BDG-04）を追記
  - メンバータスク状況画面（S-MBR-01）を追記

#### 各画面設計ファイルの更新

- `doc/design/screens/screens/auth.md`
  - 備考のトークン管理方式を修正
    - 「アクセストークンはメモリ管理・リフレッシュトークンはhttpOnly Cookie」→「両方とも sessionStorage で管理」に変更
  - 「WebSocket通知接続時はアクセストークンをURLクエリパラメータで渡す」を追記

- `doc/design/screens/screens/dashboard.md`
  - 使用APIに `GET /dashboard/alerts`（アラート案件一覧取得）を追加

- `doc/design/screens/screens/project.md`
  - 対象ロールを「APPLICANT / DEPT_MANAGER / HQ_MANAGER」→「全ロール」に修正
  - 表示項目に「アラートレベル」「予算消化率」を追加・「遅延フラグ」を削除
  - フィルター・検索セクションを新規追加（キーワード検索・ステータス・部門・アラートレベル・ページネーション）
  - 操作から「新規申請」を削除（案件申請はダッシュボードのDrawerが主導線のため）
  - バリデーション / 制御に `TASK_MEMBER`（自部門のみ）を追加
  - URLクエリパラメータによる初期フィルター反映の記載を追加
  - 使用APIに `GET /departments` を追加
  - 備考に「案件申請はダッシュボードのDrawerが主導線」を追記

- `doc/design/screens/screens/project_apply.md`
  - 表示方式の起動元から「案件一覧「新規申請」」を削除
  - 入力項目「概算予算（万円）」→「概算予算（円）」に修正
  - 入力項目「人月単価（万円）」を削除（予算登録時に入力するため）
  - 画面遷移 / 表示制御から「案件一覧「新規申請」選択」を削除
  - 関連機能から「案件一覧」を削除
  - 備考に「人月単価は案件申請時ではなく予算登録時（S-BDG-01）に入力する」を追記

- `doc/design/screens/screens/project_detail.md`
  - 表示項目「概算予算額（万円）」→「概算予算（円）」に修正
  - 表示項目「人月単価（万円）」を削除
  - 表示項目「遅延フラグ」→「アラートレベル」に修正
  - 操作に「案件編集」「着手」「完了」「タスク更新」を追加
  - タスク登録とタスク更新の操作を分離（登録は専用画面・更新はインラインDialog）
  - バリデーション / 制御に `TASK_MEMBER`（自部門のみ）を追加
  - 使用APIに `PUT /projects/{project_id}/tasks/{task_id}`・`PATCH /projects/{project_id}/start`・`PATCH /projects/{project_id}/complete` を追加
  - 備考にタスク更新・削除はインラインDialogで完結する旨を追記

- `doc/design/screens/screens/approval.md`
  - 表示項目「目的・概要」を削除・「ステータス」を追加
  - 表示項目「概算予算額（万円）」→「概算予算」に修正
  - 入力項目「コメント」を削除（APIに存在しないため）
  - バリデーションに「500字以内」「二重送信防止」を追記
  - 使用APIを修正
    - `POST /projects/{project_id}/approval/approve` / `POST /projects/{project_id}/approval/reject` → `POST /projects/{project_id}/approve`（単一エンドポイント）に統一
    - `GET /projects/{project_id}` を追加
  - 備考に `reject_reason` の有無で承認・却下を判定する旨を追記

- `doc/design/screens/screens/task.md`
  - タイトルを「タスク登録・更新画面」→「タスク登録画面」に修正
  - 入力項目に「工程名」（必須）を追加
  - 操作から「更新」「削除」を削除（インラインDialogで実行のため）
  - バリデーションに「タスク更新・削除はS-APP-03のインラインDialogで実行」を追記
  - 使用APIに `GET /projects/{project_id}`・`GET /users/department/{department_id}` を追加
  - タスク更新・削除のAPIを削除
  - 備考にタスク更新・削除はTaskDetailDialog（インライン表示）で完結する旨を追記

- `doc/design/screens/screens/budget.md`
  - S-BDG-01：予算管理画面
    - 表示項目「予算工数」→「計画工数」に修正
    - 工数実績一覧・直接経費一覧の表示項目を追加
    - 操作に「工数実績編集・削除」「直接経費編集・削除」を追加
    - 使用APIに `GET /projects/{project_id}`・工数実績・直接経費の取得・削除APIを追加
    - 承認前ステータスでAPIを呼び出さない制御を追記
  - S-BDG-02：工数実績入力・編集画面
    - タイトルを「入力画面」→「入力・編集画面」に修正
    - 入力項目「備考」を削除（実装に存在しないため）
    - 編集モード（worklog-edit）の記載を追加
    - 使用APIに工数実績更新・案件情報取得を追加
  - S-BDG-03：直接経費入力・編集画面
    - タイトルを「入力画面」→「入力・編集画面」に修正
    - 入力項目「金額（万円）」→「金額（円）」に修正
    - 発生日のバリデーション（未来の日付・案件開始日より前は不可）を追記
    - 編集モード（expense-edit）の記載を追加
    - 使用APIに直接経費更新・案件情報取得を追加
  - S-BDG-04：予算管理一覧画面を新規追加
    - 対象ロール：DEPT_MANAGER / HQ_MANAGER
    - 表示項目・フィルター・検索・操作・使用APIを定義

- `doc/design/screens/screens/notification.md`
  - 使用APIのメソッドを `POST` → `PUT` に修正
  - 既読化エンドポイントを `/notifications/read` → `/notifications/{notification_id}/read` に修正
  - WebSocket接続エンドポイント `GET /notifications/ws?token={token}` を追加
  - WebSocket自動再接続の仕様（最大10回・5秒間隔）を追記

#### ユースケースの更新

- `doc/usecases/usecase_applicant.md`
  - UC-A05 タスク登録に「工程名」（必須）を追加
  - UC-A05 タスク更新・削除はS-APP-03のインラインDialogで完結する旨を追記
  - UC-A06 工数実績の入力項目「備考」を削除
  - UC-A07 経費種別の「EQUIPMENT」の説明を「機材費相当」→「機器・備品」に修正
  - UC-A08 「予算工数」→「計画工数」に修正

- `doc/usecases/usecase_dept_manager.md`
  - UC-D03 「消化率が100%以上で危険」→「100%以上で超過」に修正
  - UC-D05 部門メンバーのタスク状況確認を新規追加
    - メンバー別サマリーカード表示（担当タスク件数・進行中・完了・未着手・期限超過・完了率）
    - メンバーフィルター・ステータスフィルターによる絞り込み

- `doc/usecases/usecase_hq_manager.md`
  - UC-H02 絞り込み条件に「部門フィルター」を追記
  - UC-H03 「消化率が100%以上で危険」→「100%以上で超過」に修正
  - UC-H03 「部門フィルター・予算帯フィルター」を追記
  - UC-H05 ダッシュボードによる全社KPI監視を新規追加
    - 全社KPIサマリーカード確認
    - 部門別グラフ（案件数・予算消化率・期限超過タスク件数）
    - 注視案件一覧（アラートレベル・注視理由・SPI・CPI）
    - 部門別ドリルダウン機能

**修正ファイル：**

- `doc/db/er_design.md`
- `doc/db/status_design.md`
- `doc/db/tables/expenses.md`
- `doc/design/api_design.md`
- `doc/design/functions.md`
- `doc/design/role_matrix.md`
- `doc/design/screens/screen-list.md`
- `doc/design/screens/navigation.md`
- `doc/design/screens/screens/auth.md`
- `doc/design/screens/screens/dashboard.md`
- `doc/design/screens/screens/project.md`
- `doc/design/screens/screens/project_apply.md`
- `doc/design/screens/screens/project_detail.md`
- `doc/design/screens/screens/approval.md`
- `doc/design/screens/screens/task.md`
- `doc/design/screens/screens/budget.md`
- `doc/design/screens/screens/notification.md`
- `doc/usecases/usecase_applicant.md`
- `doc/usecases/usecase_dept_manager.md`
- `doc/usecases/usecase_hq_manager.md`

## [chore/ci-alembic-check] - 2026-06-19

### Added

#### CIへのマイグレーション作成漏れチェック追加

- `.github/workflows/ci.yml` の `backend-and-type-check` ジョブに `マイグレーションファイル作成漏れチェック` ステップを追加
  - `alembic check` によりモデル変更に対応するマイグレーションファイルの作成漏れを自動検知
  - `pytest 実行` の直後・`バックエンド起動` の前に配置し、マイグレーション適用済み状態でチェックを実行
  - 作成漏れ検知時は `❌` を表示してCIを失敗させ、マージを防止

### Fixed

#### `deploy_check.sh` のマイグレーションチェック強化・構文修正

- `[5] Alembic Migration Check` を以下の内容に更新
  - `alembic current` による現在の適用状態の表示
  - `alembic heads` と `alembic current` を比較し未適用マイグレーションを検知
  - 未適用時は `heads` / `current` の値と対応手順（`alembic upgrade head`）を表示
  - `fi` が抜けていた構文エラーを修正（`[6]` 以降が実行されない問題を解消）

**修正ファイル：**

- `.github/workflows/ci.yml`
- `deploy_check.sh`

## [chore/ci-setup] - 2026-06-19

### Added

#### GitHub Actions CI の導入

- `.github/workflows/ci.yml` を新規作成し、以下の4ジョブで構成されるCIパイプラインを構築

**`frontend-build`：フロントエンドビルドチェック**

- `npm ci` → `npm run build`（vue-tsc + vite build）を自動実行
- pushおよびPR時に型エラー・ビルドエラーを自動検知

**`backend-and-type-check`：バックエンドテスト・型生成 → フロントビルド**

- Ruff によるPythonコード品質チェック
- pytest による32件のユニットテスト自動実行
- FastAPIを起動しOpenAPI仕様（`openapi.json`）を自動取得
- `openapi-typescript-codegen` による型自動生成
- 型生成後のフロントビルドチェック（APIスキーマとフロントの型整合性を確認）

**`docker-build`：Dockerイメージビルドチェック**

- フロントエンド（`Dockerfile.prod`）・バックエンド（`Dockerfile`）のイメージビルドを自動確認
- `ghcr.io` へのログインと `--cache-from` によるビルドキャッシュを導入し実行時間を短縮

**`e2e-test`：E2Eテスト**

- Playwright（chromium）によるブラウザ自動操作テストを導入
- `backend-and-type-check` 成功後に実行
- マイグレーション・seedデータ投入後にバックエンドを起動してテストを実行
- 失敗時はスクリーンショット・動画を `playwright-report` としてアーティファクト保存（7日間保持）

**`notify-result`：PR結果通知**

- 全ジョブの結果をPRコメントへ自動投稿
- 成功（✅）・失敗（❌）をテーブル形式で表示

#### E2Eテスト環境の構築

- `@playwright/test` を導入
- `frontend/playwright.config.ts` を新規作成
  - テストディレクトリ：`frontend/e2e/`
  - ブラウザ：chromium（headless）
  - 失敗時にスクリーンショット・動画を保存する設定を追加
- `frontend/e2e/helpers/auth.ts` を新規作成
  - テストアカウント定数（`TEST_ACCOUNTS`）を定義
  - ログイン共通処理（`login()`）を実装
- `frontend/e2e/auth.spec.ts` を新規作成
  - APPLICANTでのログイン確認
  - 誤パスワードでのログイン失敗確認
  - 未ログイン時のリダイレクト確認
- `frontend/e2e/project.spec.ts` を新規作成
  - 案件申請（APPLICANT）→ 一次承認（DEPT_MANAGER）→ 最終承認（HQ_MANAGER）の一連フローを自動確認
- `frontend/e2e/budget.spec.ts` を新規作成
  - APPLICANTによる工数実績入力フローを自動確認
- `frontend/package.json` に `test:e2e` スクリプトを追加

### Changed

#### TypeScript設定の整理

- ルートの `quest_1/tsconfig.json` を削除
  - 誤って作成されたファイルと判断（`frontend/tsconfig.json` で独立管理するため不要）
- `frontend/tsconfig.json` を新規作成（`tsconfig.app.json` / `tsconfig.node.json` を参照）
- `frontend/tsconfig.node.json` の `include` に `playwright.config.ts` を追加

### Notes

#### CI設計上の工夫点

- MySQLのヘルスチェックを `mysqladmin ping -h localhost -uroot -proot` に強化し、起動直後の失敗を防止（`health-retries: 20`）
- FastAPIを `nohup` + PIDファイルで起動し、`if: always()` による確実な停止処理を追加
- `backend-and-type-check` と `e2e-test` のMySQLを別ジョブで独立起動し、ジョブ間の依存による待機時間を最小化
- `ruff` は `requirements.txt` に含まれていないため `pip install ruff` を明示的に追加
- `alembic/env.py` で `DATABASE_URL` 環境変数による `alembic.ini` の上書きが実装済みのため、CI環境での接続先切り替えはそのまま動作

**修正ファイル：**

- `.github/workflows/ci.yml`（新規）
- `frontend/playwright.config.ts`（新規）
- `frontend/tsconfig.json`（新規）
- `frontend/tsconfig.node.json`
- `frontend/package.json`
- `frontend/e2e/helpers/auth.ts`（新規）
- `frontend/e2e/auth.spec.ts`（新規）
- `frontend/e2e/project.spec.ts`（新規）
- `frontend/e2e/budget.spec.ts`（新規）

## [chore/openapi-typescript-codegen] - 2026-06-18

### Added

#### openapi-typescript-codegenの導入

- `openapi-typescript-codegen` を導入し、バックエンドのOpenAPI仕様（`openapi.json`）から型定義・APIクライアントを自動生成
- `src/api/models/` 配下に以下の型定義ファイルを自動生成
  - `ProjectResponse` / `ProjectCreate` / `ProjectUpdate` / `ProjectStatus` / `ProjectListResponse`
  - `ApprovalRequest` / `BudgetSummaryResponse`
  - `TaskResponse` / `TaskCreate` / `TaskUpdate` / `TaskStatus`
  - `UserResponse` / `UserCreate` / `UserRole`
  - `NotificationResponse` / `NotificationListResponse`
  - `ProjectBudgetResponse` / `ProjectBudgetCreate` / `ProjectBudgetUpdate`
  - `WorklogResponse` / `WorklogCreate` / `WorklogUpdate`
  - `ExpenseResponse` / `ExpenseCreate` / `ExpenseUpdate` / `ExpenseType`
  - `DepartmentResponse` / `DevelopmentMethod` / `LoginRequest` / `RefreshRequest` / `TokenResponse`
  - `HTTPValidationError` / `ValidationError`
- `src/api/core/` 配下にAPIクライアント基盤ファイルを自動生成
  - `ApiError` / `ApiRequestOptions` / `ApiResult` / `CancelablePromise` / `OpenAPI` / `request`
- `src/api/services/` 配下に `DefaultService` / `Service` を自動生成

#### UIロジック用定数ファイルの整備

- `src/constants/chartColors.ts` を新規作成
  - 部門別グラフ（ECharts）用カラーパレット定数（`DEPARTMENT_CHART_COLORS`）を定義
- `src/constants/gantt.ts` を新規作成
  - ガントチャート左固定列幅定数（`PHASE_WIDTH` / `PERSON_WIDTH` / `TASK_WIDTH`）を定義
- `src/constants/taskStatus.ts` を新規作成
  - タスクステータスのラベル変換（`getTaskStatusLabel`）・タグ種別変換（`getTaskStatusTagType`）・CSSクラス変換（`getTaskStatusClass`）を実装
  - `TODO` / `NOT_STARTED` など表記ゆれに対応した統一処理を追加

### Changed

#### 既存型定義ファイルの自動生成ファイルへの移行

- `src/types/project.ts` を削除し、`src/api/models/` 配下の自動生成ファイルへ移行
  - 定数（`PROJECT_STATUS_LABEL` / `PROJECT_STATUS_TAG_TYPE`）は `src/constants/project.ts` へ移管
- `src/types/task.ts` を削除し、`src/api/models/` 配下の自動生成ファイルへ移行
- `src/types/user.ts` を削除し、`src/api/models/` 配下の自動生成ファイルへ移行
- `src/types/budget.ts` を削除し、`src/api/models/` 配下の自動生成ファイルへ移行
- `src/types/notification.ts` はUIロジック用の型（`NotificationLike` / `NotificationKind` / `NotificationTagType` / `NotificationToastType` / `NotificationMeta`）のみ残存

#### importパス・型名の更新

- `src/api/projects.ts` : `Project` → `ProjectResponse`、importパスを自動生成ファイルへ更新
- `src/api/tasks.ts` : `Task` → `TaskResponse`、importパスを自動生成ファイルへ更新
- `src/api/notifications.ts` : `Notification` → `NotificationResponse`、importパスを自動生成ファイルへ更新
- `src/api/budget.ts` : `BudgetSummaryResponse` → `ProjectBudgetResponse`、importパスを自動生成ファイルへ更新
- `src/constants/budget.ts` : importパスを `@/api/models/ExpenseType` へ更新
- `src/stores/auth.ts` : `Role` → `UserRole`、importパスを `@/api/models/UserRole` へ更新
- `src/components/projects/ApplicantProjectTable.vue` : 型参照・importパスを更新、`PROJECT_STATUS_TYPE` を `PROJECT_STATUS_TAG_TYPE` へ修正
- `src/components/projects/HqManagerProjectTable.vue` : 同上
- `src/components/projects/DeptManagerProjectTable.vue` : 同上
- `src/components/budget/BudgetProjectTable.vue` : 型参照・importパスを更新
- `src/components/projects/detail/ProjectBudgetSummaryCard.vue` : `ProjectBudget` → `ProjectBudgetResponse`、importパスを更新
- `src/components/dashboard/applicant/ApplicantProjectTable.vue` : 型参照・importパスを更新
- `src/composables/useBudgetList.ts` : `Project` → `ProjectResponse`、importパスを更新
- `src/views/projects/ProjectDetailView.vue` : `BudgetSummaryResponse` → `ProjectBudgetResponse` へ変更
- `src/views/budget/BudgetView.vue` : `BudgetSummaryResponse` → `ProjectBudgetResponse` へ変更、予算サマリー計算ロジックを `ProjectBudgetResponse` のフィールドに合わせて修正

### Fixed

#### 命名バグ修正

- `PROJECT_STATUS_TYPE` を `PROJECT_STATUS_TAG_TYPE` に統一（`useProjectTable.ts` から返される名前と不一致だったバグを修正）

#### ビルド設定修正

- `vite.config.ts` に `build.target: "esnext"` を追加（トップレベル `await` によるビルドエラーを解消）
- `tsconfig.app.json` の `erasableSyntaxOnly` を削除（enumを使用するため）
- `vue-tsc` を `2.2.0` に更新（TypeScript 6対応）
- `openapi-typescript` を削除（`openapi-typescript-codegen` と TypeScript バージョンの競合を解消）

### Removed

- `src/views/budget/BudgetListView copy.vue` を削除（不要ファイル）

**修正ファイル：**

- `frontend/vite.config.ts`
- `frontend/tsconfig.app.json`
- `frontend/package.json`
- `frontend/src/api/projects.ts`
- `frontend/src/api/tasks.ts`
- `frontend/src/api/notifications.ts`
- `frontend/src/api/budget.ts`
- `frontend/src/constants/budget.ts`
- `frontend/src/constants/project.ts`
- `frontend/src/stores/auth.ts`
- `frontend/src/composables/useBudgetList.ts`
- `frontend/src/components/projects/ApplicantProjectTable.vue`
- `frontend/src/components/projects/HqManagerProjectTable.vue`
- `frontend/src/components/projects/DeptManagerProjectTable.vue`
- `frontend/src/components/budget/BudgetProjectTable.vue`
- `frontend/src/components/projects/detail/ProjectBudgetSummaryCard.vue`
- `frontend/src/components/dashboard/applicant/ApplicantProjectTable.vue`
- `frontend/src/views/projects/ProjectDetailView.vue`
- `frontend/src/views/budget/BudgetView.vue`

## [fix/task-update-permission] - 2026-06-16

### Fixed

#### TASK_MEMBERがタスク更新を行うと403エラーになる不具合を修正

**原因①：フロントエンドの権限制御に TASK_MEMBER が考慮されていなかった**

- `TaskDetailDialog.vue` の入力フィールドと保存ボタンが `isApplicant` のみを条件としており、`TASK_MEMBER` でダイアログを開いても編集・保存ができない状態だった
- `auth.ts` に `isTaskMember` ゲッターを追加し、`TaskDetailDialog.vue` の制御条件に `TASK_MEMBER` を追加

**原因②：バックエンドのステータス制限の値が誤っていた**

- `task_service.py` の `TASK_MEMBER` ステータス制限で `"REVIEW"` と記載されていたが、正しい Enum 値は `TaskStatus.IN_REVIEW` であった
- 文字列リテラルを `TaskStatus.IN_REVIEW` / `TaskStatus.DONE`（Enum値）に修正

**原因③：現在値と同じ値で保存しても制限に引っかかる問題**

- 既に `DONE` / 進捗率100% のタスクを `TASK_MEMBER` が開いて保存しようとすると、値を変更していなくても制限に引っかかり 403 が返っていた
- ステータス・進捗率の制限を「現在値から変更しようとした場合のみ制限する」に緩和

### Added

#### DEPT_MANAGER / HQ_MANAGER のタスク更新に認可制限を追加

- `DEPT_MANAGER` / `HQ_MANAGER` はフロントエンドでタスク更新UIを非表示にしていたが、バックエンド側には認可制限がなかった
- `tasks.py`（ルーター）に `require_roles([UserRole.APPLICANT, UserRole.TASK_MEMBER])` を追加し、ルーター層で早期に弾くよう対応
- `task_service.py`（サービス層）にも `DEPT_MANAGER` / `HQ_MANAGER` の場合に 403 を返す処理を追加（多層防御）

**修正ファイル：**

- `frontend/src/stores/auth.ts`
- `frontend/src/components/projects/TaskDetailDialog.vue`
- `backend/app/routers/tasks.py`
- `backend/app/services/task_service.py`

## [fix/project-list-navigation] - 2026-06-15

### Fixed

#### 案件一覧から案件詳細へ遷移できない不具合を修正

- `ProjectListPanel.vue` の `openProject` 内に `embedded` フラグによる遷移ブロック処理が存在していた
- `ApplicantDashboard.vue` / `TaskMemberDashboard.vue` でダッシュボード埋め込み表示時に `embedded: true` が渡されるため、案件名クリック時に `/projects/:id` への遷移がブロックされていた
- `embedded` prop は `ProjectListPanel` をダッシュボード内に埋め込むための prop であり、遷移ブロックの用途で使用することは設計意図と合致しないと判断
- 案件詳細画面には「ダッシュボードへ戻る」ボタンは存在せず、「戻る」ボタンで案件一覧へ、メニューからダッシュボードへ戻れる導線が確保されているため、遷移ブロックを削除しても UX 上の断絶は発生しないと確認
- `openProject` 内の `if (props.embedded) { return; }` を削除し、埋め込み表示時でも案件詳細へ遷移できるよう修正

**修正ファイル：**

- `frontend/src/components/projects/ProjectListPanel.vue`

## [docs/submission-finalization] - 2026-05-13

### Fixed

#### 案件一覧の部門表示不整合修正

- seed品質監査中に、案件一覧の「部門」列が空欄になる不具合を確認
- `/api/projects` のレスポンスに `department_id` のみ含まれ、`department_name` が返却されていないことを確認
- `ProjectResponse` に `department_name` / `applicant_name` を追加
- `response_service.py` の `to_response()` を修正し、関連リレーションから部門名・申請者名をレスポンスへ設定するよう改善
- Local環境で案件一覧の部門表示が正常に復旧することを確認

---

### Changed

#### 提出物最終調整

- プレゼン資料を `presentation_final_v13` まで更新し、seed品質監査・利用者フィードバック・UI改善内容を最終反映
- インターン感想（20P・21P）を見直し、技術面・設計面・品質監査・利用者視点・今後に向けた学びの内容を整理
- PDF提出に向け、PowerPoint資料のエクスポート手順および提出形式を最終確認

#### 利用マニュアル更新

- `doc/user_manual.md` を最新実装に合わせて更新
- 案件申請Drawer、通知Popover / Drawer / Dialog、ダッシュボード内一覧切替など、画面遷移を抑えたUI設計を反映
- WebSocket通知、未読件数同期、Dialogによる既読化など最新仕様を追記
- PoCスコープおよび実運用を見据えたUI改善方針を補足

#### ER設計更新

- `doc/db/er_design.md` を最新DBモデルに合わせて更新
- `TaskStatus.REVIEW` を `IN_REVIEW` へ修正
- `notifications.updated_at` を削除し、実装との整合性を改善
- `departments → projects` の関連を追加
- `tasks` / `expenses` の日付型を `date` に統一

#### 画面設計書更新

- `doc/design/screens/dashboard.md` を最新ダッシュボード仕様に更新
- KPIカードによる一覧切替、activeMenu同期、Drawerによる案件申請導線を反映
- `doc/design/screens/notification.md` を最新通知UI仕様に更新
- PC：Popover、スマホ：Drawer、詳細Dialog、WebSocket通知を反映
- `doc/design/screens/project_apply.md` をDrawer表示、URL query同期、再読み込み復元仕様へ更新

---

### Verified

#### seed品質監査

- HQ_MANAGER で案件一覧の部門列表示を確認
- 部門別ダッシュボード集計と案件一覧表示の整合性を確認
- seedデータ不備ではなく、APIレスポンス項目不足が原因であったことを確認

#### 提出物整合確認

- プレゼン資料、利用マニュアル、ER設計、Information.md の内容整合を確認
- 課題資料（18〜20P）の提出要件との整合を確認
- プレゼン資料の企業背景、PoCスコープ、UI改善内容、将来拡張提案の反映状況を確認

## [docs/submission-finalization] - 2026-05-12

### Changed

#### 申請者・担当者ダッシュボード導線統一

- `TASK_MEMBER` / `APPLICANT` のサイドバー「案件一覧」を `/?view=projects` に統一し、専用一覧ページへの画面遷移を廃止
- `AppSidebar.vue` の `activeMenu` を queryベース判定へ更新し、`/?view=projects` 選択時もメニュー状態が正しく同期されるよう修正
- `handleMenuSelect()` を query同期型へ整理し、ロール別ダッシュボード内で案件一覧へ切替できる構成へ統一
- `DashboardView.vue` の `route.query.view` watch を整理し、`TASK_MEMBER` / `APPLICANT` / 管理者で共通導線を維持しつつ、ロール別に表示パネルを切替できるよう改善

---

#### 申請者ダッシュボードUI改善

- `ApplicantDashboard.vue` を「KPIカード常時表示 + 下部パネル切替」構成へ変更
- `summary` 表示時は「申請中案件一覧」、`projects` 表示時は `ProjectListPanel embedded` を表示する構成へ整理
- `ApplicantSummaryCards.vue` をダッシュボード常時表示へ変更し、案件一覧表示時も KPI状況を継続確認できるよう改善
- `summary` props を `DashboardView.vue` 側で存在チェック後に渡す構成へ整理し、初期描画時の `null` 型エラーを解消
- `ApplicantSummaryCards.vue` のレスポンシブ表示を見直し、ブラウザ幅縮小時は折返しではなく横スクロール表示へ統一

---

#### 担当者ダッシュボードUI整理

- `TaskMemberDashboard.vue` と `ApplicantDashboard.vue` の責務構成を統一
- 両ロールとも「KPIカード常時表示 + 下部パネル切替」という共通UXへ整理
- `ProjectListPanel.vue` の `embedded` 再利用構成を強化し、ダッシュボード内一覧表示を共通化

---

#### 案件申請Drawer導入（画面遷移削減UI）

- `APPLICANT` のサイドバー「案件申請」を `/projects/new` から `/?action=create-project` へ変更し、画面遷移なしで申請できる導線へ変更
- `AppSidebar.vue` に `action=create-project` 判定を追加し、案件申請Drawer起動用の query同期処理を追加
- `DashboardView.vue` に `route.query.action` 監視を追加し、申請者のみ `ProjectCreateDrawer.vue` を表示できる構成へ整理
- Drawer閉鎖時は `router.replace()` で `action` query を自動削除し、URL状態とUI状態の同期を維持
- `ProjectCreateDrawer.vue` を新規追加し、`v-model` ベースで開閉制御できる共通Drawerコンポーネントを実装
- `ProjectCreateForm.vue` を新規追加し、案件申請フォームをページ表示・Drawer表示の両方で再利用できる構成へ整理
- `ProjectCreateForm.vue` の部門選択UIを削除し、ログインユーザー所属部門をバックエンド側で自動設定する現行設計へ統一

---

#### フロントエンド責務分離整理

- `DashboardView.vue`
  - 状態管理・query同期・Drawer制御を担当

- `ApplicantDashboard.vue`
  - KPI表示・一覧切替表示を担当

- `ProjectCreateDrawer.vue`
  - Drawer表示責務を担当

- `ProjectCreateForm.vue`
  - 入力フォーム・バリデーション・API送信責務を担当

- `ProjectListPanel.vue`
  - embedded一覧表示責務を担当

- ダッシュボード・一覧・申請フォームの責務を明確化し、今後の「案件編集Drawer」「案件複製」「下書き保存」などの機能追加に対応しやすい構成へ整理

---

#### ダッシュボード型定義整理・型安全性向上

- `budgetWarningCount` 追加に伴う `DashboardSummary` / `SummaryData` 間の型不整合を解消
- `SummaryData` を `DashboardSummary` 継承型へ変更し、ダッシュボード集計項目の追加漏れを防止する構成へ整理
- `SummaryData` に `overdueTasks` / `lowSpiProjects` / `lowCpiProjects` / `overdueTaskCount` を拡張項目として統合
- `DashboardViewMode` を `useDashboard.ts` のローカル型から `types/dashboard.ts` へ移動し、ダッシュボード関連型を集約
- `useDashboard.ts` のローカル型定義を削減し、Composableは状態管理責務に集中できる構成へ整理
- `DashboardSummaryCards.vue` / `ApplicantDashboard.vue` / `ApplicantSummaryCards.vue` の props 型を共通 `DashboardSummary` 参照へ統一
- `api/dashboard.ts` と `types/dashboard.ts` の型整合性を見直し、ダッシュボード関連の型安全性を向上
- `npm run build` にて `vue-tsc` / `vite build` の正常完了を確認

## [fix/security-and-requirements] - 2026-05-11

### Changed

#### 通知機能UI整理

- PCではサイドバー、スマホではヘッダーから通知を確認できるように整理
- 通知一覧ページへの画面遷移を廃止し、PCはPopover、スマホはDrawerで通知一覧を確認できるUIへ変更
- 通知詳細は中央固定Dialogで表示し、一覧表示を維持したまま詳細確認できるUIへ改善
- 長文の承認・却下コメントは一覧上では省略表示し、詳細Dialogで全文確認できるよう改善
- `useNotifications.ts` を追加し、通知取得・既読処理・未読件数同期処理を共通化
- WebSocket通知の初期化処理を `App.vue` に集約し、PC / スマホ共通でリアルタイム更新される構成へ整理
- 通知種別（承認依頼・却下・着手・完了・レビュー）に応じた色分け表示を追加し、通知一覧から優先度を直感的に判断できるUIへ改善
- WebSocketトースト通知も通知種別に応じた色で表示するよう統一
- 通知UIを `NotificationList.vue` / `NotificationItem.vue` / `NotificationDetailDialog.vue` に分離し、PC / スマホで共通利用できる構成へ整理

---

#### ダッシュボード案件一覧UI改善

- サイドバー「案件一覧」とダッシュボード内「案件一覧」の表示導線を統一
- `DashboardView.vue` に案件一覧モード（`projects`）を追加し、一覧表示時は管理グラフを非表示化
- サマリーカード・本部管理者向け部門切替は案件一覧モードでも継続利用できる構成へ整理
- `DashboardContentPanel.vue` に案件一覧専用ページネーションUIを追加
- `useDashboard.ts` / `dashboard.ts` を更新し、案件一覧取得を server-side pagination に対応
- 検索条件変更時はページ番号を自動リセットするよう改善
- スマホDrawerメニューも `/?view=projects` に統一し、PC / スマホで導線を統一

---

#### タスク詳細Dialog導入（画面遷移削減UI）

- `TaskDetailDialog.vue` を新規追加し、タスク詳細をモーダル表示できるUI基盤を実装
- `ProjectDetailView.vue` に選択タスク・Dialog表示制御を追加
- `TaskGanttTable.vue` に `open-task-detail` イベントを追加し、左固定ペイン・ガントバークリックからタスク詳細を表示できるよう改善
- タスク一覧は「俯瞰表示」、TaskDetailDialog は「深掘り確認」と役割を分離
- 一覧に表示していない説明・期限・遅延判定・更新履歴などを、今後Dialogへ集約できる構成へ整理

---

#### ガントチャートUI改善

- 左固定ペインと右タイムラインの表示ラインずれを修正
- 行高さを共通変数（`--gantt-row-height`）で管理する構成へ統一
- `min-height` ベースから `height + box-sizing` ベースへ変更し、固定項目とガントバーの表示ラインを統一
- ガントバーの垂直位置を微調整し、視認性を改善

---

#### サイドバーUI復旧・スタイル整理

- `AppSidebar.vue` のスタイルを復元し、レイアウト崩れを修正
- サイドバー幅・ユーザー情報レイアウトを再調整
- 通知一覧の省略表示に `line-clamp` を追加
- PC / スマホのレイアウト責務を整理
- `position: fixed` を復元し、画面スクロール時もサイドバーを固定表示する構成へ修正
- `App.vue` の `app-content` にサイドバー幅を考慮したレスポンシブレイアウトを追加し、ブラウザ幅変更時もメイン画面が自動調整されるよう改善

---

#### ProjectDetailView責務分離・詳細画面UI復元

- `ProjectDetailView.vue` をページ制御専用へ整理し、表示責務を子コンポーネントへ分離
- `ProjectInfoCard.vue` / `ProjectTaskCard.vue` / `ProjectBudgetSummaryCard.vue` を新規追加し、案件詳細画面の責務を明確化
- `Project` / `Task` / `ProjectBudget` のローカル型定義を廃止し、`types/` 配下の共通型へ統一
- `PROJECT_STATUS_LABEL` / `PROJECT_STATUS_TAG_TYPE` / `TASK_STATUS_LABEL` など既存定数を再利用する構成へ統一
- `TaskDetailDialog.vue` を `visible` prop設計から Vue3標準 `v-model (modelValue)` 対応へ移行し、親子間状態同期を統一
- `TaskGanttTable.vue` の `open-task-detail` イベントと `ProjectTaskCard.vue` を接続し、ガントチャートからタスク詳細Dialogを表示できるよう修正
- `router.params.id` 参照を `router.params.projectId` に修正し、本部管理者で案件詳細が「案件IDが不正です」と表示される不具合を修正
- `authStore.user?.role` 参照を `authStore.role` に統一し、権限制御ロジックを現行Store設計へ整合
- `budgetsAPI` の誤参照を `budgetAPI` に修正し、予算サマリ取得処理を正常化
- `TaskGanttTable.vue` / `ProjectTaskCard.vue` のイベント名を統一し、ガントチャート上のタスク選択時に詳細Dialogが正常表示されるよう修正

---

#### 案件詳細UIレイアウト復元

- `ProjectInfoCard.vue` を分離前の「案件情報」レイアウトへ復元し、ステータス・概算予算・概算工数・進捗率・目的概要を従来構成で表示するよう修正
- `ProjectTaskCard.vue` のテーブル一覧を整理し、分離前と同様にガントチャート主体の俯瞰表示へ統一
- `TaskGanttTable.vue` を `ProjectTaskCard.vue` 内へ移設し、タスク一覧カード内にガントチャートを内包する従来UIへ復元
- `ProjectBudgetSummaryCard.vue` を KPIカード型から表形式レイアウトへ変更し、分離前と同じ「予算サマリ」表示へ復元
- 分離後に変化していた表示順を「案件情報 → タスク一覧 → 予算サマリ」に再統一し、プレゼン資料・既存UIとの整合性を確保

---

#### 予算管理画面責務分離・一覧UIコンポーネント化

- `BudgetListView.vue` をページ制御専用へ整理し、検索条件・一覧表示・サマリー表示の責務を子コンポーネントへ分離
- `BudgetListHeader.vue` を新規追加し、案件名検索・ステータス・部門・予算帯フィルターをヘッダーUIとして分離
- `BudgetSummaryCards.vue` を新規追加し、案件数・総予算・総実績・平均消化率のサマリーカード表示責務を分離
- `BudgetProjectTable.vue` を新規追加し、案件別予算一覧・ソート・ページネーション・詳細遷移UIを分離
- `useBudgetList.ts` を新規追加し、予算一覧取得・サマリー取得・部門取得・検索条件・ソート・ページング・画面遷移処理を composable 化
- `BudgetListView.vue` 内に混在していた API呼び出し・状態管理・UIロジックを整理し、ページコンポーネントはレイアウト制御に専念する構成へ改善
- `BudgetProjectTable.vue` の `defineProps` を `props` 参照へ統一し、TypeScript の暗黙 `any` 警告に対応
- サマリーカード・一覧テーブル・検索ヘッダーの責務を明確化し、他画面でも再利用しやすい構成へ整理
- API取得処理を `useBudgetList.ts` に集約し、View層からデータ取得責務を分離
- 今後の「予算詳細Dialog」「費目別集計」「月次予算グラフ」などの機能追加に対応しやすい拡張性の高い構成へ整理

---

#### タスク登録画面責務分離・フォームUIコンポーネント化

- `TaskFormView.vue` をページ制御専用へ整理し、フォーム表示・操作ボタン・API処理の責務を分離
- `TaskFormCard.vue` を新規追加し、タスク入力フォームUIを分離
- `TaskFormActions.vue` を新規追加し、戻る・登録/更新・削除ボタンの操作UIを分離
- `useTaskForm.ts` を新規追加し、案件取得・担当者取得・タスク取得・登録・更新・削除処理を composable 化
- `TaskFormView.vue` 内に混在していた API呼び出し・権限制御・フォーム状態管理・watcher処理を `useTaskForm.ts` へ集約
- `TASK_MEMBER` と `APPLICANT` の編集権限制御を composable 側へ集約し、UIと業務ロジックの責務を分離
- `TaskFormCard.vue` の `el-form` ref を `v-model (formRef)` で親子接続し、バリデーション処理を従来通り利用できる構成へ整理
- タスク登録画面を UI部品・状態管理・業務ロジックに分離し、今後の「工数入力」「レビューコメント」「添付ファイル」などの機能追加に対応しやすい構成へ整理

---

#### ライブラリ警告対応

- `Element Plus` の `el-radio-button` 非推奨警告に対応し、`label` 属性を `value` 属性へ更新
- 将来の `Element Plus v3` 移行を見据えた互換性対応を実施

## [fix/security-and-requirements] - 2026-05-08

### Fixed

#### ダッシュボード導線修正

- APPLICANT / TASK_MEMBER のダッシュボードカードクリック時に画面遷移・表示切替が正しく動作しない問題を修正
- TASK_MEMBER の担当タスク行クリック時に、対象タスクの案件詳細へ遷移するよう修正
- ダッシュボード内の `project_id` / `id` の扱いを見直し、案件詳細遷移先を `/projects/:projectId` に統一

---

### Changed

#### 申請者ダッシュボード改善

- 申請者ダッシュボードのサマリーカードを以下の構成へ整理
  - 申請中
  - 却下
  - 注意・危険
  - 予算消費率
  - 下書き
- カードクリック時に画面遷移せず、下部の案件一覧をカード種別に応じて切り替える方式へ変更
- 下部一覧を初期表示では「自分の進行中案件」として表示するよう変更
- 「進行中案件に戻る」ボタンを追加し、絞り込み後に初期表示へ戻れるよう改善
- 注意・危険 / 予算確認案件の表示対象を、進行中・承認済み案件中心に整理

---

#### 担当者ダッシュボード改善

- 担当者ダッシュボードのサマリーカードクリック時に、画面遷移せず下部の担当タスク一覧を切り替える方式へ変更
- 担当タスク数 / 今日期限 / 期限超過 / 進行中 / レビュー中 の各カードに応じて、一覧表示を絞り込むよう改善
- 担当者ダッシュボードの初期表示を「自分の担当タスク」とし、カード選択によるフィルター切替に統一
- 担当タスク一覧の件数とサマリーカード件数が一致するよう、未完了タスク基準へ集計を調整

---

### Refactored

#### ダッシュボードコンポーネント整理

- `ApplicantSummaryCards.vue` でカード選択イベントを emit し、親コンポーネント側で表示フィルターを管理する構成へ変更
- `ApplicantProjectTable.vue` で表示対象案件を filter prop に応じて computed で切り替える構成へ変更
- `TaskMemberDashboard.vue` でカード選択状態を内部 state として管理し、表示対象タスクを computed で切り替える構成へ変更
- `useDashboardActions.ts` の不要・重複した遷移処理を整理

### Changed

#### HQ_MANAGERダッシュボードUI整理

- 注視部門ランキングをダッシュボードから削除
- 現在のPoCでは部門数が2部門のため、ランキングによる情報価値が限定的と判断
- 部門比較は案件数・予算・期限超過グラフへ集約し、画面の情報重複を解消
- 将来的な多部門運用を想定し、注視部門ランキングは future_proposals.md へ移管

### Changed

#### 管理者ダッシュボードUI整理

- HQ_MANAGER / DEPT_MANAGER 向けダッシュボードの表示構成を整理
- 注視部門ランキングを削除し、部門数が少ないPoCではグラフ中心の比較に集約
- 部門別グラフは初期表示時のみ表示する構成へ変更
- サマリーカード選択時は画面遷移せず、ダッシュボード内の案件一覧を切り替える方式へ変更
- 管理者向けサマリーカードを以下の構成へ整理
  - 承認待ち
  - 進行中案件
  - 危険案件
  - 注意案件
  - 予算消費率
- 予算消費率カード選択時の一覧名を「予算注意案件」へ整理
- 危険 / 注意 / 予算注意案件は、承認済み・進行中案件を中心に表示するよう整理
- カード選択後に「ダッシュボード表示に戻る」ボタンを表示し、初期表示へ戻れるよう改善

---

### Refactored

#### ダッシュボード責務分離

- 管理者ダッシュボードのフィルター制御を `useManagementDashboard.ts` へ分離
- 管理者ダッシュボード用フィルター型を `types/dashboard.ts` に共通化
- 部門別グラフ表示を `ManagementCharts.vue` としてコンポーネント化
- `DashboardView.vue` から管理者向けフィルター処理・グラフ表示処理を分離し、画面全体の責務を整理
- `DashboardSummaryCards.vue` は画面遷移ではなく、親コンポーネントへフィルター選択イベントを emit する構成へ変更
- `DashboardProjectList.vue` は選択フィルターに応じて一覧タイトル・説明文を切り替える構成へ変更

### Fixed

#### 案件一覧導線修正

- `frontend/src/views/ProjectListView.vue`
  - 各案件テーブル（申請者・部門管理者・本部管理者）の `move` イベント受け取り処理を追加
  - 案件名クリック時に `/projects/:id` へ遷移する `goToProjectDetail()` を追加

#### 動作改善

- 案件一覧から案件詳細へ遷移できない不具合を修正
- ロール別一覧画面で案件詳細導線を復旧

---

### Changed

#### ガントチャートUI改善

- `TaskGanttTable.vue` を案件詳細画面のガント表示コンポーネントとして整理し、ガント表示を一本化
- 横スクロール時でも対象タスクを見失わないよう、以下の固定ペインUIを追加
  - 工程
  - タスク名
  - 担当者
  - 状態
  - 進捗率
- 進捗表示をバー形式から数値表示（%）へ整理し、ガントバーとの情報重複を解消
- ガント表示に担当者フィルターを追加し、担当者単位での工程確認を可能に改善
- ガント表示に以下の表示切替を追加
  - 日表示
  - 週表示
  - 月表示
- ガント上に「本日ライン」を追加し、現在位置とタスク期間の差分を視覚的に把握できるよう改善
- 初期表示時に本日ライン位置へ自動スクロールするよう改善
- 「📍 今日へ移動」ボタンを追加し、スクロール後も本日ライン位置へ戻れるよう改善

---

### Refactored

#### ガントチャート責務整理

- ガント計算処理を `useTaskGantt.ts` へ分離
- `TaskGanttTable.vue` は表示責務に集中する構成へ整理
- 固定列とタイムライン列を DOM 構造として分離し、`position: sticky` に依存しない固定表示へ改善

---

#### 未使用コンポーネント整理

- `TaskGuideAlert.vue` を削除
  - ガント高度UI・タスク一覧UIの整理により役割が重複していたため削除
- `GanttChart.vue` を未使用コンポーネント候補として整理
  - `TaskGanttTable.vue` へ機能集約を進行

## [fix/security-and-requirements] - 2026-05-07

### Added

#### ダッシュボード（ロール別UI再設計）

- ダッシュボードをロール別表示へ再設計
  - `TASK_MEMBER`：担当者ダッシュボード
  - `APPLICANT`：申請者ダッシュボード
  - `DEPT_MANAGER` / `HQ_MANAGER`：管理者ダッシュボード

- `DashboardView.vue` をロール分岐構成へ変更
- ページタイトル・説明文をロールごとに動的表示するよう改善

---

#### 担当者ダッシュボード追加

- `TaskMemberDashboard.vue` を追加
- サマリーカードと担当タスク一覧を分離実装
  - `TaskMemberSummaryCards.vue`
  - `TaskMemberTaskTable.vue`

- 表示内容を担当者向けに最適化
  - 自分の担当タスク件数
  - 今日期限タスク
  - 期限超過タスク
  - 進行中タスク
  - レビュー待ちタスク

---

#### 申請者ダッシュボード追加

- `ApplicantDashboard.vue` を追加
- サマリーカードと申請案件一覧を分離実装
  - `ApplicantSummaryCards.vue`
  - `ApplicantProjectTable.vue`

- 表示内容を申請者向けに最適化
  - 自分の申請案件数
  - 承認待ち案件数
  - 進行中案件数
  - 注意・危険案件数
  - 予算消費率

---

#### 管理者ダッシュボード改善

- 部門別案件数可視化を追加
  - `DepartmentProjectChart.vue` を追加
  - ドーナツグラフ形式で部門別案件数を表示
  - 合計案件数・部門別件数・構成比を表示

- `useDashboard.ts` に部門別案件データ管理を追加
  - `departments` state追加
  - APIレスポンスとの同期処理追加

- `dashboard.ts` に部門別案件集計型を追加
  - `DepartmentSummary`
  - `DashboardResponse.departments`

---

### Changed

#### ダッシュボード内部構成整理

- ダッシュボードコンポーネントをロール別責務で分離
- 管理者画面の構成を以下へ整理
  - KPIサマリー
  - 部門別案件数グラフ
  - 注視案件一覧

- ステータス表示を `PROJECT_STATUS_TAG_TYPE` に統一
- 重複していたステータス表示ロジックを共通定義へ集約

---

### Fixed

#### TypeScript / Vueエラー修正

- `v-if / v-else-if / v-else` 構造の重複によるVueテンプレートエラーを修正
- `TaskMemberDashboard` の `summary` props不足による型エラーを修正
- `ApplicantProjectTable` のステータス定義重複を解消
- `PROJECT_STATUS_LABEL / PROJECT_STATUS_TAG_TYPE` のimport不整合を修正

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- HQ_MANAGER で部門別案件数グラフ表示確認
- DEPT_MANAGER で部門別案件数グラフ表示確認
- APPLICANT で申請者ダッシュボード表示確認
- TASK_MEMBER で担当者ダッシュボード表示確認

---

#### 管理者ダッシュボード改善（予算可視化）

- 部門別予算消費率可視化を追加
  - `DepartmentBudgetChart.vue` を追加
  - 棒グラフ形式で部門別予算消費率を表示
  - 部門名・消費率（%）を可視化
  - データ未存在時の空状態表示を追加

- 管理者ダッシュボードへ部門別予算消費率グラフを追加
  - `DashboardView.vue` に組み込み
  - 部門別案件数グラフに続けて予算状況を確認できる構成へ改善

- `echarts` / `vue-echarts` を導入
  - 棒グラフ表示用ライブラリを追加
  - Docker開発環境へ依存パッケージを反映

---

#### グラフ描画設定追加

- `DepartmentBudgetChart.vue` に ECharts初期設定を追加
  - `CanvasRenderer`
  - `BarChart`
  - `GridComponent`
  - `TooltipComponent`

- `consumption_rate` を使用するよう型定義に合わせて修正
  - `budget_consumption_rate` → `consumption_rate`

---

### Fixed

#### TypeScript / Vue / EChartsエラー修正

- `DepartmentSummary` の存在しないプロパティ参照エラーを修正
  - `budget_consumption_rate` の参照を `consumption_rate` へ修正

- `vue-echarts` import解決エラーを修正
  - Dockerコンテナ内の依存パッケージ未反映を解消

- ECharts renderer未登録エラーを修正
  - `Renderer 'undefined' is not imported` を解消
  - `CanvasRenderer` の明示登録を追加

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- `HQ_MANAGER` で部門別予算消費率（棒グラフ）表示確認
- `DEPT_MANAGER` で部門別予算消費率（棒グラフ）表示確認
- Docker開発環境で `vue-echarts` 正常読み込み確認
- ECharts renderer登録後のグラフ描画確認

---

### Added

#### 管理者ダッシュボード改善（納期リスク可視化）

- 部門別期限超過タスク件数可視化を追加
  - `DepartmentOverdueChart.vue` を追加
  - 棒グラフ形式で部門別の期限超過タスク件数を表示
  - 部門名・期限超過件数（件）を可視化
  - データ未存在時の空状態表示を追加

- 管理者ダッシュボードへ納期リスクグラフを追加
  - `DashboardView.vue` に組み込み
  - 部門別案件数・予算消費率に続けて納期リスクを確認できる構成へ改善

- `dashboard.ts` に部門別期限超過タスク件数型を追加
  - `DepartmentSummary.overdue_task_count`

---

### Changed

#### ダッシュボード集計機能拡張

- `dashboard_service.py` を拡張
  - 部門別期限超過タスク件数集計処理を追加
  - `projects` と `tasks` をもとに部門単位で期限超過タスクを集計
  - `departments` レスポンスへ `overdue_task_count` を追加

- 管理者ダッシュボード構成を改善
  - KPIサマリー
  - 部門別案件数グラフ
  - 部門別予算消費率グラフ
  - 部門別期限超過タスク件数グラフ
  - 注視案件一覧

---

#### フロントエンドビルド最適化

- ECharts系コンポーネントを遅延読み込み化
  - `DepartmentProjectChart`
  - `DepartmentBudgetChart`
  - `DepartmentOverdueChart`

- `DashboardView.vue` の静的importを `defineAsyncComponent` に変更

- 初期ロードチャンクを軽量化
  - `DashboardView` 約510KB → 約18KBへ改善

- グラフ表示処理を個別チャンクへ分離し、管理者ダッシュボードの初期表示性能を改善

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- `HQ_MANAGER` で部門別期限超過タスク件数（棒グラフ）表示確認
- `DEPT_MANAGER` で部門別期限超過タスク件数（棒グラフ）表示確認
- 部門別案件数・予算消費率・納期リスクの3グラフ同時表示確認
- ECharts系コンポーネントの個別チャンク出力確認
- `DashboardView` のチャンクサイズ削減確認

---

### Added

#### 管理者ダッシュボード改善（注視理由可視化）

- 注視案件一覧へ「注視理由」表示を追加
  - `DashboardProjectList.vue` を更新
  - 危険度に加えて「なぜ危険・注意なのか」を一覧上で確認可能に改善

- `dashboard.ts` に注視理由型を追加
  - `ProjectDashboard.alert_reason`

---

### Changed

#### アラート判定ロジック改善

- `dashboard_calc_service.py` を改善
  - `judge_alert_level` を `judge_alert` へ拡張
  - 危険度に加えて注視理由を返却する構成へ変更

- 注視理由判定を追加
  - `未着手`
  - `納期遅延`
  - `予算超過`
  - `期限超過`

- 複数条件に該当する場合は複合表示へ対応
  - 例：`未着手 + 納期遅延`
  - 例：`納期遅延 + 予算超過`

- `dashboard_builders.py` を更新
  - `build_project_item()` に `alert_reason` を追加
  - `alert_level` と `alert_reason` を分離管理する構成へ改善

---

#### 管理者ダッシュボードUX改善

- 注視案件一覧の表示順を改善
  - `危険度` の次に `注視理由` を表示
  - 危険度と発生理由を横並びで確認できるよう改善

---

### Fixed

#### アラートデータ構造修正

- `judge_alert()` の戻り値変更に伴うデータ構造不整合を修正
  - `alert_level` に dict が格納される問題を修正
  - `alert["level"]` / `alert["reason"]` を個別に格納するよう修正

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- `HQ_MANAGER` で注視理由表示確認
- `DEPT_MANAGER` で注視理由表示確認
- 危険・注意案件で注視理由の複合表示確認
- `DashboardView` の遅延読み込み最適化が維持されていることを確認

### Added

#### 管理者ダッシュボード改善（注視部門ランキング）

- `DepartmentRankingCard.vue` を追加
- 部門別データをもとに注視部門ランキングを表示
- 危険案件数・注意案件数・期限超過タスク数・予算消費率をカード形式で可視化
- 管理者が優先的に確認すべき部門を把握しやすい構成へ改善

---

### Changed

#### 管理者ダッシュボードUX改善

- 管理者ダッシュボードに注視部門ランキングを追加
- KPIサマリー直下にランキングを配置し、部門別グラフ確認前に重点部門を把握できる構成へ改善
- `DepartmentRankingCard` を遅延読み込み対象に追加し、初期チャンク肥大化を抑制

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- `DepartmentRankingCard` の個別チャンク出力確認
- `DashboardView` の軽量化維持確認

---

### Added

#### 管理者ダッシュボード改善（EVM指標可視化）

- 注視案件一覧へ `SPI` / `CPI` 表示を追加
  - `DashboardProjectList.vue` を更新
  - 案件ごとの進捗健全性・予算効率を数値で確認可能に改善

- `dashboard.ts` にEVM指標型を追加
  - `ProjectDashboard.spi`
  - `ProjectDashboard.cpi`

---

### Changed

#### ダッシュボード集計機能拡張

- `dashboard_calc_service.py` を拡張
  - `calc_spi()` を追加
    - `SPI = progress ÷ schedule_rate`
    - 予定進捗に対する実績進捗率を算出

  - `calc_cpi()` を追加
    - `CPI = progress ÷ consumption_rate`
    - 予算消費率に対する実績進捗率を算出

  - `schedule_rate <= 0` / `consumption_rate <= 0` の場合は `None` を返却し、0除算を防止

- `dashboard_builders.py` を更新
  - `build_project_item()` に `spi` / `cpi` を追加
  - 注視案件一覧・ダッシュボードAPIでEVM指標を利用可能に改善

---

#### 管理者ダッシュボードUX改善

- 注視案件一覧の表示順を改善
  - `進捗率` の次に `SPI` / `CPI` を表示
  - 進捗・納期・予算効率を横並びで比較できる構成へ改善

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- `HQ_MANAGER` で `SPI` / `CPI` 表示確認
- `DEPT_MANAGER` で `SPI` / `CPI` 表示確認
- `schedule_rate = 0` / `consumption_rate = 0` の場合に `-` 表示されることを確認
- `DashboardView` の遅延読み込み最適化が維持されていることを確認

### Added

#### ナビゲーションUI改善（PCサイドバー化）

- `AppSidebar.vue` を追加し、PC表示時のナビゲーションをヘッダーからサイドバーへ変更
- `App.vue` を更新し、画面幅に応じてナビゲーションを自動切替
  - PC：サイドバー表示
  - モバイル：従来ヘッダー表示
- サイドバー下部にユーザー情報・ログアウトメニューを配置
- 通知メニューをサイドバーへ統合
  - 未読件数を右寄せタグ形式で表示
  - `/notifications` の active 状態に対応

---

#### ナビゲーション設定共通化

- `frontend/src/constants/navigation.ts` を追加
- ロール別メニュー定義を共通化
  - `MenuItem`
  - `menuMap`
- `AppHeader.vue` / `AppSidebar.vue` の重複していた menu定義を削除
- icon import の重複を解消

---

#### HQ_MANAGER 部門別ドリルダウン機能追加

- `DashboardView.vue` に部門別表示切替機能を追加
- `HQ_MANAGER` のみ部門切替UIを表示
  - `全社`
  - 各部門単位表示

- `selectedDepartmentId` stateを追加
- 以下の computed を追加
  - `filteredDepartments`
  - `filteredRiskProjects`

- 部門選択に応じて以下を動的絞り込み表示
  - 注視部門ランキング
  - 部門別案件数
  - 部門別予算消費率
  - 部門別期限超過タスク件数
  - 注視案件一覧

---

### Changed

#### ダッシュボードレイアウト最適化

- 管理者ダッシュボードのグラフ表示を3カラム構成へ変更
  - `DepartmentProjectChart`
  - `DepartmentBudgetChart`
  - `DepartmentOverdueChart`

- `management-chart-grid` を追加し、縦長だったグラフ表示を横並びへ最適化
- サイドバー化に伴い、ダッシュボードの横幅利用効率を改善

---

#### 通知UI改善

- サイドバー通知を `el-badge` から `el-tag` 表示へ変更
- 未読件数をアイコン上表示からメニュー右側表示へ変更
- 通知メニューを `el-menu-item` 化し、他メニューとUIを統一

---

### Fixed

#### TypeScript / Vue修正

- `DashboardView.vue`
  - `ref` import不足による型エラーを修正
  - `computed` 内の state参照順を整理

- `AppSidebar.vue`
  - `/notifications` active制御を追加
  - 不要となった旧通知UI用CSSを削除
  - footerレイアウト崩れを修正

---

### Verified

#### 動作確認

- `npm run build` 成功確認
- PC表示でサイドバー正常表示確認
- モバイル表示でヘッダー切替確認
- `HQ_MANAGER` で部門切替表示確認
- 部門切替時のグラフ・注視案件一覧の動的更新確認
- 通知メニュー active状態・未読件数表示確認

### Added

#### KPIカード詳細導線

- `DashboardSummaryCards.vue`
  - KPIカードクリック時に関連画面へ遷移する導線を追加
  - hover時のカーソル・アニメーションを追加し操作性を向上

- KPIカード遷移先
  - 案件総数 → `/projects`
  - 進行中案件 → `/projects?status=APPROVED,IN_PROGRESS`
  - 危険案件 → `/projects?alertLevel=danger`
  - 注意案件 → `/projects?alertLevel=warning`
  - 予算消費率 → `/budget`

---

### Changed

#### 案件一覧のquery連携強化

- `frontend/src/views/projects/ProjectListView.vue`
  - `alertLevel` queryパラメータ対応を追加
  - URL queryから危険案件・注意案件フィルタを初期反映
  - `pageTitle` / `pageSubtitle` を queryに応じて動的変更
    - 危険案件一覧
    - 注意案件一覧
    - 進行中案件一覧
    - 承認待ち案件一覧
  - filter reset時にqueryパラメータを初期化するよう修正

- `frontend/src/api/projects.ts`
  - `getProjects()` に `alertLevel` パラメータを追加
  - `alert_level` をAPI queryとして送信するよう修正
  - `sortOrder` 引数を追加し型安全性を改善

---

#### Backend API拡張

- `backend/app/routers/project_router.py`
  - `get_projects()` に `alert_level` queryパラメータを追加

- `backend/app/services/project/project_service.py`
  - `get_projects()` に `alert_level` フィルタ処理を追加
  - `to_response()` 後の危険度判定結果で一覧フィルタ可能に改善

---

#### ProjectResponse拡張

- `backend/app/schemas/project.py`
  - `alert_level`
  - `alert_reason`

  を追加

---

#### アラート判定共通化

- `backend/app/services/response_service.py`
  - `_calc_schedule_rate()` を追加
  - `_judge_alert()` を追加
  - `to_response()` 内で進捗率・予算消費率から危険度を算出

- 判定ルール
  - schedule diff <= -20 → `danger`
  - schedule diff <= -10 → `warning`
  - budget diff <= -25 → `danger`
  - budget diff <= -15 → `warning`

---

#### 判定対象ステータス最適化

- アラート対象を以下のみに限定
  - `APPROVED`
  - `IN_PROGRESS`

- 以下はアラート対象外へ変更
  - `DRAFT`
  - `PENDING_DEPT`
  - `PENDING_HQ`
  - `COMPLETED`
  - `REJECTED`

- 却下案件が危険案件一覧に表示される問題を修正

---

#### UI調整

- `frontend/src/views/projects/ProjectListView.vue`
  - `.project-list { padding: 24px; }` を追加
  - サイドメニューとの余白を調整し、予算管理画面とUI統一

### Added

#### 部門別案件数グラフ ドリルダウン

- `frontend/src/components/dashboard/DepartmentProjectChart.vue`
  - 部門別案件数グラフの凡例クリック機能を追加
  - `defineEmits()` を追加し、選択部門IDを親コンポーネントへ通知する仕組みを実装
  - 凡例クリック時に `selectDepartment` event を emit するよう対応
  - hover時のカーソル変更・背景色変化を追加し操作性を向上

- クリック対象
  - 部門凡例（ドーナツグラフ右側の部門一覧）

- 動作
  - クリックした部門の `department_id` を親へ通知
  - HQ_MANAGERダッシュボード全体を対象部門へドリルダウン

---

### Changed

#### Dashboard連携強化

- `frontend/src/views/DashboardView.vue`
  - `DepartmentProjectChart` に `@select-department` を追加
  - グラフクリック時に `selectedDepartmentId` を更新するよう修正

- ドリルダウン連携対象
  - KPIサマリ
  - 部門ランキング
  - 注視案件一覧
  - 各分析グラフ

- 上部の部門切替ボタンと同じ状態管理へ統一

---

#### 型安全性改善（build対応）

- `frontend/src/views/budget/BudgetListView.vue`
  - `null` を `undefined` に変換してAPIへ渡すよう修正
  - `?? undefined` を適用

- 対象フィルタ
  - `departmentFilter`
  - `min`
  - `max`
  - `sortBy`

- TypeScript build error を解消

---

### Verified

#### Build確認

- `npm run build`

結果：

- Build Success
- TypeScript Error なし
- Vite Build 成功

---

### UX Improvements

#### ダッシュボード分析導線強化

- KPIカードクリック（S7）
- 部門別案件数グラフクリック（S8-1）

### Added

#### 注視部門ランキング ドリルダウン

- `frontend/src/components/dashboard/DepartmentRankingCard.vue`
  - 注視部門ランキングの各部門カードをクリック可能に改善
  - `defineEmits()` を追加し、選択部門IDを親コンポーネントへ通知する仕組みを実装
  - 部門クリック時に `selectDepartment` event を emit するよう対応

- クリック対象
  - 🥇 注視部門ランキング
  - 🥈 注視部門ランキング
  - 🥉 注視部門ランキング

- 動作
  - クリックした部門の `department_id` を親コンポーネントへ通知
  - HQ_MANAGERダッシュボード全体を対象部門へドリルダウン

---

### Changed

#### Dashboard連携強化

- `frontend/src/views/DashboardView.vue`
  - `DepartmentRankingCard` に `@select-department` を追加
  - ランキングクリック時に `selectedDepartmentId` を更新するよう修正

- ドリルダウン連携対象
  - KPIサマリ
  - 部門別案件数
  - 部門別予算消費率
  - 部門別期限超過タスク件数
  - 注視案件一覧

- 上部の部門切替ボタンと同一の状態管理へ統一

---

### UX Improvements

#### ランキングUI改善

- `frontend/src/components/dashboard/DepartmentRankingCard.vue`
  - hover時のカーソル変更を追加
  - hover時の背景色変化を追加
  - hover時の微小アニメーションを追加

---

### Verified

#### Build確認

- `npm run build`

結果：

- Build Success
- TypeScript Error なし
- Vite Build 成功

---

#### 動作確認

- HQ_MANAGERで手動確認実施

確認項目：

- 注視部門ランキングクリックで対象部門へ切替
- 上部の部門切替ボタンと状態同期
- KPIサマリが対象部門へ更新
- 各分析グラフが対象部門へ更新
- 注視案件一覧が対象部門へ更新

結果：

- 正常動作確認済み

---

### Dashboard Analysis Flow

以下の分析導線を実現：

```txt
KPIカード → 詳細一覧（S7）
↓
部門別案件数 → ドリルダウン（S8-1）
↓
注視部門ランキング → ドリルダウン（S8-2）
```

「見る → 気づく → 深掘る」分析UXを強化

### Added

#### タスク一覧インライン編集対応

- `frontend/src/views/projects/ProjectDetailView.vue`

タスク一覧の編集導線を改善し、専用編集画面への遷移を廃止。
案件詳細画面上でタスクの更新が完結するインライン編集機能を追加。

変更前：

```txt
編集アイコン
↓
専用編集画面へ遷移
↓
更新
↓
案件詳細へ戻る
```

変更後：

```txt
編集アイコン
↓
タスク更新ダイアログ表示
↓
一覧画面のまま更新
```

---

#### タスク更新ダイアログ追加

- `el-dialog` を追加
- 編集対象タスクを `editingTask` へ保持
- `destroy-on-close` を適用

編集可能項目：

- 工程名
- タスク名
- ステータス
- 進捗率

---

#### タスク削除機能追加

- 更新ダイアログ内に削除ボタンを追加
- `ElMessageBox.confirm()` による削除確認を追加
- 削除後は一覧を即時再取得

削除フロー：

```txt
削除
↓
確認ダイアログ
↓
削除実行
↓
一覧再取得
```

---

### Changed

#### 編集導線変更

- `goTaskEdit()` を廃止
- `router.push()` による画面遷移を廃止
- `openTaskEditDialog()` を追加

変更内容：

- 編集アイコン押下で対象タスク情報をダイアログへ展開
- 一覧画面のコンテキストを維持したまま編集可能に改善

---

#### 更新処理改善

- `saveTaskEdit()` を追加

更新処理：

- `tasksAPI.updateTask()` を利用
- 更新後に以下を再取得
  - `fetchTasks()`
  - `fetchProject()`

---

#### 型安全性改善

API送信用 payload を明示的に生成し、
レスポンス型と更新型の差異を吸収。

対応内容：

- `null → undefined` 変換を追加

対象：

- `phase_name`
- `description`
- `assignee_id`
- `start_date`
- `due_date`

TypeScript build error を解消。

---

#### 権限制御追加

削除ボタン表示制御を追加。

削除可能：

- `APPLICANT`
- `DEPT_MANAGER`

削除不可：

- `TASK_MEMBER`

---

### UX Improvements

#### タスク操作性向上

従来：

```txt
一覧 → 編集画面 → 戻る
```

改善後：

```txt
一覧 → 編集 / 更新 / 削除
```

一覧画面のまま操作が完結するよう改善。

---

### Verified

#### Build確認

実行：

```bash
npm run build
```

結果：

- Build Success
- TypeScript Error なし
- Vite Build 成功

---

#### 動作確認

確認項目：

- 編集アイコン押下でダイアログ表示
- タスク内容更新
- 更新後一覧へ即反映
- 削除確認ダイアログ表示
- 削除後一覧から即時反映
- 権限別削除ボタン表示確認

結果：

- 正常動作確認済み

### Changed

#### タスク管理UI改善（一覧＋ガント統合）

- `TaskGanttTable.vue` を新規作成
- 従来の「タスク一覧」と「ガントチャート」を統合し、一覧右側へタイムラインを表示する構成へ変更
- 工程名・タスク名・担当者列を `fixed="left"` に変更し、横スクロール時も主要情報を固定表示
- ステータス・進捗率を一覧画面上で直接編集可能なUIへ変更
- ガントバーを一覧と同一画面内で確認できる構成へ改善

---

#### タスク編集UX改善

- 従来の「編集アイコン → 専用編集画面遷移」方式を廃止
- `ProjectDetailView.vue` 上でモーダルによるインライン編集へ変更
- タスク名・工程名・ステータス・進捗率をモーダル内で編集可能に変更
- タスク削除機能を編集モーダルへ統合
- 更新後にタスク一覧・ガント表示へ即時反映される構成へ改善

---

#### ルーティング整理

- `/projects/:projectId/tasks/:taskId/edit` を削除
- `TaskEdit` ルートを削除
- `goTaskEdit()` による画面遷移処理を削除
- 一覧編集への移行に伴い、旧編集導線を整理
- `TaskFormView.vue` は新規タスク登録専用画面として継続利用

---

#### 不要コード整理

- `ProjectDetailView.vue`
  - 不要となった `router.push()` を削除
  - 不要となった `useRouter()` を削除
- 旧編集画面参照が残っていないことを確認済み

---

#### 品質確認

- `npm run build` 成功
- モーダル編集・削除・ガント表示・横スクロール固定表示の手動確認完了

## [fix/security-and-requirements] - 2026-05-06

### Changed

#### PoC方針整理

- PoC方針を「ウォーターフォール型開発案件予実可視化」へ整理
- 「全部入り開発管理システム」ではなく、進捗・予算可視化を重視したPoCへスコープを明確化
- README / user_manual / ER設計 / future_proposals の記載内容を統一

---

#### フロントエンドUI整理

- 開発手法選択UIを削除
- AGILE関連表現を整理
- ウォーターフォール型案件管理前提のUI・説明へ統一

---

#### README.md 更新

- PoC概要を「予実可視化」「KPI監視」中心へ修正
- PoCスコープ説明を追加
- ウォーターフォール型案件管理前提へ表現統一
- 将来拡張項目を整理
- AGILE関連記述を削除

---

#### user_manual.md 更新

- 開発手法選択手順を削除
- ウォーターフォール型運用前提の説明を追加
- phase_name（工程管理）の説明を追加
- KPI / アラートダッシュボード説明を整理
- 操作説明・用語をREADMEと統一

---

#### er_design.md 更新

- ER設計概要をPoC方針に合わせて整理
- development_method カラム残置理由を追記
- phase_name の用途説明を追加
- AGILE を「将来拡張用」として整理

---

### Notes

- DB上の `development_method` カラムは将来的なアジャイル案件対応を考慮し保持
- 現行UIではウォーターフォール型案件管理のみを対象とする

---

#### dashboard_service.py 改善

- alerts を監視KPIの単一ソースとして再整理
- DashboardSummary 用 KPI を alerts から集計する構成へ統一
- danger / warning / overdue / SPI / CPI を summary API へ追加
- KPI監視型ダッシュボード向けレスポンス構成へ改善
- HQ_MANAGER / DEPT_MANAGER / TASK_MEMBER のロール別対象案件取得を整理

---

#### useDashboard composable 整理

- summaryData へ監視KPI項目を追加
- dashboard API レスポンスと frontend state の整合性を整理
- KPI集計値を DashboardSummaryCards へ連携
- 未使用 summary 項目を整理

---

#### DashboardSummaryCards レイアウト改善

- el-row / el-col ベース構成から CSS Grid ベース構成へ変更
- KPIカードのレスポンシブ表示を改善
- KPI数増加時のカード崩れを解消
- KPI件数表示を強調し監視視認性を改善

---

#### ダッシュボードKPI監視型改善

- DashboardSummaryCards を監視KPI中心構成へ変更
- 「危険案件」「注意案件」「SPI低下案件」「CPI低下案件」「期限超過タスク」を主要KPIとして整理
- 完了件数・単純進行中件数など監視価値の低い指標を削減
- KPIカードへ補足説明文を追加し、監視意図を明確化
- KPIカードUIの配色・視認性を改善

---

#### DashboardView 整理

- DashboardView の責務を親コンテナへ整理
- DashboardSummaryCards / DashboardProjectList へ責務分離
- 未使用コード・不要Alert表示を整理
- 上部「期限超過Alert」表示を削除
- KPI監視型ダッシュボード構成へ整理

---

#### DashboardProjectCard 強化

- 案件カードタイトル行へ SPI / CPI / 期限超過件数を追加
- danger / warning 状態をより視覚的に判別できるよう改善
- KPIタグをタイトル行へ追加し、カードを開かずに状況把握可能化
- 「案件詳細を見る」ボタンUIを改善
- カードhover時の視認性を改善
- KPI監視型案件カードUIへ整理

---

#### DashboardAlertDetail 強化

- SPI / CPI / 期限超過タスクを常時表示へ変更
- Popover依存だった詳細指標を監視指標として常時可視化
- 「進捗遅延」「予算超過傾向」「SPI低下」「CPI低下」「期限超過あり」など危険理由タグを追加
- KPI表示レイアウトを整理
- 監視指標の色分け・視認性を改善
- 承認権限に依存しないKPI表示へ変更

---

#### DashboardTodayTasks 改善

- カテゴリ別表示件数を調整（5件 → 3件）
- タスク行クリックで案件詳細へ遷移可能化
- タスクカードUIを改善
- 今日期限 / 今日開始 / 進行中 の視認性を改善
- hover時の操作感を改善
- HQ_MANAGERでは個別タスクを非表示化し、ロール別情報最適化の土台を整理

---

#### ロール別ダッシュボード方針整理

- HQ_MANAGER：
  KPI・危険案件監視中心

- DEPT_MANAGER：
  部門案件・危険案件・予算監視中心

- APPLICANT / PM：
  今日の対応タスク・進捗確認中心

- 完全分離ではなく「表示内容調整」による軽量ロール差別化方針を整理

#### WFタスク未登録警告機能追加

- 案件着手時にタスク未登録状態を検知する確認処理を追加
- タスク0件状態で「着手する」を押下した際、警告ダイアログを表示するよう改善
- 「ウォーターフォール型案件ではタスク登録を推奨する」旨の確認メッセージを追加
- タスク未登録でも実務上の柔軟性を考慮し、着手継続可能な設計を採用
- キャンセル時は案件ステータス更新を中断するよう改善
- useProjectActions に着手前確認フックを追加し、ProjectDetailView と疎結合で連携
- DB / API変更を伴わないフロントエンド改善として実装

#### タスク更新権限制御の修正

- 申請者が自案件のタスク更新画面へ遷移できない問題を修正
- 部門管理者がタスク編集ボタン押下時にダッシュボードへ戻される問題を修正
- タスク更新ルートの許可ロールを APPLICANT / DEPT_MANAGER / TASK_MEMBER に整理
- 本部管理者はタスク編集対象外とし、KPI監視・案件確認中心の権限設計へ整理
- 担当者は自分に割り当てられたタスクのみ編集可能とする方針を維持

---

#### ガントチャートWF工程順改善

- ガントチャートのタスク並び順をウォーターフォール工程順へ整理
- phase_name の文字列順ではなく、WF工程定義順で表示するよう改善
- 「調査 → 要件定義 → 設計 → 実装 → テスト → リリース」の自然な工程順表示へ変更
- 開始日順のみでは発生していた工程順の違和感を解消
- 未定義工程は末尾表示とするフォールバック処理を追加

---

#### ガントチャート構成整理

- `gantt.constants.ts` を新規追加
- ガントチャート固定列幅定数を外部化
- WF工程順定義（PHASE_ORDER）を定数化
- ガント関連定義の責務を分離

---

#### useGanttTasks.ts 追加

- ガントチャート用タスク処理を composable 化
- visibleTasks の filter / sort 処理を分離
- 担当者フィルター処理を composable へ移動
- 工程順取得処理を共通化
- GanttChart.vue の責務を軽量化

---

#### GanttChart.vue 整理

- gantt.constants.ts / useGanttTasks.ts を利用する構成へ変更
- ガントチャート内の工程順ロジックを整理
- 担当者一覧取得ロジックを composable へ移動
- タスク並び替え責務を composable へ分離
- GanttChart.vue を表示中心コンポーネントへ整理

---

#### 定数管理整理

- `PHASE_ORDER` の重複定義を解消
- WF工程順定義を `src/constants/task.ts` へ統一
- gantt / task 間で工程定義を共通利用する構成へ整理
- 定数分散による保守性低下を解消

---

#### タスク登録ガイド追加

- TaskFormView に「推奨タスク粒度ガイド」を追加
- タスク粒度・PM向け運用想定を明示
- TaskGuideAlert.vue を新規追加し責務を分離
- タスク関連定数を `src/constants/task.ts` へ集約
- WF工程定義（WATERFALL_PHASES）を共通化
- タスク登録画面の説明責務をコンポーネント分離

---

#### 実務フィードバック資料更新

- `user_feedback_report-2.md` へ各レビュー項目の「対応状況」を追記
- 「実装済み」「PoC範囲外」「課題２将来拡張」の分類を追加
- 実務レビューからPoCスコープ整理までの改善履歴を明文化
- フィードバック資料を提出物として活用できる構成へ改善

---

#### ドキュメント構成整理

- フィードバック関連資料を `doc/feedback/` 配下へ集約
- 実務レビュー資料と設計資料の責務を分離
- 提出物確認時の参照性を改善

## [fix/security-and-requirements] - 2026-05-05

### Updated

#### 提出物監査を実施し提出ドキュメントを調整

##### Information.md

- `doc/Information.md` の配置を課題指定に合わせて確認・修正
- 動作確認用テストアカウント一覧を seed.py と照合し整合性を確認
- ロール表記をシステム正式名称へ統一
  - `TASK_MEMBER（担当者）`
  - `APPLICANT（申請者）`
  - `DEPT_MANAGER（部門管理者）`
  - `HQ_MANAGER（本部管理者）`
- Swagger URL記載を見直し、実際の公開状態と整合する内容へ修正

##### README.md

- 評価者が最短で確認できるようデモ環境導線を追加
  - デプロイURL
  - テストアカウント参照先
- `TASK_MEMBER` を含む4ロール構成へ表記統一
- 「進行中・予定」を削除し、提出用ドキュメントとして誤解のない構成へ調整
- cloneコマンド・ディレクトリ構成・提出資料導線を整理

##### doc構成

- 課題指定に合わせ `docs/ → doc/` へ変更
- `Information.md` のファイル名を課題指定に合わせて統一
- 提出資料の命名規則・配置を最終確認
  - `Information.md`
  - `er_design.md`
  - `presentation_安成鎔.pdf`
  - `future_proposals.md`

---

### Proposed

#### 利用者フィードバックをもとに今後の機能改善案を整理

- `user_feedback_report.md` をもとにプレゼン資料への反映内容を整理

##### タスク実績管理の改善案

- 予定開始日とは別に `started_at`（実績開始日）を追加する設計を提案
- 計画日と実績日の差異分析を可能にし、スケジュール精度向上に活用可能

##### レビュー依頼ワークフローの改善案

- TASK_MEMBER：
  - `IN_PROGRESS → REVIEW_REQUEST`

- APPLICANT：
  - `REVIEW`

- 将来的に品質保証を考慮したレビュー承認フローへ拡張可能

---

### Verified

#### 提出物監査

##### Information.md

- 課題指定パス `doc/Information.md` に配置されていることを確認
- 全ロール分のテストアカウント情報が seed.py と一致することを確認

##### README.md

- 課題要件・追加提案・セットアップ手順が最新内容と整合していることを確認

##### デプロイURL

- 外部回線からログイン画面が正常表示されることを確認
- CSS崩れ・Consoleエラーがないことを確認

##### 提出ファイル構成

- 提出必須ファイルが揃っていることを確認
- placeholder名や不要な命名が残っていないことを確認

## [fix/security-and-requirements] - 2026-05-04

### Fixed

#### セキュリティ修正

- `backend/app/services/task_service.py`
  - `get_tasks` に `check_project_access` を追加し、別部門ユーザーが他部門のタスク一覧を取得できるIDOR脆弱性を修正
  - `get_all_tasks` の `UserRole.HEADQUARTERS` を `UserRole.HQ_MANAGER` に修正（AttributeErrorによるクラッシュバグを解消）
  - `_check_project_approved` の対象ステータスに `IN_PROGRESS` を追加（進行中案件のタスク更新が400エラーになる問題を修正）

- `backend/app/services/budget/budget_service.py`
  - `get_budget` に `check_project_access` を追加し、別部門ユーザーが他部門の予算データを取得できるIDOR脆弱性を修正

- `backend/app/services/project/project_service.py`
  - `create_project` の `Project` コンストラクタに `development_method` を追加（案件申請時に開発手法が保存されないバグを修正）

#### TASK_MEMBERロール実装完結

- `backend/app/services/project/permission_service.py`
  - `check_project_access` にTASK_MEMBERの分岐を追加（自部門の案件のみアクセス可能）

- `backend/app/services/project/query_service.py`
  - `apply_project_filters` にTASK_MEMBERの分岐を追加（自部門の案件のみ一覧取得可能）

- `backend/app/services/task_service.py`
  - `update_task` にTASK_MEMBERの権限チェックを追加（自部門の案件内であれば他メンバーのタスクも更新可能）

- `backend/app/scripts/seed.py`
  - TASK_MEMBERアカウント（亀田 大輔・斉藤 彩香・林 直樹・中村 葵）のパスワードを固定値（`password`）に変更しログイン可能に

- `frontend/src/router/index.ts`
  - `task-edit` ルートの `roles` に `TASK_MEMBER` を追加

#### ドキュメント修正

- `docs/提出物/マニュアル.md`
  - ロール別機能一覧に担当者（TASK_MEMBER）列を追加
  - 担当者向け操作手順（第6章）を新規追加
  - 以降の章番号を繰り上げ（6→7・7→8・8→9・9→10）
  - テストアカウント一覧にTASK_MEMBERアカウント4名を追加

- `docs/提出物/Information.md`
  - テストアカウント一覧にTASK_MEMBERアカウント4名を追加

### Performance

#### SQLクエリ最適化

- `backend/app/services/response_service.py`
  - `_calc_progress` のタスク進捗率計算をPythonループから SQL `AVG` に変更
  - 案件一覧取得時に案件数N回発行されていたSELECTクエリを1回に削減

- `backend/app/services/dashboard_service.py`
  - `get_dashboard_summary` の未読通知カウントをPython全件取得から SQL `COUNT` に変更
  - `from sqlalchemy import func` を追加

#### フロントエンドバグ修正

- `frontend/src/views/budget/BudgetView.vue`
  - 承認前ステータス（DRAFT・PENDING_DEPT・PENDING_HQ・REJECTED）の案件で予算管理画面を開いた際に `worklogs`・`expenses` のAPIが404エラーを返す問題を修正
  - `onMounted` の処理を変更し、案件取得後にステータスを確認してから `worklogs`・`expenses`・`budget` を取得する形に変更（`APPROVED`・`IN_PROGRESS`・`COMPLETED` のみAPIを呼び出す）
- `backend/app/services/budget/worklog_service.py`
  - `get_worklogs` に `check_project_access` を追加し、別部門ユーザーが他部門の工数実績を取得できるIDOR脆弱性を修正

- `backend/app/services/budget/expense_service.py`
  - `get_expenses` に `check_project_access` を追加し、別部門ユーザーが他部門の直接経費を取得できるIDOR脆弱性を修正

### Changed

#### ダッシュボードUX改善

- `frontend/src/views/DashboardView.vue`
  - ページタイトル（`page-header`・`page-title`）を削除
  - セクションタイトルを「案件状況・今日の対応タスク」から「本日の案件状況」に変更
  - 期限超過タスクが1件以上ある場合のみ画面上部にアラートバナー（`el-alert`）を表示する機能を追加
  - `.overdue-alert` スタイルを追加

- `frontend/src/components/dashboard/DashboardSummaryCards.vue`
  - 期限超過カードを削除（アラートバナーに移行したため）
  - `Warning` アイコンのimportを削除
  - `SummaryData` インターフェースから `overdueTaskCount` を削除
  - `.compact-icon.overdue` スタイルを削除

#### ダッシュボードUX改善

- `frontend/src/components/dashboard/DashboardProjectCard.vue`
  - `el-collapse` に `project-card` クラスを追加し枠線・角丸・影を追加
  - `.project-title-row` の縦中央寄せを修正（`:deep(.el-collapse-item__header)` で調整）

- `frontend/src/components/dashboard/DashboardProjectList.vue`
  - `.el-col .el-collapse` に `margin-bottom: 0` を追加

- `frontend/src/views/DashboardView.vue`
  - 「本日の案件状況」カードを `project-list-card` クラスで枠線表示に変更
  - `DashboardProjectList` をカード外に分離しプロジェクトごとの枠表示を実現
  - `.project-list-card` スタイルを追加

- `frontend/src/components/dashboard/DashboardAlertDetail.vue`
  - `.alert-detail-section` の左右パディングを `0` から `16px` に変更し内容を右寄せ

#### 進行中案件一覧のUX改善

- `frontend/src/components/projects/ApplicantProjectTable.vue`
  - ステータス・承認ステップ列の非表示条件を `IN_PROGRESS` のみから `APPROVED` または `IN_PROGRESS` フィルター時に拡張

- `frontend/src/components/AppHeader.vue`
  - 「進行中案件」メニューのリンク先を `/projects?status=APPROVED,IN_PROGRESS` に統一

- `frontend/src/components/dashboard/DashboardSummaryCards.vue`
  - 「進行中」カードのリンク先を `/projects?status=APPROVED,IN_PROGRESS` に統一

#### 工数実績一覧への金額列追加

- `frontend/src/views/budget/BudgetView.vue`
  - 工数実績一覧に「金額（円）」列を追加
  - `実績工数（人月） × 単価` の計算結果を表示（単価未設定の場合は「—」を表示）

#### ガントチャート修正

- `frontend/src/components/projects/GanttChart.vue`
  - ウォーターフォール型のタスク並び順を `phase_name` の五十音順から `start_date`（開始日）の昇順に変更（工程順が正しく表示されるよう修正）
  - 横スクロール時に工程・担当者・作業詳細列が固定されるよう `position: sticky` を適用
  - `PHASE_WIDTH`・`PERSON_WIDTH`・`TASK_WIDTH` を定数化しインラインスタイルで参照する形に変更
  - `border-collapse` を `separate` に変更し `position: sticky` との組み合わせによる表示崩れを修正
  - ウォーターフォール型・アジャイル型それぞれで固定列の `left` 値を正しく算出するよう対応

#### 予算管理 絞り込み・ソート機能追加

- `backend/app/services/project/query_service.py`
  - `apply_project_filters` に `department_id`・`budget_min`・`budget_max` フィルタ条件を追加

- `backend/app/services/project/project_service.py`
  - `get_projects` に `department_id`・`budget_min`・`budget_max`・`sort_by`・`sort_order` パラメータを追加
  - `_apply_project_sort` 関数を追加（`budget_amount` による昇順・降順ソートに対応・未指定時は作成日降順を維持）

- `backend/app/services/budget/budget_summary_service.py`
  - `get_budget_summary` に `department_id`・`budget_min`・`budget_max` パラメータを追加しフィルタに連動

- `backend/app/routers/projects.py`
  - `GET /api/projects` に `department_id`・`budget_min`・`budget_max`・`sort_by`・`sort_order` クエリパラメータを追加
  - `GET /api/projects/budget-summary` に `department_id`・`budget_min`・`budget_max` クエリパラメータを追加

- `frontend/src/api/projects.ts`
  - `getProjects` に `departmentId`・`budgetMin`・`budgetMax`・`sortBy`・`sortOrder` パラメータを追加
  - `getBudgetSummary` に `departmentId`・`budgetMin`・`budgetMax` パラメータを追加
  - `ProjectSortBy`・`SortOrder` 型を追加

- `frontend/src/views/budget/BudgetListView.vue`
  - 部門絞り込みセレクト（本部管理者のみ表示）を追加（BL1対応）
  - 予算帯絞り込みセレクト（〜500万・500万〜1000万・1000万〜）を追加（BL2対応）
  - 予算列にサーバーサイドソート（`sortable="custom"`）を追加（BL3対応）
  - `handleSortChange` でソート変更時にAPIを再取得するよう実装
  - `fetchData` でフィルタ・ソートパラメータをAPIに渡すよう変更
  - フィルタ変更時はページを1にリセットしてからAPI再取得（`watchDebounced` で300msデバウンス）
  - サマリーカードがフィルタと連動して更新されるよう対応

### Removed

#### 未使用コードの削除

- `frontend/src/types/common.ts`
  - `ApiResponse`・`ApiError` 型が `api/client.ts` で独自定義されており参照されていないためファイルごと削除

- `backend/app/schemas/notification.py`
  - `NotificationUpdate` クラスを削除（どこからも参照されていないため）

- `backend/app/services/notification_service.py`
  - `create_notification` 関数を削除（どこからも呼び出されていないため）

- `backend/app/services/project/query_service.py`
  - `paginate` 関数を削除（`project_service.py` で独自に `count / offset / limit` を実装しており使用されていないため）

## [Unreleased] - 2026-04-28

### Added

#### ダッシュボード機能強化

- 案件状況・今日の対応タスクセクションを統合（アラートダッシュボードと当日タスクを一元表示）
- 今日の対応タスクを3分類（今日期限・今日開始・進行中）で表示する機能を追加
- 案件カードをアラートレベル順（danger → warning → 今日タスクあり → 通常）に自動ソート
- カテゴリ別タスク件数上限（5件）と「他N件」リンク表示を追加
- サマリカードを左サイドバー縦列に再配置し、案件状況エリアを拡大
- ダッシュボードコンポーネントを分離（DashboardSummaryCards / DashboardProjectList / DashboardProjectCard / DashboardAlertDetail / DashboardTodayTasks）
- composableを分離（useDashboard / useDashboardActions）

#### バックエンド

- `dashboard_service.py` に当日タスク取得ロジック（`_get_today_tasks`）を追加
- `get_dashboard_summary` のレスポンスに `projects` フィールドを追加
- `_get_target_tasks` に `joinedload(Task.assignee)` を追加しN+1問題を解消

#### API型定義

- `dashboard.ts` に `TodayTask`・`ProjectDashboard` 型を追加
- `DashboardResponse` に `projects` フィールドを追加

#### シードデータ

- `seed.py` の全日付を実行日基準の相対日付に変更し、当日タスクが常に表示されるよう改善

#### ドキュメント・環境整備

- ER設計ドキュメントを更新
  - `users.role` に `TASK_MEMBER` を追加
  - `projects` に `development_method` カラムを追加
  - `tasks` に `phase_name`・`description` カラムを追加
  - `departments`・`notifications` のタイムスタンプカラムを修正
  - `DevelopmentMethod` Enum を追加
- 利用マニュアル（`manual.md`）を作成（全ロール向け操作手順）
- `Information.md` を作成（デプロイURL・テストアカウント一覧）
- プレゼンテーション資料（`presentation_{おなまえ}.pdf`）を作成（15枚構成）
- Windows開発環境に Git for Windows を導入し、Git Bash 実行環境を構築
- `deploy_check.sh` の動作検証を実施（環境変数ファイル確認・Dockerコンテナ稼働確認・Frontend Build まで正常動作を確認）
- `deploy_check.sh` を強化し以下の自動チェック機能を追加
  - backend Ruff によるコード品質チェック
  - Alembic 現在バージョン確認
  - Git 作業差分確認
  - `.env` と `backend/.env` の `DATABASE_URL` 整合性チェック
- 過去の環境変数不一致によるDB接続障害を踏まえ、デプロイ前自動確認体制を整備

### Fixed

- `GET /api/users/department/{department_id}` の権限制御を修正
  - 申請者・メンバーが自部門のメンバー一覧を取得できない問題を解消
  - 申請者・部門管理者・メンバーは自部門のみ参照可能、本部管理者は全部門参照可能に変更

### Changed

- ダッシュボードの通知カードを期限超過タスクカードに変更
- 案件申請カードをダッシュボードから削除（ヘッダーナビゲーションに統合済みのため）
- アラート詳細の詳細指標表示を `el-collapse` から `el-popover` に変更（二重collapse解消）
- Windows / Linux 双方で利用可能なデプロイ運用方法に整理

## [feature/improvements] - 2026-04-27

### Added

#### TASK_MEMBERロール追加

- `app/models/user.py`
  - `UserRole`に`TASK_MEMBER`を追加

- `alembic/versions/001_create_initial_tables.py`
  - usersテーブルのroleカラムに`TASK_MEMBER`を追加
  - projectsテーブルに`development_method`カラムを追加
  - projectsテーブルのstatusに`IN_PROGRESS`・`COMPLETED`を追加
  - tasksテーブルに`phase_name`カラムを追加

- `app/scripts/seed.py`
  - 亀田 大輔・斉藤 彩香・林 直樹・中村 葵を`TASK_MEMBER`として新規追加（ダミー認証情報）
  - 各案件に`development_method`を設定
  - ウォーターフォール型案件のタスクに`phase_name`を設定

#### 開発手法（ウォーターフォール/アジャイル）対応

- `app/models/project.py`
  - `DevelopmentMethod` Enumを追加（`WATERFALL`・`AGILE`）
  - `development_method`カラムを追加

- `app/schemas/project.py`
  - `ProjectCreate`・`ProjectUpdate`・`ProjectResponse`に`development_method`を追加

- `app/schemas/task.py`
  - `TaskCreate`・`TaskUpdate`・`TaskResponse`に`phase_name`・`assignee_name`を追加

- `app/services/task_service.py`
  - `_to_response`関数を追加（`phase_name`・`assignee_name`を付与）
  - 各関数の戻り値を`_to_response`経由に変更

- `frontend/src/types/project.ts`
  - `DevelopmentMethod`型を追加
  - `Project`・`ProjectCreate`型に`development_method`を追加

- `frontend/src/types/task.ts`
  - `Task`・`TaskCreate`型に`phase_name`・`assignee_name`を追加

- `frontend/src/views/projects/ProjectNewView.vue`
  - 開発手法の選択UI（ウォーターフォール型・アジャイル型）を追加
  - `development_method`を必須バリデーション付きで追加

- `frontend/src/views/tasks/TaskFormView.vue`
  - 案件の`development_method`に応じて工程名フィールドの表示・非表示を切り替え
  - 部門メンバー取得を`getDepartmentUsers`APIに変更（TASK_MEMBER含む）

#### ガントチャート実装

- `frontend/src/components/projects/GanttChart.vue`（新規）
  - ウォーターフォール型・アジャイル型の表示切り替えに対応
  - 担当者フィルター・日/週/月表示切り替えを実装
  - 工程列（ウォーターフォール型のみ）・本日ラインを実装
  - 工程順・担当者順のソートを実装

#### アラートダッシュボード実装

- `app/services/dashboard_service.py`（新規）
  - A案（差分方式）でアラートレベルを判定
  - SPI・CPI・スケジュール乖離・予算乖離・期限超過タスク数を計算
  - 部門管理者・本部管理者・申請者のロール別データ取得に対応

- `app/routers/dashboard.py`（新規）
  - `GET /api/dashboard`エンドポイントを追加
  - `GET /api/dashboard/alerts`エンドポイントを追加

- `app/routers/admin_tasks.py`（新規）
  - `GET /api/tasks/all`エンドポイントを追加（本部管理者専用）

- `app/main.py`
  - `dashboard`・`admin_tasks`ルーターを登録

- `frontend/src/api/dashboard.ts`（新規）
  - `dashboardAPI`を追加（`getDashboard`・`getAlerts`）

- `frontend/src/views/DashboardView.vue`
  - アラートダッシュボードセクションを追加（部門管理者・本部管理者のみ）
  - `dashboardAPI.getDashboard()`でバックエンドに計算を委譲
  - 主要導線カードを整理（申請者向け案件申請カードのみ残す）

#### メンバータスク状況強化

- `frontend/src/views/members/MemberTaskView.vue`
  - メンバーごとのサマリカードを追加（担当タスク数・進行中・完了・未着手・完了率）
  - 期限超過タスクがあるメンバーのカードを赤背景で強調
  - 余裕ありメンバーに「余裕あり」バッジを表示

### Changed

- `frontend/Dockerfile.prod`
  - ビルド時に`VITE_API_BASE_URL`環境変数を受け取る`ARG`・`ENV`を追加

- `docker-compose.prod.yml`
  - `frontend`の`build.args`に`VITE_API_BASE_URL`を追加
  - `.env.production`への依存を廃止

- `backend/.env.example`
  - `MAIL_FROM`・`MAIL_FROM_NAME`を本システム用に修正

- `backend/app/scripts/seed.py`
  - 新規ユーザー追加（亀田 大輔・斉藤 彩香）
  - `project_p1`のタスクを田中 翔太・亀田 大輔で分担
  - `project_c1`のタスクを佐藤 美咲・斉藤 彩香で分担
  - `project_p4`にタスクを追加（亀田 大輔と田中 翔太で分担）
  - `project_c5`にタスクを追加（斉藤 彩香と佐藤 美咲で分担）
  - 新規ユーザーへのアサイン通知を追加

- `frontend/src/composables/useProjectTable.ts`
  - `goToProject`関数・`useRouter`を削除

- `frontend/src/components/projects/ApplicantProjectTable.vue`
  - 案件名を`router-link`から`span`+`@click`に変更
  - `@click.middle.prevent`で中クリックを無効化
  - `@row-click`・`row-class-name`・`clickable-row`スタイルを削除
  - 「開発手法」列を追加

- `frontend/src/components/projects/DeptManagerProjectTable.vue`
  - 同上

- `frontend/src/components/projects/HqManagerProjectTable.vue`
  - 同上

- `frontend/src/views/DashboardView.vue`
  - サマリーカードに`@click.middle.prevent`と`openInNewTab`を追加
  - `openInNewTab`関数を追加

- `frontend/src/components/AppHeader.vue`
  - 通知アイコンに`@click.middle.prevent`と`openInNewTab`を追加
  - `openInNewTab`関数を追加

- `frontend/src/views/projects/ProjectDetailView.vue`
  - 案件情報に「開発手法」項目を追加
  - タスク一覧・予算サマリを折りたたみ可能に変更
  - タスク一覧にウォーターフォール型のみ「工程名」列を追加
  - ガントチャートコンポーネントを組み込み

- `app/services/query_service.py`
  - `check_project_approved`の対象ステータスに`IN_PROGRESS`・`COMPLETED`を追加

- `app/schemas/user.py`
  - `UserResponse`の`email`フィールドを`EmailStr`→`str`に変更（TASK_MEMBERのダミーメール対応）

### Fixed

- 本番環境で`VITE_API_BASE_URL`が`localhost:8000`にハードコードされる問題を修正
  - `Dockerfile.prod`でビルド時に環境変数を渡す形に変更

- `app/services/dashboard_service.py`
  - `datetime.datetime`と`datetime.date`の比較エラーを修正（`.date()`変換を追加）
  - 申請者ロールでの403エラーを修正（ロール別データ取得分岐を追加）

## [feature/improvements] - 2026-04-25

### Changed

- `frontend/src/views/projects/ProjectDetailView.vue`
  - `fetchBudget`に`isStarted`チェックを追加
  - 承認済み以降の案件のみ予算取得APIを呼び出す形に変更
  - 404・400エラーは予算未登録の正常系として静かに処理

## [feature/responsive] - 2026-04-25

### Changed

#### 課題2：レスポンシブ対応の強化

- `frontend/src/components/AppHeader.vue`
  - `@vueuse/core`の`useWindowSize`を使用してモバイル判定を実装
  - スマートフォン時（768px未満）にハンバーガーメニューを表示
  - `el-drawer`によるモバイル用ドロワーメニューを実装
  - スマートフォン時はユーザー名・ロール表示を非表示に変更
  - `Expand`・`Close`アイコンによるメニュー開閉を実装

## [feature/member-task-status] - 2026-04-25

### Added

#### 課題2：メンバー別タスク状況一覧の実装

- `backend/app/services/project/permission_service.py`
  - `check_dept_access`関数を追加（部門へのアクセス権限チェック）

- `backend/app/services/task_service.py`
  - `get_department_tasks`関数を追加（部門内全案件のタスク一覧取得）

- `backend/app/services/user_service.py`
  - `get_users_by_department`関数を追加（部門メンバー一覧取得）

- `backend/app/routers/departments.py`
  - `GET /api/departments/{department_id}/tasks` エンドポイントを追加

- `backend/app/routers/users.py`
  - `GET /api/users/department/{department_id}` エンドポイントを追加

- `frontend/src/api/tasks.ts`
  - `getDepartmentTasks`を追加

- `frontend/src/api/users.ts`
  - `getUsers`・`getDepartmentUsers`を追加

- `frontend/src/views/members/MemberTaskView.vue`
  - 部門管理者向けメンバー別タスク状況一覧画面を新規作成
  - 担当者フィルター・ステータスフィルターを実装
  - 期限超過タスクの赤色強調表示を実装

- `frontend/src/router/index.ts`
  - `/members/tasks`ルートを追加（DEPT_MANAGERのみ）

- `frontend/src/components/AppHeader.vue`
  - DEPT_MANAGERのナビゲーションに「メンバー状況」を追加

## [refactor/frontend-structure] - 2026-04-25

### Changed

#### フロントエンド構造整理・バグ修正

- `frontend/src/composables/usePagination.ts`
  - 未使用ファイルのため削除

- `frontend/src/views/budget/BudgetListView.vue`
  - `fetchData`内の`departmentsAPI.getDepartments()`重複呼び出しを修正
  - `onMounted`で1回のみ取得する形に変更

- `frontend/src/views/budget/BudgetView.vue`
  - `summary` computedのフロントエンド再計算を廃止
  - 実績金額・消化率をバックエンドの`budget.actual_amount`から算出する形に変更

- `frontend/src/components/AppHeader.vue`
  - `notificationsAPI.getNotifications()`のレスポンス形式変更に対応
  - `.data.filter()`を`.data.items.filter()`に修正

- `frontend/src/views/DashboardView.vue`
  - 同上・`.data.filter()`を`.data.items.filter()`に修正

- `backend/app/schemas/budget.py`
  - `ProjectBudgetResponse`に`consumption_rate`フィールドを追加

- `backend/app/services/budget/budget_service.py`
  - `_to_budget_response`関数を追加
  - `create_budget`・`get_budget`・`update_budget`の戻り値に`consumption_rate`を付与

- `frontend/src/types/budget.ts`
  - `ProjectBudget`型に`consumption_rate`フィールドを追加

- `frontend/src/views/projects/ProjectDetailView.vue`
  - 予算サマリの金額消化率をフロントエンド再計算から`budget.consumption_rate`に変更

## [refactor/frontend-style] - 2026-04-25

### Added

#### フロントエンドグローバルCSS対応

- `frontend/src/assets/styles/variables.css` を新規作成
  - CSS変数（--page-padding / --card-margin-bottom / --form-hint-color等）を定義

- `frontend/src/assets/styles/typography.css` を新規作成
  - `.page-title` / `.page-subtitle` をグローバル化

- `frontend/src/assets/styles/layout.css` を新規作成
  - `.page-header` / `.card-header` / `.pagination-wrapper` / `.form-actions` をグローバル化

- `frontend/src/assets/styles/utilities.css` を新規作成
  - `.mb-16` / `.mt-16` / `.text-gray` / `.form-hint` / `.project-name-link` をグローバル化

- `frontend/src/main.ts`
  - 上記4ファイルのimportを追加

### Changed

- 以下の各Vueファイルの`<style scoped>`からグローバルCSSに移行済みの重複クラスを削除
  - `ApprovalView.vue`
  - `BudgetListView.vue`
  - `BudgetView.vue`
  - `ProjectDetailView.vue`
  - `DashboardView.vue`
  - `ExpenseFormView.vue`
  - `WorklogFormView.vue`
  - `ProjectListView.vue`
  - `ProjectNewView.vue`
  - `TaskFormView.vue`
  - `NotificationView.vue`
  - `ApplicantProjectTable.vue`
  - `DeptManagerProjectTable.vue`
  - `HqManagerProjectTable.vue`

## [docs/update-design-documents] - 2026-04-25

### Updated

#### 設計ドキュメントの更新

- `docs/db/er_design.md`
  - 各テーブルのカラム情報を追加
  - Enum定義セクションを追加
  - ProjectStatusに`IN_PROGRESS`・`COMPLETED`を反映
  - `projects ||--o{ notifications`のリレーションを追加

- `docs/design/api_design.md`
  - BaseURLを`/api/v1`から`/api`に修正
  - `departments`エンドポイントを追加
  - 案件APIにページネーション・フィルター・着手・完了・budget-summaryエンドポイントを追加
  - 通知APIにWebSocket・ページネーションを追加
  - ProjectStatusに`IN_PROGRESS`・`COMPLETED`を追加
  - TaskStatusを`TODO`・`DONE`に修正

- `docs/design/functions.md`
  - 着手・完了操作・ページネーション・リアルタイム通知等を追加
  - TaskStatusを`TODO`・`DONE`に修正

- `docs/db/status_design.md`
  - `IN_PROGRESS`・`COMPLETED`を追加
  - ステータス遷移図（Mermaid）を追加
  - 操作権限テーブルを追加
  - TaskStatusを`TODO`・`DONE`に修正・進捗率連動テーブルを追加

- `docs/db/tables/projects.md`
  - カラム定義を実装に合わせて更新
  - `IN_PROGRESS`・`COMPLETED`をENUMに追加
  - `start_date`・`end_date`を追加
  - `approved_by`・`approved_at`を削除

- `docs/Information.md`
  - Swagger UIのURLを追加
  - 起動手順にマイグレーション・seed・テスト実行コマンドを追記
  - DBリセット手順を追加

- `docs/design/role_matrix.md`
  - 着手・完了操作を追加
  - リアルタイム通知・ダッシュボードを追加

- `docs/memo/requirements_phase1.md`
  - 着手・完了操作・BR-10・BR-11を追加
  - ページネーション・バリデーション制限を反映

- `docs/usecases/usecase_applicant.md`
  - UC-A04（着手操作）を追加
  - UC-A05〜A08を繰り下げ・内容を更新

- `docs/usecases/usecase_dept_manager.md`
  - UC-D04（着手・完了操作）を追加
  - ページネーション・フィルター・サマリーカードを追記

- `docs/usecases/usecase_hq_manager.md`
  - UC-H04（着手・完了操作）を追加
  - ページネーション・フィルター・サマリーカードを追記

- `README.md`
  - services/ディレクトリ構成をproject/・budget/サブディレクトリに更新
  - 進行中・予定に課題2の実装項目を追加

## [feature/notification-pagination] - 2026-04-24

### Added

#### 通知一覧のページネーション実装

- `backend/app/schemas/notification.py`
  - `NotificationListResponse` を追加（total / page / limit / items）

- `backend/app/services/notification_service.py`
  - `get_notifications` をページネーション対応に変更（戻り値を `NotificationListResponse` に変更）
  - page・limitの防御処理を追加（page: min 1、limit: 10〜100）

- `backend/app/routers/notifications.py`
  - `GET /api/notifications` にページネーションパラメータ（page / limit）を追加

- `frontend/src/types/notification.ts`
  - `NotificationListResponse` 型を追加

- `frontend/src/api/notifications.ts`
  - `getNotifications` にページネーションパラメータを追加

- `frontend/src/views/NotificationView.vue`
  - ページネーションUI（`el-pagination`）を追加
  - `fetchNotifications` をページネーション対応に変更
  - `handleReadAll` を全件既読後に再取得する形に変更

## [refactor/backend-service-structure] - 2026-04-24

### Changed

#### バックエンド サービス層のディレクトリ整理

- `backend/app/services/project/`ディレクトリを新規作成
  - `project_service.py` を移動
  - `approval_service.py` を移動
  - `permission_service.py` を移動
  - `query_service.py` を移動
- `backend/app/services/budget/`ディレクトリを新規作成
  - `budget_service.py` を移動
  - `budget_calc_service.py` を移動
  - `budget_summary_service.py` を移動
  - `worklog_service.py` を移動
  - `expense_service.py` を移動
- `backend/app/routers/projects.py` importパスを更新
- `backend/app/routers/budget.py` importパスを更新
- `backend/tests/test_approval_service.py` importパスを更新
- `backend/tests/test_permission_service.py` importパスを更新
- `backend/tests/test_project_service.py` importパスを更新

### Added（feature/server-side-pagination）- 2026-04-23

#### サービス層の責務分離

- `backend/app/services/permission_service.py`（新規）
  - `check_project_access` - 案件アクセス権限チェック
  - `check_project_editable` - 案件編集権限チェック
  - `check_approval_permission` - 承認操作権限チェック
  - `check_budget_permission` - 予算・工数・経費操作権限チェック
  - `check_start_permission` - 着手操作権限チェック
  - `check_complete_permission` - 完了操作権限チェック
- `backend/app/services/approval_service.py`（新規）
  - 承認・却下処理を `project_service.py` から分離
- `backend/app/services/budget_calc_service.py`（新規）
  - 実績額再計算ロジックを分離
- `backend/app/services/budget_summary_service.py`（新規）
  - 予算サマリー集計処理を分離
- `backend/app/services/worklog_service.py`（新規）
  - 工数実績CRUDを分離
- `backend/app/services/expense_service.py`（新規）
  - 直接経費CRUDを分離
- `backend/app/services/query_service.py`
  - `check_project_approved` を追加
- `backend/tests/conftest.py`（新規）
  - テスト共通フィクスチャ（db / applicant / dept_manager / hq_manager / project）
- `backend/tests/test_permission_service.py`（新規）
  - 権限チェック15件のテストを追加
- `backend/tests/test_approval_service.py`（新規）
  - 承認・却下フロー6件のテストを追加
- `backend/tests/test_project_service.py`（新規）
  - ページネーション・案件操作11件のテストを追加

### Updated

- `backend/app/services/project_service.py`
  - 権限チェックを `permission_service` に委譲
  - 承認処理を `approval_service` に分離
  - 通知処理のimportを `notification_service` に統一
- `backend/app/services/budget_service.py`
  - 権限チェックを `permission_service` に委譲
  - 実績額計算を `budget_calc_service` に委譲
  - 工数・経費処理を各サービスに分離
- `backend/app/routers/projects.py`
  - `approval_service`・`budget_summary_service` のimportに更新
- `backend/app/routers/budget.py`
  - `worklog_service`・`expense_service` のimportに更新

#### バックエンド集計処理のSQL最適化

- `backend/app/services/budget_summary_service.py`
  - `total_projects`の集計をPython `len()` からSQL `COUNT` に変更
  - `total_budget`・`total_actual`の集計をPythonループからSQL `SUM` に変更
  - `avg_consumption_rate`を単純平均からSQL加重平均（`SUM(actual) / SUM(budget) * 100`）に変更
  - `CASE`式によるゼロ除算対策を追加
  - `ProjectBudget`とのJOINによりPython側のループ処理を全廃

- `backend/app/services/budget_calc_service.py`
  - 工数実績合計をPython `sum()` からSQL `SUM` に変更
  - 直接経費合計をPython `sum()` からSQL `SUM` に変更
  - `func.coalesce` によるNULL対策を追加

- `frontend/src/views/budget/BudgetListView.vue`
  - 消化率列で`consumption_rate`が`null`の場合に`--`を表示するよう修正

## [feature/server-side-pagination] - 2026-04-22

### Added

#### サーバーサイドページネーションの実装

- `backend/app/schemas/project.py`
  - `ProjectListResponse` を追加（total / page / limit / items）
  - `BudgetSummaryResponse` を追加（total_projects / total_budget / total_actual / avg_consumption_rate）

- `backend/app/services/project_service.py`
  - `_apply_project_filters` を追加（一覧・サマリー共通のフィルター定義関数）
  - `get_budget_summary` を追加（予算サマリー集計・フィルター連動）

- `backend/app/routers/projects.py`
  - `GET /api/projects` にページネーションパラメータ（page / limit）を追加
  - `GET /api/projects` にフィルターパラメータ（status / keyword）を追加
  - `GET /api/projects/budget-summary` 予算サマリーエンドポイントを追加（部門管理者・本部管理者のみ）

- `frontend/src/types/project.ts`
  - `ProjectListResponse` 型を追加
  - `BudgetSummaryResponse` 型を追加

- `frontend/src/api/projects.ts`
  - `getProjects` にページネーション・フィルターパラメータを追加
  - `getBudgetSummary` メソッドを追加

- `frontend/package.json`
  - `@vueuse/core` を追加（デバウンス処理用）

- `backend/app/scripts/seed.py`
  - ページネーション動作確認用にデータを増強（合計14件）
  - プロダクト開発部：7件（DRAFT / PENDING_DEPT / PENDING_HQ / APPROVED / IN_PROGRESS / COMPLETED / REJECTED）
  - カスタマーソリューション部：7件（同上）

### Updated

- `backend/app/services/project_service.py`
  - `get_projects` をページネーション・フィルター対応に変更（戻り値を `ProjectListResponse` に変更）
  - `get_projects` に `order_by(created_at.desc())` を追加（ページ間の順序保証）
  - `get_projects` にページ・件数の防御処理を追加（page: min 1、limit: 10〜100）
  - `_apply_project_filters` を使用するよう `get_projects` を修正

- `frontend/src/views/projects/ProjectListView.vue`
  - ページネーションUI（`el-pagination`）を追加
  - ステータスフィルターをサーバーサイドに移行
  - キーワード検索をサーバーサイドに移行（`watchDebounced` で300msデバウンス）
  - フィルター変更時にページを1にリセットする処理を追加

- `frontend/src/views/DashboardView.vue`
  - `getProjects` のレスポンス取得を `response.data.items` に変更
  - `projectTotal` を追加し管理案件数の表示を `ProjectListResponse.total` から取得するよう変更
  - `getProjects(1, 100)` で最大100件取得するよう変更

- `frontend/src/views/budget/BudgetListView.vue`
  - ページネーションUI（`el-pagination`）を追加
  - キーワード検索をサーバーサイドに移行（`watchDebounced` で300msデバウンス）
  - ステータスフィルターをサーバーサイドに移行
  - サマリーカードを `getBudgetSummary` APIから取得したデータに変更（フィルターと連動）
  - `onMounted` の二重API呼び出しを修正

## [feature/screen-verification] - 2026-04-22

### Added

- 部門管理者向け予算管理画面の閲覧機能を追加
- AppHeader.vueに部門管理者の予算管理メニューを追加
- BudgetListView.vueを新規作成（本部管理者・部門管理者向け予算一覧）
- 直接経費の編集機能を追加（ExpenseFormView.vue編集モード対応）
- 申請者向けダッシュボードに完了案件カードを追加
- 管理者向けダッシュボードに完了案件カードを追加

### Updated

- DashboardView.vue
  - unreadCountをWebSocketと連携（notificationService.tsに統一）
  - 申請者の申請中案件カウントをDRAFT・PENDING_DEPT・PENDING_HQ・REJECTEDに限定
  - ダッシュボードテーブルの申請者表示を申請中ステータスのみに絞り込み
  - 主要導線のボタンラベルを申請者向けに「申請中案件一覧へ」に変更
- ProjectListView.vue
  - 申請者のデフォルト表示をDRAFT・PENDING_DEPT・PENDING_HQ・REJECTEDのみに変更
  - 複数ステータスのフィルター対応（カンマ区切り）
  - pageTitle・pageSubtitleの条件順序を修正
- ProjectDetailView.vue
  - パンくずリストを申請者向けに「申請中案件一覧」に変更
  - 却下理由を画面上部にel-alertで表示
  - タスク一覧・予算サマリ・進捗率をAPPROVED以降のみ表示
- AppHeader.vue
  - 申請者メニューの「案件一覧」を「申請中案件」に変更
  - 申請者メニューに「進行中案件」を追加
  - 部門管理者メニューに「予算管理」を追加
  - notificationServiceのimportパスを修正
- BudgetView.vue
  - パンくずリストを申請者向けに変更
  - 直接経費一覧に編集・削除ボタンを追加
  - 操作ボタンを各テーブルヘッダーに移動
  - 金額のカンマ区切り表示対応
  - 予算未登録時の操作ボタン非表示対応
- router/index.ts
  - /budgetルートを追加（HQ_MANAGER・DEPT_MANAGERのみ）
  - 直接経費編集ルートを追加
- BudgetListView.vue
  - 部門管理者対応（自部門案件のみ表示・サブタイトル動的切り替え）
  - 部門名表示対応（departmentsAPIから取得）
- project_service.py
  - 部門管理者のget_projectsを自部門のみに戻す
  - \_check_project_accessを部門管理者は自部門のみアクセス可能に修正

## [feature/ux-improvements] - 2026-04-22

### Added

#### ロール別テーブルコンポーネントの分割

- `frontend/src/components/projects/ApplicantProjectTable.vue`（新規）
  - 申請者向けテーブル（承認ステップ可視化付き）
- `frontend/src/components/projects/DeptManagerProjectTable.vue`（新規）
  - 部門管理者向けテーブル
- `frontend/src/components/projects/HqManagerProjectTable.vue`（新規）
  - 本部管理者向けテーブル（部門名表示付き）
- `frontend/src/composables/useProjectTable.ts`（新規）
  - 共通ロジック（formatDate・getConsumptionStatus・getApprovalStepType等）を分離
- `frontend/src/composables/useProjectActions.ts`（新規）
  - 案件詳細画面のアクション定義・権限制御・ハンドラーを分離
- `frontend/src/api/departments.ts`（新規）
  - 部門一覧APIクライアントを追加
- `backend/app/routers/departments.py`（新規）
  - `GET /api/departments` 部門一覧エンドポイントを追加

#### プロジェクトステータスの分離・拡張

- `backend/app/models/project.py`
  - `IN_PROGRESS`・`COMPLETED`・`DRAFT` を追加
- `backend/app/routers/projects.py`
  - `PATCH /projects/{id}/start` 着手エンドポイントを追加
  - `PATCH /projects/{id}/complete` 完了エンドポイントを追加
- `backend/alembic/versions/002_add_project_status.py`（新規）
  - ProjectStatusのEnum拡張マイグレーションを追加
- `frontend/src/api/client.ts`
  - `patch` メソッドを追加

### Updated

#### バリデーション強化

- `frontend/src/views/projects/ProjectNewView.vue`
  - 完了予定日のタイムゾーンバグ修正
  - 開始日変更時に完了日バリデーションを自動再実行
  - 開始日に申請日より前の日付を選択不可に追加

#### 案件一覧・ダッシュボードの改善

- `frontend/src/views/projects/ProjectListView.vue`
  - ロール別コンポーネントに置き換え
  - クエリパラメータによる初期フィルター対応
  - filterStatusに連動したpageTitle・pageSubtitleの動的切り替え
  - フィルタークリアボタンの追加
- `frontend/src/views/DashboardView.vue`
  - ロール別コンポーネントに置き換え
  - 進行中案件の件数判定を `IN_PROGRESS` に修正
  - 承認待ちカードのクリック先をロール別に分岐
  - 進行中案件カードのクリック先を `IN_PROGRESS` に修正
- `frontend/src/views/projects/ProjectDetailView.vue`
  - 着手・完了ボタンを追加
  - アクション定義をuseProjectActionsに分離
  - 予算消化率の除算ゼロバグ修正

#### ステータス対応

- `frontend/src/types/project.ts` - 新ステータスを追加
- `frontend/src/constants/project.ts` - 新ステータスのラベル・タグ種別を追加
- `frontend/src/views/budget/BudgetView.vue` - `IN_PROGRESS` 対応
- `frontend/src/views/tasks/TaskFormView.vue` - `IN_PROGRESS` 対応
- `backend/app/services/project_service.py` - start_project・complete_project追加・get_projectsをロール統合
- `backend/app/scripts/seed.py` - 新ステータスに対応
- `backend/app/main.py` - 部門ルーターを登録

## [feature/websocket-realtime-notification] - 2026-04-21

### Added

#### WebSocketによるリアルタイム通知

- `backend/app/websocket_manager.py`（新規）
  - ユーザーIDごとの複数WebSocket接続を管理する `ConnectionManager` クラスを実装
  - 切断済み接続の自動除去・JSON送信を実装

- `frontend/src/services/notificationService.ts`（更新）
  - WebSocket接続・自動再接続（最大10回・5秒間隔）を実装
  - `unreadCount` / `latestNotification` をreactive状態として公開
  - `startNotificationWs` / `stopNotificationWs` を公開

### Updated

- `backend/app/routers/notifications.py`
  - `GET /api/notifications/ws` WebSocketエンドポイントを追加
  - クエリパラメータ経由のJWT検証を実装（認証失敗時はcode 4001で切断）

- `backend/app/services/project_service.py`
  - 通知生成の3箇所（申請時・部門承認時・本部承認/却下時）に `_push_notification` を追加
  - WebSocket接続中のユーザーへリアルタイムプッシュ送信

- `backend/app/main.py`
  - CORSの `allow_origins` に本番URL `http://158.101.148.143` を追加

- `frontend/src/components/AppHeader.vue`
  - ログイン後にWebSocket接続を開始・ログアウト時に切断
  - 通知受信時にバッジをリアルタイム更新
  - 通知受信時にトースト（画面右下）を表示

- `frontend/nginx.conf`
  - `/api/notifications/ws` のWebSocketプロキシ設定を追加（`Upgrade` / `Connection` ヘッダー対応）

## [feature/validation-and-worklog-delete] - 2026-04-21

### Added

#### 工数実績削除機能

- `frontend/src/views/budget/BudgetView.vue`
  - 工数実績一覧に削除ボタンを追加
  - 削除前に確認ダイアログを表示
  - 削除後に予算サマリーを再取得して表示を更新

- `frontend/src/api/budget.ts`
  - `deleteWorklog` メソッドを追加

- `backend/app/routers/budget.py`
  - `DELETE /api/projects/{project_id}/worklogs/{worklog_id}` エンドポイントを追加

- `backend/app/services/budget_service.py`
  - `delete_worklog` 関数を追加

### Updated

#### バリデーション強化

- `frontend/src/views/projects/ProjectNewView.vue`
  - 完了予定日のカレンダーで開始日より前の日付を選択不可に修正
  - `disabledEndDate` のタイムゾーンバグを修正（`T00:00:00` 付与によりローカル日付として解釈）
  - 開始日変更時に完了日バリデーションを `watch` で自動再実行

- `frontend/src/views/approval/ApprovalView.vue`
  - 承認・却下API成功後に `actionDone` フラグをセットしボタンを非活性化
  - ページ遷移前の二重送信・誤クリックを防止

## [feature/deploy-oracle-cloud] - 2026-04-20

### Added

#### デプロイ

- Oracle Cloud（Ubuntu 24.04）へのデプロイ完了
  - URL: http://158.101.148.143
  - フロントエンド・バックエンド・DBをDocker Composeで統合デプロイ
- `docker-compose.prod.yml` - 本番環境用Docker Compose設定を更新

## [feature/documentation] - 2026-04-20

### Added

#### ドキュメント整備

- `doc/Information.md` - デプロイURL・テストアカウント一覧・起動方法
- `doc/manual.html` - アプリケーション利用マニュアル
  - アクセス情報・テストアカウント
  - ロール別操作手順（申請者・部門管理者・本部管理者）
  - データ入力制限・注意事項

## [feature/improvements] - 2026-04-20

### Added

#### axiosからfetchへの差し替え

- `frontend/src/api/client.ts` - axiosからfetch APIに差し替え
  - 認証トークン自動付与・401エラー時ログアウト処理を自前実装
  - ステータスコード別エラーハンドリングを実装

#### 機能改善・バリデーション強化

- `frontend/src/views/tasks/TaskFormView.vue`
  - ステータスと進捗率の連動を実装
  - 完了選択時に進捗率を100%に自動設定
  - 進捗率100%入力時にステータスを完了に自動設定
  - 完了状態から進捗率を下げた場合は進行中に自動変更
  - タスク開始日・期限に案件期間外の日付を選択不可にするバリデーションを追加

- `frontend/src/views/budget/WorklogFormView.vue`
  - 対象月に未来の月・案件開始日より前の月を選択不可にするバリデーションを追加
  - 工数上限値チェックを追加（20人月以下）
  - 編集モード対応（worklogId有無で新規・編集を切り替え）
  - 編集時は対象月を変更不可に設定
  - 0人月への更新を許容（誤登録時の対処）

- `frontend/src/views/budget/BudgetView.vue`
  - 工数実績一覧に編集ボタンを追加

- `frontend/src/views/budget/ExpenseFormView.vue`
  - 発生日に未来の日付・案件開始日より前の日付を登録不可にするバリデーションを追加
  - 金額上限値チェックを追加（999,999,999円以下）

- `frontend/src/views/projects/ProjectNewView.vue`
  - 開始日に過去の日付を選択不可にするバリデーションを追加
  - 概算予算の上限値チェックを追加（999,999,999円以下）

- `frontend/src/views/approval/ApprovalView.vue`
  - 却下理由の文字数制限を追加（500字以内）

- `frontend/src/router/index.ts`
  - 工数実績編集ルートを追加（/projects/:projectId/budget/worklogs/:worklogId/edit）

### Updated

#### バックエンド

- `backend/app/services/budget_service.py`
  - 承認前案件への予算APIアクセス時のレスポンスを400から404に変更

## [feature/dashboard-implementation] - 2026-04-20

### Added

#### ダッシュボード実装

- `frontend/src/views/DashboardView.vue` - モックデータをAPIに差し替え・ロール別案件状況テーブル追加
  - 本部管理者向け：全部門の案件進捗・予算消化状況の横断確認
  - 部門管理者向け：自部門の案件進捗・予算消化状況の確認
  - 申請者向け：自身の案件承認ステップの可視化・進捗確認
  - 予算消化率の閾値アラート表示（80%以上で警告・100%以上で危険）

### Updated

#### バックエンド

- `backend/app/schemas/project.py` - ProjectResponseに予算情報（actual_amount / consumption_rate）を追加
- `backend/app/services/project_service.py` - \_to_response関数に予算消化率の自動算出を追加

#### フロントエンド

- `frontend/src/types/project.py` - Project型にactual_amount / consumption_rateを追加

## [feature/frontend-api-integration] - 2026-04-17

### Added

#### フロントエンド：APIクライアント実装

- `frontend/src/api/client.ts` - axiosベースAPIクライアント（認証トークン自動付与・401エラー時ログアウト）
- `frontend/src/api/auth.ts` - 認証API（ログイン・トークンリフレッシュ）
- `frontend/src/api/users.ts` - ユーザーAPI（ログインユーザー情報取得）
- `frontend/src/api/projects.ts` - 案件API（一覧・詳細・作成・更新・承認）
- `frontend/src/api/tasks.ts` - タスクAPI（一覧・作成・更新・削除）
- `frontend/src/api/budget.ts` - 予算・工数・経費API
- `frontend/src/api/notifications.ts` - 通知API（一覧・既読・全既読）

### Updated

#### 型定義の整理

- `frontend/src/types/user.ts` - Role型を追加・バックエンドレスポンスに合わせて更新
- `frontend/src/types/project.ts` - バックエンドレスポンスに合わせて更新・progress追加
- `frontend/src/types/task.ts` - TaskStatusをバックエンドに合わせて更新（NOT_STARTED→TODO / COMPLETED→DONE）
- `frontend/src/types/budget.ts` - バックエンドレスポンスに合わせて更新（人月管理に変更）
- `frontend/src/types/notification.ts` - バックエンドレスポンスに合わせて更新
- `frontend/src/constants/task.ts` - TaskStatusラベルをバックエンドに合わせて更新

#### 認証ストア

- `frontend/src/stores/auth.ts` - ダミーログインをAPI接続に差し替え・refreshToken管理追加

#### 画面API接続

- `frontend/src/views/projects/ProjectListView.vue` - 案件一覧APIに接続
- `frontend/src/views/projects/ProjectDetailView.vue` - 案件詳細・タスク・予算APIに接続（モックデータ全面差し替え）
- `frontend/src/views/projects/ProjectNewView.vue` - 案件申請APIに接続
- `frontend/src/views/approval/ApprovalView.vue` - 承認・却下APIに接続
- `frontend/src/views/tasks/TaskFormView.vue` - タスク登録・更新・削除APIに接続
- `frontend/src/views/budget/BudgetView.vue` - 予算・工数・経費APIに接続・サマリー自動計算実装
- `frontend/src/views/budget/WorklogFormView.vue` - 工数実績登録APIに接続
- `frontend/src/views/budget/ExpenseFormView.vue` - 直接経費登録APIに接続
- `frontend/src/views/NotificationView.vue` - 通知一覧・既読APIに接続

#### バックエンド追加対応

- `backend/app/schemas/project.py` - ProjectResponseにprogressフィールドを追加
- `backend/app/services/project_service.py` - タスク進捗率平均を自動算出する\_calc_progress・\_to_response関数を追加

## [feature/backend-api-implementation] - 2026-04-17

### Added

#### バックエンド：モデル実装

- `backend/app/models/__init__.py` - モデルパッケージ定義・Alembic認識用インポート
- `backend/app/models/department.py` - Departmentモデル
- `backend/app/models/user.py` - Userモデル（UserRoleEnum定義含む）
- `backend/app/models/project.py` - Projectモデル（ProjectStatusEnum定義含む）
- `backend/app/models/task.py` - Taskモデル（TaskStatusEnum定義含む）
- `backend/app/models/project_budget.py` - ProjectBudgetモデル
- `backend/app/models/worklog.py` - Worklogモデル（月次工数管理・UniqueConstraint設定）
- `backend/app/models/expense.py` - Expenseモデル（ExpenseTypeEnum定義含む）
- `backend/app/models/notification.py` - Notificationモデル
- `backend/alembic/versions/001_create_initial_tables.py` - 初期テーブル作成マイグレーション

#### Docker環境修正

- `docker-compose.dev.yml` - backendおよびfrontendサービスに`app-network`・`depends_on`を追加
- `backend/alembic/script.py.mako` - Alembicマイグレーションテンプレートファイルを追加

### Updated

- `backend/alembic/env.py` - `from app.models import Base` に変更し全モデルをAlembicに認識させる

#### バックエンド：スキーマ実装

- `backend/app/schemas/__init__.py` - スキーマパッケージ定義（空ファイル）
- `backend/app/schemas/auth.py` - 認証スキーマ（LoginRequest / TokenResponse / RefreshRequest）
- `backend/app/schemas/user.py` - ユーザースキーマ（UserCreate / UserResponse）
- `backend/app/schemas/project.py` - 案件スキーマ（ProjectCreate / ProjectUpdate / ApprovalRequest / ProjectResponse）
- `backend/app/schemas/task.py` - タスクスキーマ（TaskCreate / TaskUpdate / TaskResponse）
- `backend/app/schemas/budget.py` - 予算・工数・経費スキーマ
- `backend/app/schemas/notification.py` - 通知スキーマ（NotificationResponse / NotificationUpdate）

#### バックエンド：セキュリティ実

- `backend/app/utils/__init__.py` - utilsパッケージ定義（空ファイル）
- `backend/app/utils/security.py` - パスワードハッシュ化（Argon2）・JWT生成・デコード

#### バックエンド：依存性注入実装

- `backend/app/dependencies/__init__.py` - dependenciesパッケージ定義
- `backend/app/dependencies/auth.py` - `get_current_user`・`require_roles` 実装

#### バックエンド：サービス層実装

- `backend/app/services/__init__.py` - servicesパッケージ定義（空ファイル）
- `backend/app/services/auth_service.py` - ログイン・トークンリフレッシュ
- `backend/app/services/user_service.py` - ユーザー作成・一覧・詳細取得
- `backend/app/services/project_service.py` - 案件申請・一覧・詳細・更新・承認却下・通知生成
- `backend/app/services/task_service.py` - タスク作成・一覧・更新・削除
- `backend/app/services/budget_service.py` - 予算・工数実績・直接経費のCRUD・実績額自動計算
- `backend/app/services/notification_service.py` - 通知一覧・既読・全既読

#### バックエンド：ルーター実装

- `backend/app/routers/__init__.py` - routersパッケージ定義（空ファイル）
- `backend/app/routers/auth.py` - 認証ルーター
- `backend/app/routers/users.py` - ユーザールーター
- `backend/app/routers/projects.py` - 案件ルーター
- `backend/app/routers/tasks.py` - タスクルーター
- `backend/app/routers/budget.py` - 予算管理ルーター
- `backend/app/routers/notifications.py` - 通知ルーター

#### バックエンド：アプリケーション設定

- `backend/app/main.py` - FastAPIアプリケーション設定・CORSミドルウェア・全ルーター登録

#### シードデータ

- `backend/app/scripts/seed.py` - 初期データ投入スクリプト
  - 部門: プロダクト開発部 / カスタマーソリューション部 / 開発本部
  - ユーザー: 5名（申請者×2 / 部門管理者×2 / 本部管理者×1）
  - 案件: 3件（承認済み×2 / 部門承認待ち×1）
  - タスク・工数実績・直接経費の初期データを含む

### Tested

#### バックエンドAPI動作確認

- ログイン・トークン発行（POST /api/auth/login）
- 案件一覧取得・ロール別アクセス制御（GET /api/projects）
  - 申請者：自身の案件のみ
  - 部門管理者：自部門の案件のみ
  - 本部管理者：全部門の案件
- 承認フロー（POST /api/projects/{id}/approve）
  - PENDING_DEPT → PENDING_HQ（部門管理者による一次承認）
  - PENDING_HQ → APPROVED（本部管理者による最終承認）
- タスク一覧取得（GET /api/projects/{id}/tasks）
- 予算情報取得（GET /api/projects/{id}/budget）
- 工数実績一覧取得（GET /api/projects/{id}/worklogs）
- 通知一覧取得（GET /api/notifications）

## [feature/mock-ui-deploy] - 2026-04-16

### Added

- `docs/memo/TestInfo.html` - テスト案内ページ（アクセスURL・テストアカウント・機能概要）

### Updated

- `frontend/src/composables/` - 別プロジェクトの不要ファイルを削除（useRadarData.ts / useRankingData.ts / useTrendData.ts）

### Deployed

- Vercel（Production）へフロントエンドをデプロイ
  - URL: https://frontend-alpha-blue-45.vercel.app
  - モックUI段階のため固定サンプルデータで動作
  - バックエンド未接続

## [feature/docker-setup] - 2026-04-16

### Added

#### Docker環境構築

- `docker-compose.yml` - 共通サービス定義（db / backend / frontend）
- `docker-compose.dev.yml` - 開発環境設定（ホットリロード・ポート公開）
- `docker-compose.prod.yml` - 本番環境設定
- `mysql/Dockerfile` - MySQL 8.0 Dockerfile
- `mysql/conf.d/my.cnf` - MySQL設定（utf8mb4_unicode_ci）
- `backend/Dockerfile` - FastAPI Dockerfile（python:3.12-slim）
- `backend/requirements.txt` - 依存パッケージ定義
- `backend/alembic.ini` - Alembic設定
- `backend/alembic/env.py` - マイグレーション環境設定
- `backend/app/db.py` - DB接続設定（SQLAlchemy）
- `backend/app/models/base.py` - SQLAlchemyベースクラス
- `backend/app/scripts/wait_for_db.py` - DB起動待機スクリプト
- `frontend/Dockerfile.dev` - Vue/Vite開発用Dockerfile
- `frontend/Dockerfile.prod` - Vue/Vite本番用Dockerfile（マルチステージビルド）
- `frontend/nginx.conf` - nginx設定（Vue Router対応・APIプロキシ）
- `frontend/vite.config.ts` - Vite設定（ホットリロード・APIプロキシ）
- `.gitignore` - 環境変数・node_modules等を除外

#### 画面設計ファイルの追加

- `docs/design/screens/screens/project_apply.md`
  - S-APP-02：案件申請画面を新規作成
- `docs/design/screens/screens/project_detail.md`
  - S-APP-03：案件詳細画面を新規作成
- `docs/design/screens/screen-list.md`
  - ファイル構成テーブルを追加
- `docs/design/screens/README.md`
  - 構成ツリーにS-APP-02・S-APP-03を追加

#### フロントエンド環境整備

- Element Plus・@element-plus/icons-vueを導入
- `src/types/common.ts` - API共通レスポンス型
- `src/types/user.ts` - ユーザー型定義
- `src/types/project.ts` - 案件・承認関連型定義
- `src/types/task.ts` - タスク関連型定義
- `src/types/budget.ts` - 予算・工数・経費関連型定義
- `src/types/notification.ts` - 通知関連型定義
- `src/constants/project.ts` - 案件ステータスラベル・タグ種別定数
- `src/constants/task.ts` - タスクステータスラベル・タグ種別定数
- `src/constants/budget.ts` - 経費種別ラベル定数

#### モックUI実装（全11画面）

- `src/views/auth/LoginView.vue` - ログイン画面
- `src/views/DashboardView.vue` - ダッシュボード
- `src/views/projects/ProjectListView.vue` - 案件一覧画面
- `src/views/projects/ProjectNewView.vue` - 案件申請画面
- `src/views/projects/ProjectDetailView.vue` - 案件詳細画面
- `src/views/approval/ApprovalView.vue` - 承認・却下画面
- `src/views/tasks/TaskFormView.vue` - タスク登録・更新画面
- `src/views/budget/BudgetView.vue` - 予算管理画面
- `src/views/budget/WorklogFormView.vue` - 工数実績入力画面
- `src/views/budget/ExpenseFormView.vue` - 直接経費入力画面
- `src/views/NotificationView.vue` - 通知一覧画面
- `src/views/NotFoundView.vue` - 404画面

### Updated

- `src/main.ts` - Element Plus・日本語ロケール設定・Bootstrapを削除
- `src/App.vue` - ヘッダー制御を追加
- `src/components/AppHeader.vue` - Element Plus対応・ロール別メニュー実装
- `src/router/index.ts` - 画面設計に合わせて全面刷新・ナビゲーションガード実装
- `src/stores/auth.ts` - ロール定義更新・ダミーログイン実装

## [feature/design-docs, feature/er-diagram] - 2026-04-14

### Updated

#### 設計ドキュメント全面見直し（仮想業務要件定義書をもとに更新）

- `docs/memo/domain_policy.md`
  - 工数管理を日次→月次に変更
  - ガントチャート廃止・タスクリスト＋進捗率バーに変更
  - 業務ルール（BR-1〜BR-9）追加
  - 予算・コスト定義を更新（人月単価・直接経費の概念追加）
  - 承認フローにおける各ロールの役割・観点を追加

- `docs/requirements/requirements_phase1.md`
  - ロール定義・必須機能を更新
  - タスクステータスに「レビュー中」追加
  - 業務ルール（BR-1〜BR-9）追加
  - 予算サマリ（自動算出項目）を追加

- `docs/design/role_matrix.md`
  - 開発者ロール（DEVELOPER）を廃止
  - 申請者への権限統合

- `docs/design/functions.md`
  - タスク管理・工数管理・直接経費管理機能を見直し
  - スケジュール管理機能を削除

- `docs/usecase/usecase_applicant.md`
  - UC-A04〜07を全面見直し（タスク登録・工数実績・直接経費・予実確認）

- `docs/usecase/usecase_dept_manager.md`
  - UC-D03（予算消費状況確認）を追加

- `docs/usecase/usecase_hq_manager.md`
  - UC-H01〜03を全面見直し

- `docs/design/api_design.md`
  - worklogs APIを日次→月次に変更
  - expenses APIを新規追加
  - スケジュールAPIを削除
  - タスクステータスにIN_REVIEWを追加
  - 予算サマリレスポンス定義を追加

- `docs/design/db/er_design.md`
  - tasksの階層構造（parent_task_id）を削除
  - worklogsのFKをtask_id→project_idに変更
  - expensesテーブルを追加

- `docs/design/db/tables/tasks.md`
  - 階層構造カラム削除（parent_task_id・level）
  - 工数関連カラム削除（planned_hours・actual_hours）
  - statusにIN_REVIEWを追加

- `docs/design/db/tables/worklogs.md`
  - task_id・user_idを削除（案件単位管理に変更）
  - work_date→work_monthに変更（日次→月次）
  - ユニーク制約を(project_id, work_month)に変更

- `docs/design/db/tables/project_budgets.md`
  - unit_price（人月単価）カラムを追加
  - 人月単価をproject_budgetsで一元管理する方針に変更

- `docs/design/db/design_policy.md`
  - 設計方針を最新の内容に更新

- `docs/design/db/status_design.md`
  - tasksステータスにIN_REVIEWを追加

- `docs/memo/phase2_ideas.md`
  - KPI表示をダッシュボード候補として追記
  - 月次進捗レポート自動生成・出力を追加

#### ER設計見直し

- `docs/design/db/tables/departments.md`
  - `parent_department_id`・`deleted_at` を削除しシンプル構成へ変更
  - 部門テーブルをPoCスコープに合わせて階層構造・論理削除を排除

- `docs/design/db/tables/users.md`
  - roleのENUMから `DEVELOPER` を削除
  - 開発者ロールを廃止し、申請者・部門管理者・本部管理者の3区分に統一

- `docs/design/db/er_design.md`
  - `tasks → worklogs` のリレーションを削除
  - 工数管理をタスク単位から案件単位へ変更した設計に整合

- `docs/design/db/tables/expenses.md`
  - `expense_type` を `VARCHAR(100)` から `ENUM` に変更
  - 表記ゆれ防止のためシステム定義値化
  - 経費種別定義を追加（`OUTSOURCING` / `LICENSE` / `EQUIPMENT` / `OTHER`）

### Added

- `docs/background/virtual_requirements/01_業務要件定義書.md`
- `docs/background/virtual_requirements/カスタマーソリューション部_案件進捗_2026Q1-Q2.xlsx`
- `docs/background/virtual_requirements/プロダクト開発部_進捗管理_2026年4月.xlsx`
- `docs/background/virtual_requirements/開発本部_予算管理_2026年度.xlsx`
- `docs/background/virtual_requirements/本部向け_月次進捗報告_プロダクト開発部_2026年4月.xlsx`
- `docs/design/screens/README.md`
- `docs/design/screens/navigation.md`
- `docs/design/screens/screen-list.md`
- `docs/design/screens/screens/auth.md`
- `docs/design/screens/screens/dashboard.md`
- `docs/design/screens/screens/project.md`
- `docs/design/screens/screens/approval.md`
- `docs/design/screens/screens/task.md`
- `docs/design/screens/screens/budget.md`
- `docs/design/screens/screens/notification.md`
- `docs/design/db/tables/expenses.md`

### Deleted

- `docs/usecase/usecase_developer.md`
- `docs/design/screens.md`（screens/ディレクトリに分割）

## [feature/design-docs] - 2026-04-13

### Added

#### ドキュメント構成

- `docs/requirements/requirements_phase1.md` - 課題１要件まとめ
- `docs/memo/domain_policy.md` - ドメイン・方針定義
- `docs/memo/phase2_ideas.md` - 課題２機能アイデア・メモ
- `docs/background/current_operations.md` - 現在の運用とPoC企画時の課題点

#### ユースケース

- `docs/usecase/usecase_applicant.md` - 申請者ユースケース
- `docs/usecase/usecase_dept_manager.md` - 部門管理者ユースケース
- `docs/usecase/usecase_hq_manager.md` - 本部管理者ユースケース
- `docs/usecase/usecase_developer.md` - 開発者ユースケース

#### 設計ドキュメント

- `docs/design/role_matrix.md` - ロール権限マトリクス
- `docs/design/functions.md` - 機能一覧
- `docs/design/screens.md` - 画面設計
- `docs/design/api_design.md` - API設計
- `docs/design/er_design.md` - ER図

#### DB設計（テーブル定義）

- `docs/design/db/db_design.md` - DB設計インデックス
- `docs/design/db/design_policy.md` - DB設計方針
- `docs/design/db/er_design.md` - ER図
- `docs/design/db/status_design.md` - ステータス設計
- `docs/design/db/tables/departments.md` - departmentsテーブル定義
- `docs/design/db/tables/users.md` - usersテーブル定義
- `docs/design/db/tables/projects.md` - projectsテーブル定義
- `docs/design/db/tables/tasks.md` - tasksテーブル定義
- `docs/design/db/tables/worklogs.md` - worklogsテーブル定義
- `docs/design/db/tables/project_budgets.md` - project_budgetsテーブル定義
- `docs/design/db/tables/notifications.md` - notificationsテーブル定義

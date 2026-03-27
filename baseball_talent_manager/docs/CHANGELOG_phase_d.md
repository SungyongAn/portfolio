
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
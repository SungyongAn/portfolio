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
## 2026-04-08

## [TypeScript移行] フロントエンドのTypeScript化完了

### Changed

**フロントエンド**
- `frontend/src/services/` 配下を `.js` → `.ts` に移行
  - `api.ts` / `authService.ts` / `measurementService.ts` / `userService.ts` / `notificationService.ts`
- `frontend/src/composables/` 配下を `.js` → `.ts` に移行
  - `usePagination.ts` / `useTrendData.ts` / `useRadarData.ts` / `useRankingData.ts`
- `frontend/src/constants/measurementFields.js` → `measurementFields.ts` に移行
- `frontend/src/stores/` 配下を `.js` → `.ts` に移行
  - `auth.ts` / `notification.ts`
- `frontend/src/router/index.js` → `index.ts` に移行
- `frontend/src/views/` 配下の全`.vue`ファイルを `<script setup lang="ts">` に移行
- `frontend/src/components/` 配下の主要`.vue`ファイルを `<script setup lang="ts">` に移行
  - 未対応：`MeasurementResultGraph.vue` / `NotFoundView.vue`

### Added

**フロントエンド**
- `frontend/src/env.d.ts` を新規作成
  - `.vue` ファイルのモジュール型宣言を追加
- `frontend/tsconfig.json` を新規作成
- `frontend/vite.config.js` → `vite.config.ts` にリネーム・修正
- ESLintにTypeScriptパーサーを追加
  - `@typescript-eslint/parser` / `vue-eslint-parser`

### Technical Notes
- 型定義は各サービスファイルにまとめてエクスポート（`Measurement`・`User`・`MeasurementStatus`など）
- 共通型は各コンポーネントからもエクスポートして再利用（`SortKey`・`Grade`・`ActionType`など）
- `reactive<T>()`の型推論競合は`reactive({}) as T`の形で回避
- EChartsの`valueFormatter`は`(value: unknown) => string`で型安全化
- `lowerIsBetter`を全`MEASUREMENT_FIELDS`に統一してTS型エラーを解消

## 2026-03-30

## [課題2] 退部・引退日付記録・測定日年月変更・測定進捗確認・ヘッダー更新

### Added

**バックエンド**
- `backend/alembic/versions/005_add_status_changed_at.py` を新規作成
  - `users` テーブルに `status_changed_at` カラムを追加（DATETIME・NULL許容）
  - 既存データへの初期値：NULL（過去の処理日は不明なため）

**フロントエンド**
- `frontend/src/components/MemberHistory.vue` を新規作成
  - 退部・引退済み部員の履歴画面
  - 部員名・学年・ステータス・退部/引退日付を一覧表示
  - ソート・絞り込み・ページネーション機能を追加
- `frontend/src/views/shared/MeasurementProgressView.vue` を新規作成
  - 対象月の測定登録状況を部員ごとに一覧表示
  - 年月ピッカーで対象月を選択（初期値は当月）
  - 在籍中の全部員と測定記録を突き合わせて登録状況・ステータスを表示
  - ページネーション機能を追加

### Changed

**バックエンド**
- `backend/app/models/user.py`
  - `status_changed_at` カラムを追加
- `backend/app/schemas/user.py`
  - `UserListItem` に `status_changed_at: datetime | None` を追加
- `backend/app/services/user_service.py`
  - `get_user_list()` のクエリに `User.status_changed_at` を追加
  - `update_user_status()` で退部・引退処理時に `status_changed_at` を記録

**フロントエンド**
- `frontend/src/components/MemberManagement.vue`
  - 「退部・引退履歴」カードを追加
- `frontend/src/views/manager/MeasurementResultSubmit.vue`
  - 計測日入力を `type="date"` から `type="month"` に変更
  - 当月を初期値として自動設定
  - 送信時に `measurement_date` を月初（YYYY-MM-01）に変換
- `frontend/src/components/measurement/MeasurementTable.vue`
  - 計測日表示を年月のみ（YYYY-MM）に変更（`.slice(0, 7)`）
- `frontend/src/views/manager/MeasurementStatusList.vue`
  - 計測日表示を年月のみ（YYYY-MM）に変更
- `frontend/src/views/manager/DashboardView.vue`
  - 「測定登録状況」カードを追加
- `frontend/src/views/shared/DashboardView.vue`
  - 「測定登録状況」カードを追加（コーチ・監督のみ表示）
- `frontend/src/components/AppHeader.vue`
  - 各ロールのメニューに不足していた項目を追加
    - manager: 測定登録状況
    - member: 可視化ダッシュボード
    - coach: 測定登録状況・可視化ダッシュボード
    - director: 測定登録状況・可視化ダッシュボード
- `frontend/src/router/index.js`
  - コーチ・監督ルートに `members/member-history` を追加
  - マネージャー・コーチ・監督ルートに `progress` を追加

### Technical Notes
- 測定日はDBの `date` 型（YYYY-MM-01）を維持しフロントエンドのUIのみ年月に変更（案A）
- `MeasurementProgressView.vue` はAPIの追加なしで既存の `getUsers()` と `getAllMeasurements()` を流用
- `status_changed_at` は退部・引退処理時に `datetime.now(timezone.utc)` で記録

## 2026-03-29

## [課題2] ダッシュボード通知機能・WebSocketリアルタイム通知・承認済みレコード確認済み管理

### Added

**バックエンド**
- `backend/alembic/versions/004_add_manager_confirmed.py` を新規作成
  - `measurements` テーブルに `manager_confirmed` カラムを追加（BOOLEAN・NOT NULL・DEFAULT FALSE）
  - 既存の `approved` レコードは `TRUE`、それ以外は `FALSE` で初期化
- `backend/app/routers/notifications.py` を新規作成
  - `ConnectionManager` クラス（`user_id → WebSocket` のマッピングで接続管理）
  - `GET /ws/notifications` WebSocketエンドポイント（クエリパラメータでJWT認証）
- `backend/app/services/notification_service.py` を新規作成
  - `notify_user(user_id, message)` — 特定ユーザーへの通知
  - `notify_role(role, message, db)` — ロール全体への通知

**フロントエンド**
- `frontend/src/services/notificationService.js` を新規作成
  - WebSocket接続・切断・自動再接続ロジック
- `frontend/src/stores/notification.js` を新規作成
  - 通知リスト管理（Pinia）
  - `isConnected` フラグによる重複接続防止

### Changed

**バックエンド**
- `backend/app/models/measurement.py`
  - `manager_confirmed` カラムを追加
- `backend/app/schemas/measurement.py`
  - `MeasurementItem` に `manager_confirmed: bool` を追加
- `backend/app/services/measurement_service.py`
  - `submit_measurement()`・`member_approve()`・`coach_approve()` を `async def` に変更
  - 各関数に通知呼び出しを追加
  - `confirm_measurement()` を新規追加
  - `get_measurements()` の `MeasurementItem` 生成に `manager_confirmed` を追加
- `backend/app/routers/measurements.py`
  - `submit_measurement_endpoint()`・`member_approve_endpoint()`・`coach_approve_endpoint()` を `async def` に変更
  - `PATCH /api/measurements/{measurement_id}/confirm` エンドポイントを追加
- `backend/app/main.py`
  - `notifications` ルーターを登録
- `backend/requirements.txt`
  - `websockets==16.0` を追加

**フロントエンド**
- `frontend/src/stores/auth.js`
  - `login()` にWebSocket接続を追加
  - `initAuth()` にWebSocket接続を追加（重複接続防止付き）
  - `logout()` にWebSocket切断を追加
- `frontend/src/views/manager/DashboardView.vue`
  - 通知サマリーカードを追加（否認件数・部員承認待ち件数・コーチ承認待ち件数・新着通知）
  - 通知受信時のデータ再取得（`watch`）を追加
- `frontend/src/views/shared/DashboardView.vue`
  - 通知サマリーカードを追加（部員：承認依頼の有無、コーチ：承認待ち件数）
  - 通知受信時のデータ再取得（`watch`）を追加
- `frontend/vite.config.js`
  - WebSocket接続調査のため追加したプロキシ設定を削除（調査用途のため最終的に不使用）

### Technical Notes
- WebSocketはHTTPヘッダーを使用できないため、クエリパラメータでAccess Tokenを渡しJWT検証を行う
- PoCのシングルワーカー構成では問題ないが、本番運用時の複数ワーカー構成ではRedis Pub/Subの導入が必要
- `manager_confirmed` のデフォルト値はAlembicの `op.execute()` で条件付き設定（`approved` → TRUE、それ以外 → FALSE）
- WebSocketライブラリとして `websockets==16.0` を追加（`uvicorn[standard]` 相当）
- Viteの開発サーバーとWebSocketのパス競合を避けるため、直接 `ws://localhost:8000` へ接続する方式を採用

## 2026-03-27

## [ドキュメント] 提出物・手順書の整備

### Added
- `docs/test_accounts.md` を新規作成
  - seed.sqlを元にしたテストアカウント一覧
  - 動作確認推奨アカウントを記載
- `docs/presentation.md` を新規作成
  - 課題1の工夫点・アピール
  - 課題2の提案内容・実装済み機能・技術証明
  - デプロイ環境情報

### Changed
- `docs/CHANGELOG.md` を更新
  - インデックス＋フェーズA（設計・環境構築）として整理
- `docs/CHANGELOG_phase_b.md` を新規作成
  - 日付順（03-09→03-04→03-03）に整理
- `docs/CHANGELOG_phase_c.md` を新規作成
- `docs/CHANGELOG_phase_d.md` を新規作成
- `docs/CHANGELOG_phase_e.md` を新規作成
- `README.md` を更新
  - 「次の予定」セクションを更新（完了済み項目を削除・残タスクを整理）
  - `visualization/`配下のディレクトリ構成を修正
  - `composables/`・`views/shared/`配下を最新状態に更新

## [DB] インデックス追加

### Added
- `backend/alembic/versions/003_add_indexes.py` を新規作成
  - `ix_users_role`：ロール別絞り込みの高速化
  - `ix_users_status`：在籍状況での絞り込みの高速化
  - `ix_measurements_status`：承認フローの絞り込みの高速化
  - `ix_measurements_measurement_date`：計測日での絞り込みの高速化
  - `ix_measurements_user_id_measurement_date`：重複チェック用複合インデックス

### Technical Notes
- インデックスは別マイグレーションファイル（003）で管理

## 2026-03-26

## [課題2] 可視化ダッシュボード実装・コンポーネント責務分離

### Added
- `frontend/src/composables/useTrendData.js` を新規作成
  - 推移データ加工ロジックを分離（チーム平均・個人推移の時系列データ生成）
  - `getTrendSeries({ fieldKey, userId })` で統一インターフェース化
- `frontend/src/composables/useRadarData.js` を新規作成
  - レーダーチャート用データ加工ロジックを分離
  - 正規化処理・`lowerIsBetter`反転処理を含む
  - `getRadarSeries(playerIds)` / `getTeamAvgSeries()` を提供
- `frontend/src/composables/useRankingData.js` を新規作成
  - ランキングデータ加工ロジックを分離
  - `lowerIsBetter`対応・同率順位対応
  - `getRanking(fieldKey)` を提供
- `frontend/src/components/visualization/TrendChart.vue` を新規作成
  - ECharts折れ線グラフの描画専用コンポーネント
  - `series` / `labels` / `unit` をpropsで受け取る
- `frontend/src/components/visualization/TrendChartView.vue` を新規作成
  - 推移分析コンテナコンポーネント
  - `useTrendData`を使用してチーム推移・個人推移を切り替え表示
  - staffロールのみチーム推移タブを表示
- `frontend/src/views/shared/ChartView.vue` を新規作成
  - 3タブ構成（成長推移・能力比較・チーム内順位）
  - `getAllMeasurements()`で全件取得してpropsで渡す

### Changed
- `frontend/src/components/visualization/RadarChart.vue`
  - `useRadarData`を使用してUI特化に書き換え
  - データ加工ロジックを`useRadarData.js`に分離
- `frontend/src/components/visualization/RankingTable.vue`
  - `useRankingData`を使用してUI特化に書き換え
  - データ加工ロジックを`useRankingData.js`に分離
- `frontend/src/constants/measurementFields.js`
  - `lowerIsBetter`フラグを追加（sprint_50m・base_running）
- `frontend/src/stores/auth.js`
  - `isStaff` getterを追加（coach・directorの場合にtrue）
- `backend/app/routers/measurements.py`
  - `GET /api/measurements/all` エンドポイントを追加（可視化用全件取得）
- `backend/app/services/measurement_service.py`
  - `get_measurements()`に`include_all`引数を追加
  - memberロールでも`include_all=True`の場合は全件取得

### Removed
- `frontend/src/components/visualization/TeamTrendChart.vue`（TrendChartView.vueに統合）
- `frontend/src/components/visualization/PlayerTrendChart.vue`（TrendChartView.vueに統合）

### Technical Notes
- composablesパターンでデータ加工ロジックとUI描画を分離
- `toValue()`を使用してref・computed・生配列の全パターンに対応
- EChartsは`autoresize` + `style="height: 400px"`でDOMサイズエラーを回避
- 可視化用全件取得はバックエンド側で制御（フロントエンドからフラグ渡し不可）

## 2026-03-25

## [課題2] 重複登録防止・確認フロー追加

### Added
- `frontend/src/views/manager/MeasurementResultSubmit.vue`
  - 確認モーダルを追加（登録前に入力内容を確認してから承認依頼を送信）
  - `errorMessage` を追加（エラー種別に応じたメッセージ表示）

### Changed
- `backend/app/services/measurement_service.py`
  - `create_measurement()` に同一部員・同一計測日の重複チェックを追加
    - `rejected`ステータスのレコードが存在する場合は上書き更新して`draft`に戻す
    - `draft` / `pending_member` / `pending_coach` / `approved` の場合は400エラーを返す
  - `submit_measurement()` / `member_approve()` / `coach_approve()` に`updated_at`の明示的な更新を追加
  - `datetime` / `timezone` のimportを追加
- `frontend/src/views/manager/MeasurementResultSubmit.vue`
  - 登録処理を確認モーダル経由に変更（`handleSubmit` → モーダル表示、`handleConfirm` → API呼び出し）
  - 新規登録・上書き更新どちらも承認依頼まで自動送信する設計に変更
  - エラーハンドリングを`alert()`からインライン表示に変更
- `frontend/src/views/manager/MeasurementStatusList.vue`
  - `statusConfig`に`draft`を追加（label: 「入力済み（未依頼）」・badge: `bg-secondary`）

## [リファクタリング] AppHeader・各コンポーネントのCSS整理

### Changed
- `frontend/src/components/AppHeader.vue`
  - パンくずリスト（`showBreadcrumb`・`breadcrumbs`）を削除
  - `<style scoped>`を削除しBootstrapユーティリティクラスに統一
  - `sticky-top`・`fw-semibold`をHTMLクラスに移動
- 各コンポーネントのカスタムCSSをBootstrapユーティリティクラスで代用する形に統一

### Technical Notes
- `updated_at`はPython側（`datetime.now(timezone.utc)`）で明示的に管理する方針を全サービス関数に適用
- カスタムCSSはBootstrapで再現できない箇所のみ使用する方針に統一

## [課題2] コンポーネント分離・リファクタリング

### Added
- `frontend/src/components/measurement/MeasurementFilterBar.vue` を新規作成
  - ソート・絞り込みUIを共通コンポーネントとして分離
- `frontend/src/components/measurement/MeasurementTable.vue` を新規作成
  - 測定記録テーブルを共通コンポーネントとして分離
  - `showActions` propsで承認・否認ボタンの表示を制御
  - `submittingId` propsで二重クリック防止を制御
  - `MEASUREMENT_FIELDS`を使ってヘッダー・ボディを動的生成
- `frontend/src/components/member/MemberFilterBar.vue` を新規作成
  - 部員管理向けソート・絞り込みUIを分離
- `frontend/src/components/member/MemberTable.vue` を新規作成
  - 部員一覧テーブルを共通コンポーネントとして分離
- `frontend/src/components/member/MemberConfirmModal.vue` を新規作成
  - 退部・引退処理の確認モーダルを分離

### Changed
- `frontend/src/components/MeasurementResultList.vue`
  - `MeasurementFilterBar`・`MeasurementTable`を適用
  - `components/measurement/`配下のコンポーネントを利用する形に変更
- `frontend/src/components/MeasurementResultReview.vue`
  - `MeasurementFilterBar`・`MeasurementTable`を適用
  - `handleAction()`を追加して承認・否認処理を共通化
  - 二重クリック防止（`submittingId`）を追加
  - エラーハンドリングを`handleApprove`・`handleReject`に追加
- `frontend/src/components/MemberRetire.vue`
  - `MemberFilterBar`・`MemberTable`・`MemberConfirmModal`を適用

## [課題2] 可視化ダッシュボード骨格実装

### Added
- `frontend/src/views/shared/ChartView.vue` を新規作成
  - タブ切り替えによる4グラフ表示の骨格を実装
  - ロール別タブ表示制御（member：2タブ、coach・director：4タブ）
- `frontend/src/components/visualization/TeamTrendChart.vue` を新規作成（実装中）
- `frontend/src/components/visualization/PlayerTrendChart.vue` を新規作成（実装中）
- `frontend/src/components/visualization/RadarChart.vue` を新規作成（実装中）
- `frontend/src/components/visualization/RankingTable.vue` を新規作成（実装中）
- `frontend/src/views/shared/DashboardView.vue`
  - 「可視化ダッシュボード」カードを追加

### Changed
- `frontend/src/router/index.js`
  - `member`・`coach`・`director`ルートに`chart`を追加
  - `breadcrumbs`のダッシュボードリンクをロール別に修正

### Technical Notes
- ECharts・vue-echartsをインストール（`echarts`・`vue-echarts`）
- タブ定義はキー・ラベル・表示ロール配列で管理
- 各グラフコンポーネントは`components/visualization/`配下に配置

## 2026-03-24

## [課題2] コンポーネントのリファクタリング・機能追加

### Added
- `frontend/src/composables/usePagination.js` を新規作成
  - ページネーションロジック（currentPage・pageSize・totalPages・paginatedData・ページ番号補正）を共通化
- `frontend/src/components/Pagination.vue` を新規作成
  - ページネーションUI（件数選択・ページ送りボタン）を共通コンポーネントとして分離
- `frontend/src/constants/measurementFields.js` を新規作成
  - 測定項目定義（key・label・unit・step・placeholder・category）を定数として切り出し

### Changed
- `frontend/src/components/MeasurementResultList.vue`
  - usePagination・Paginationコンポーネントを適用
  - MEASUREMENT_FIELDSを定数として参照するように変更（削除済みのインライン定義を整理）
- `frontend/src/components/MemberRetire.vue`
  - usePagination・Paginationコンポーネントを適用
  - closeModal()関数を追加（selectedMember・actionTypeのリセット処理を含む）
  - onMounted・handleProcessにtry/catchを追加
  - URLからpageSizeを復元する処理を追加
- `frontend/src/views/manager/MeasurementStatusList.vue`
  - usePagination・Paginationコンポーネントを適用
  - ソート・絞り込み・ページネーション機能を追加
    - 部員名テキスト検索・学年・ステータス・計測日フィルタを追加
    - ソート対象：部員名・学年・ステータス・計測日
    - フィルタ・ソート条件をURLクエリパラメータに同期
    - リセットボタンを追加（条件未設定時は無効化）
  - セクションコメントを整理（インポート・定数・computed・メソッド・副作用の順）
- `frontend/src/components/MeasurementResultReview.vue`
  - usePagination・Paginationコンポーネントを適用
  - MEASUREMENT_FIELDSを定数として参照するように変更
  - コーチ向けにソート・絞り込み機能を追加
    - 部員名テキスト検索・学年・計測日フィルタを追加
    - ソート対象：部員名・学年・計測日
    - コーチ以外（部員）はフィルタUIを非表示
  - 部員・コーチで異なるタイトル表示を実装
- `frontend/src/components/Pagination.vue`
  - 件数選択に`w-auto`を追加（幅の最適化）
  - ページ数表示に`white-space: nowrap`を追加（折り返し防止）
  - ページ操作divに`flex-nowrap`を追加（折り返し防止）

## [セキュリティ] ログイン画面からテストアカウント情報を削除

### Changed
- `frontend/src/views/LoginView.vue`
  - テストアカウント情報（メールアドレス・パスワード）の表示を削除

## [バグ修正] AppHeader.vueのログアウト処理を修正

### Fixed
- `frontend/src/components/AppHeader.vue`
  - `handleLogout()`に`router.push("/login")`を追加
  - `useRouter`のimportを追加
  - 修正前：ログアウト後にログイン画面へ遷移しない不具合があった
  - 修正後：ログアウト後に正常にログイン画面へ遷移するようになった

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
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
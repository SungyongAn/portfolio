
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

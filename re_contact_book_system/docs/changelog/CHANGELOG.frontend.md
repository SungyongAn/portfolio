# Frontend Changelog

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

## 2026/02/03
### Added
- 連絡帳（Journal）機能のフロントエンド画面を追加
  - 状態管理: `stores/journal.js`
  - API 呼び出し: `journalService.js`
  - 生徒向け連絡帳提出画面: `SubmitView.vue`
  - 生徒向け連絡帳履歴表示画面: `HistoryView.vue`

### Changed
- 連絡帳関連フロントエンドの構成を整理
  - 既存バックエンド API を利用する形で画面設計を調整
  - 連絡帳取得・提出処理をサービス層経由で呼び出す構成に変更
  - 表示用データ構造を API レスポンスに合わせて調整

### Changed
- 連絡帳取得・提出処理を service 経由に変更

## 2026/02/01
### Changed
- 認証初期化処理（initAuth）の設計を改善
  - アプリ起動時のアクセストークンリフレッシュ処理を整理
  - 未ログイン状態では refresh API の失敗をエラーとして扱わないように変更
  - 認証状態に応じた初期化フローを明確化

## 2026/01/26
### Changed
- 認証方式を interceptor による 401 ハンドリング中心の構成へ変更
  - アクセストークンはメモリ管理、リフレッシュトークンは HttpOnly Cookie 管理へ移行
  - フロントエンドでのリフレッシュトークン保持を廃止
  - 無操作ログアウト処理を認証ストアに集約
  - 認証初期化処理を refresh API ベースで再設計
  - 詳細設計は `docs/design/auth-design.md` を参照

## 2026/01/23
### Added
- 共通ヘッダー / フッターを実装
- ロール別ナビゲーション表示を追加

## 2026/01/16
### Changed
- 認証ストア（Pinia）を更新し、アクセストークンをメモリ上で管理
- `auth.js` / `api.js` を更新
  - `refreshToken` の localStorage 保存を削除
  - axios の `withCredentials` を設定し、Cookie 経由でリフレッシュトークンを送信
- `main.js` / `LoginView.vue` を更新

## 2026/01/14
### Added
- 管理者用コンポーネントの作成を開始
  - `UsersView.vue` `UserCreateView.vue` を作成
  - 空ファイルの `UserEditView.vue` `GradesView.vue` `ClassesView.vue` を作成
  - `UserManagementView.vue` を削除
  - `api.js` `index.js` を更新

## 2026/01/07
### Changed
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

## 2025/12/30
### Added
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

### Fixed
- Viteの import エラーを解決（ビューファイルの不足を修正）
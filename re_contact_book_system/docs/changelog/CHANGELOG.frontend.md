# Frontend Changelog

--------------------------------------------

Fixed：バグ修正
Infrastructure：環境・基盤変更（アプリの挙動自体は変わらない）
Refactored：動作を変えないコード改善（内部構造のみ変更）
Removed：完全削除
Deprecated：今は使えるが将来削除予定
Security：安全性に関わる変更

⚠️ Breaking Change：破壊的変更
※補足：
アップデート後、これまで動いていた利用者側のコードや使い方が、
そのままでは動作しなくなり、修正が必要となる変更を指します。

例：
- DBスキーマの変更（名称変更・型変更・必須項目の追加など）
- テーブルのカラム追加・削除・名称変更
- APIリクエスト／レスポンス仕様の変更により、
  利用者側の実装修正が必要になる場合

※原則として、項目の追加のみで既存の挙動や前提が変わらない場合は
Breaking Change には該当しません。
※ Breaking Change は変更内容のカテゴリではなく、
各項目に付随する注意事項です。

--------------------------------------------

## 2026/02/12
### Changed
- 認証フローの実装を改善
  - authService では API 通信のみを担当し、state 更新処理を Pinia store に集約
  - login / refreshToken 処理の責務を明確化

- Pinia auth store の構造を整理
  - primary_assignment をオブジェクトとして保持する形に統一
  - teacher_assignments を将来拡張可能な構造として保持

### Fixed
- 教師ダッシュボードで担当区分が undefined になる問題を修正
  - store の state 構造と View 側の参照先の不一致を解消

## 2026/02/10
### Added
- 管理者画面のユーザー一覧ページにおける表示用フィールドを統一
  - `displayRole`、`displayGrade`、`displayClass` を追加
  - 生徒・教師・管理者で情報取得元が異なる場合も template 側で統一的に表示可能に

### Changed
- `fetchUsers` 内で取得したユーザー情報を整形し、template 用の表示情報を事前に生成
  - 教師の場合は `primary_assignment` から `assignment_type`、`grade_number`、`class_name` を取得
  - 生徒の場合は `student_class` から `grade_number`、`class_name` を取得
  - 管理者の場合は role 表示のみ
- template 側での role / クラス情報の条件分岐を簡略化
  - `user.displayRole`、`user.displayGrade`、`user.displayClass` を参照する形に変更
- ロールバッジ表示も `displayRole` を参照するように変更

### Refactored
- 教師・生徒・管理者の表示ロジックを `fetchUsers` 内で集約
  - template 側では表示専用フィールドのみを参照
  - 表示ロジックの重複や分岐を削減

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
# CHANGELOG

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
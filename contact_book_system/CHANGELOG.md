# Changelog

All notable changes to this project will be documented in this file.

## 2025-12

## 12/10

- **Viteの導入（続き）**
  - 各種コンポーネントのVue SFC 形式に変換
  - `main.js` の内容を修正
  - `renrakucho-app` ディレクトリを削除
  - `npm create vite@latest frontend -- --template vue` でViteプロジェクトの作成をやり直し
  - `components` `App.vue` `main.js` を作成済みのファイルに更新
  - Bootstrap / Font Awesome / axios をインストール

## 12/9

- **部分修正**
  - フロントエンド
    - `AccountSearch.js` と教員区分マスタ・科目マスタで `code` 情報が違っていたため教員区分マスタ・科目マスタを修正
    - `AccountUpdateTable` の氏名表示を姓・名へ対応と、教師情報の更新時に教員区分・担当科目が空白だった状態から現在の設定状況を初期表示とするように変更
  - バックエンド
    - `account_service.py` を `id` から `email` に、 `fullName` から `last_name` と `first_name` への変更に対応した内容に一部修正
    - 4月1日午前1時に3年を卒業、１年２年は学年を+1と自動で行うイベントを `promote_students` を作成

- **年次処理機能の追加**
  - フロントエンド
    - `AccountManagementMenu.js` に年度処理の項目を追加
    - `YearlyProcessingMenu.js` を作成

- **Viteの導入開始**
  - `index.html` `app.js` の冗長化に伴いViteの導入開始
  - `npm create vite@latest renrakucho-app -- --template vue` Viteプロジェクトの作成
  - `/src` 配下に `/components` を移動
  - `/src` 配下に `App.vue` `main.js` を作成
  - 各種コンポーネントのVue SFC 形式に変換を開始

## 12/8

- **ログイン機能の仕様変更**
  - フロントエンド
    - `LoginForm.js` を修正し、ログインIDとして メールアドレスのローカルパートを入力する形式に変更
    - バックエンドへ送信する前に、ローカルパートに固定ドメインを付与して 完全な `email` を生成 するように変更
    - `UserHeader.js` を氏名から姓、名を表示するように変更
  - バックエンド
    - `auth_schema.py` の `LoginRequest` で、フィールド名を `id` から `email` に変更
    - `auth.py`（service / api）の認証処理を、従来の `id` ベースから `email` ベースに変更

- **連絡帳アーカイブ機能の追加(データベース)**
  - テーブル追加
    - `renrakucho_entries_archive`：連絡帳の過去データを保存するアーカイブテーブル（3～5年分）
    - `data_deletion_log`：アーカイブデータ削除時の監査ログ用テーブル
  - ストアドプロシージャ追加
    - `archive_old_renrakucho(years INT)`：古い連絡帳をアーカイブ
    - `delete_expired_renrakucho(retention_years INT)`：保管期限切れアーカイブデータを削除
    - `get_archive_statistics()`：アクティブ・アーカイブデータの統計取得
  - スケジュールイベント追加
    - `yearly_archive_renrakucho`：毎年4月1日午前2時にアーカイブ実行
    - `yearly_delete_expired_renrakucho`：毎年4月1日午前3時に削除実行（アーカイブ1時間後）

- **アカウント検索機能の仕様変更**
  - フロントエンド
    - `AccountSearch.js` を修正し、ログインIDとして メールアドレスのローカルパートを入力する形式に変更
    - バックエンドへ送信する前に、ローカルパートに固定ドメインを付与して 完全な `email` を生成 するように変更
    - 氏名を姓、名と分けて入力する形式に変更
  - バックエンド
    - `accounts_schema.py` 内のフィールド名を `id` から `email` に、 `fullName` から `last_name` と `first_name` に全て変更
    - `account_repository.py` を `id` から `email` に、 `fullName` から `last_name` と `first_name` への変更に対応した内容に修正
    - `account_service.py` を `id` から `email` に、 `fullName` から `last_name` と `first_name` への変更に対応した内容に一部修正

## 12/7

- **アカウント登録機能の仕様変更**
  - フロントエンド
    - `AccountForm.js` を修正し、生徒・職員ID入力欄をローカルパート入力欄に変更（ドメインを固定）
    - アカウント登録時にバックエンドへ送信する項目を id から email に変更
  - バックエンド
    - `accounts_schema.py` の `AccountRegisterRequest` に `email` フィールドを追加
    - `account_repository.py`に`def find_by_email()`メゾットを追加

## 12/4

- **ドキュメント整理**
  - `README.md` から開発履歴部分を抽出し、`CHANGELOG.md` に整理

- **ログイン機能の仕様変更**
  - ログイン方式を **メールアドレス + パスワードのみ** に統一
  - フロントエンド
    - `LoginForm.js` を更新し、不要な項目を削除
    - 認証 API 呼び出し処理をメールアドレス専用仕様に変更
  - バックエンド
    - `auth_schema.py` を修正（ログイン用スキーマをメールアドレス専用に）
    - `auth.py` の認証処理を更新（ユーザー名不要のメールアドレス認証へ変更）
    - `accounts_model.py` に `email` カラムを追加
      - ログイン ID をメールアドレスで管理するため
      - `email: String(255), nullable=False` を新規追加
      - 今後の認証方式をメールアドレス＋パスワードに統一するための更新

## 2025-11

### 11/18

- **スケジュールイベント**
  - 年次アーカイブイベントを作成
  - 年次削除イベントを作成
- **バックエンド開発**
  - `archive_schema.py` を作成（Null 許容型・ユニオン型に変更）
  - `archive_service.py` を作成
- **データベース管理**
  - プロシージャへのアクセス権限を持ったユーザーを作成
  - アーカイブ管理用コンポーネントからデータベースへアクセスできたことを確認

### 11/17

- **データベース設計**
  - アーカイブ・削除・データ統計取得プロシージャを作成
- **UI 開発**
  - システム管理者用のアーカイブ管理用コンポーネントを作成
- **開発環境改善**
  - Prettier が正常に機能していなかった問題を解決

### 11/14

- **ヘッダー表示の調整**
  - 学年主任：学年のみ表示
  - 養護教諭・教科担当：学年・組ともに非表示
- **権限設定の調整**
  - 学年主任ログイン時、一時的に担任・副担任と同じ機能を使えるように設定
  - 教科担当ログイン時は報連相部屋（仮）のみ使えるように設定
- **アカウント管理**
  - アカウント情報検索時に管理者権限のアカウントを除外するように設定
- **連絡帳フォーム**
  - 連絡帳フォームの構成を更新
- **養護教諭機能**
  - ログイン時にメインメニューを表示するように変更
  - 報連相（仮）、生徒の状況確認（仮）を設定
- **アーカイブシステム**
  - 卒業生の連絡帳管理システムの構築を開始（`卒業生の連絡帳情報管理システム.md` を参考）
  - アーカイブ・削除テーブルを作成

### 11/12

- **WebSocket 通信管理**
  - チャットルーム・養護教諭専用ページ退出時に WebSocket 通信を自動切断してバックエンドへ通知する設定を追加
  - バックエンドで上記通知を受け取り処理する機能を追加
- **チャット機能拡張**
  - リアルタイムでのメッセージ更新を実装
  - 入力中の表示を実装
  - 未読メッセージ数の表示を実装

### 11/11

- **ブラウザ機能対応**
  - 戻る・進む・更新ボタンへの対応（`app.js` を更新）
- **チャット機能強化**
  - チャットルーム参加者の表示機能を追加（`ChatRoom.js` を更新）
  - 参加者のオンライン/オフライン表示機能を追加（`ChatRoom.js` を更新）
- **WebSocket 通信**
  - 対象アカウントとの通信状況の定期確認（ping）を実装

### 11/4

- 採用インターン課題提出内容の復習・見直しを開始

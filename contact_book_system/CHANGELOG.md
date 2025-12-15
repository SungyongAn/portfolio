# Changelog

All notable changes to this project will be documented in this file.

## 2025-12

## 12/15

- **Docker Desktop 起動時のコンテナ自動機能を停止**

  - `docker-compose.yml` の全ての `restart:` を `always` から `no` に変更

- **FastAPI の設計思想に合わせ、バックエンド構成を明確化するため `routes` ディレクトリを `app` に名称変更**

  - バックエンド
    - ディレクトリ名を `routes` から `app` に変更
    - 上記に伴い `/app` に `__init__.py` を作成
    - 上記に伴い、import 文を `from routes.*` から `from app.*` に修正

## 12/14

- **開発環境のパスワードリセット機能の実装**

  - フロントエンド
  - `LoginForm.vue` を更新

  - バックエンド
    - `auth_schema.py` `/api/auth.py` `/service/auth.py` を更新
    - `password_reset_model.py` を作成

## 12/13

- **一部機能の更新、修正**

  - フロントエンド
    - `UserHeader.vue` の戻るボタンを、`Vue Router` の履歴管理機能を利用する実装に変更
    - `AccountForm.vue` の `template` の欠損を復元

## 12/12

- **画面管理に Vue Router を使う仕様に変更**

  - フロントエンド
    - コンポーネントの更新の続きを行い、既存のコンポーネント全ての更新を完了

- **ブラウザの戻るボタンでログイン画面に戻る際にヘッダーが残る問題を修正**

  - フロントエンド
    - `App.vue` `MainMenu.vue` `AccountManagementMenu.vue` を更新
    - 合わせて `LoginForm.vue` に戻ったらユーザー情報もリセットするように更新(`App.vue`)

## 12/11

- **ローカル環境のコンテナ化**

  - バックエンド
    - コンテナ後にデータベース接続でエラー発生していたため `db.py` 内の `DATABASE_URL` を修正

- **画面管理に Vue Router を使う仕様に変更**

  - フロントエンド
    - `npm install vue-router` にて `vue-router` をインストール
    - `src` 配下に `router`ディレクトリと `main.js` を作成
    - `router` 配下に `index.js` を作成
    - `App.vue` を `Vue Router` に対応、かつコンポーネント内の画面切り替えボタンに対応した内容に更新
    - コンポーネントの更新を開始 次回 `PastRenrakuchoSearch.vue` の修正から

## 12/10

- **Vite の導入（続き）**

  - 各種コンポーネントの Vue SFC 形式に変換
  - `main.js` の内容を修正
  - `renrakucho-app` ディレクトリを削除
  - `npm create vite@latest frontend -- --template vue` で Vite プロジェクトの作成をやり直し
  - `components` `App.vue` `main.js` を作成済みのファイルに更新
  - Bootstrap / Font Awesome / axios をインストール

- **その他**
  - `frontend_old` を削除
  - `login_info.txt` と情報が被っていたため `accounts.csv` `accounts.json` `accounts.txt` を削除
  - Vite の導入に合わせてフロントエンドの `Dockerfile` と `docker-compose.yml` を修正

## 12/9

- **部分修正**

  - フロントエンド
    - `AccountSearch.js` と教員区分マスタ・科目マスタで `code` 情報が違っていたため教員区分マスタ・科目マスタを修正
    - `AccountUpdateTable` の氏名表示を姓・名へ対応と、教師情報の更新時に教員区分・担当科目が空白だった状態から現在の設定状況を初期表示とするように変更
  - バックエンド
    - `account_service.py` を `id` から `email` に、 `fullName` から `last_name` と `first_name` への変更に対応した内容に一部修正
    - 4 月 1 日午前 1 時に 3 年を卒業、１年２年は学年を+1 と自動で行うイベントを `promote_students` を作成

- **年次処理機能の追加**

  - フロントエンド
    - `AccountManagementMenu.js` に年度処理の項目を追加
    - `YearlyProcessingMenu.js` を作成

- **Vite の導入開始**
  - `index.html` `app.js` の冗長化に伴い Vite の導入開始
  - `npm create vite@latest renrakucho-app -- --template vue` Vite プロジェクトの作成
  - `/src` 配下に `/components` を移動
  - `/src` 配下に `App.vue` `main.js` を作成
  - 各種コンポーネントの Vue SFC 形式に変換を開始

## 12/8

- **ログイン機能の仕様変更**

  - フロントエンド
    - `LoginForm.js` を修正し、ログイン ID として メールアドレスのローカルパートを入力する形式に変更
    - バックエンドへ送信する前に、ローカルパートに固定ドメインを付与して 完全な `email` を生成 するように変更
    - `UserHeader.js` を氏名から姓、名を表示するように変更
  - バックエンド
    - `auth_schema.py` の `LoginRequest` で、フィールド名を `id` から `email` に変更
    - `auth.py`（service / api）の認証処理を、従来の `id` ベースから `email` ベースに変更

- **連絡帳アーカイブ機能の追加(データベース)**

  - テーブル追加
    - `renrakucho_entries_archive`：連絡帳の過去データを保存するアーカイブテーブル（3 ～ 5 年分）
    - `data_deletion_log`：アーカイブデータ削除時の監査ログ用テーブル
  - ストアドプロシージャ追加
    - `archive_old_renrakucho(years INT)`：古い連絡帳をアーカイブ
    - `delete_expired_renrakucho(retention_years INT)`：保管期限切れアーカイブデータを削除
    - `get_archive_statistics()`：アクティブ・アーカイブデータの統計取得
  - スケジュールイベント追加
    - `yearly_archive_renrakucho`：毎年 4 月 1 日午前 2 時にアーカイブ実行
    - `yearly_delete_expired_renrakucho`：毎年 4 月 1 日午前 3 時に削除実行（アーカイブ 1 時間後）

- **アカウント検索機能の仕様変更**
  - フロントエンド
    - `AccountSearch.js` を修正し、ログイン ID として メールアドレスのローカルパートを入力する形式に変更
    - バックエンドへ送信する前に、ローカルパートに固定ドメインを付与して 完全な `email` を生成 するように変更
    - 氏名を姓、名と分けて入力する形式に変更
  - バックエンド
    - `accounts_schema.py` 内のフィールド名を `id` から `email` に、 `fullName` から `last_name` と `first_name` に全て変更
    - `account_repository.py` を `id` から `email` に、 `fullName` から `last_name` と `first_name` への変更に対応した内容に修正
    - `account_service.py` を `id` から `email` に、 `fullName` から `last_name` と `first_name` への変更に対応した内容に一部修正

## 12/7

- **アカウント登録機能の仕様変更**
  - フロントエンド
    - `AccountForm.js` を修正し、生徒・職員 ID 入力欄をローカルパート入力欄に変更（ドメインを固定）
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

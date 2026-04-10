# CHANGELOG

## 2026-04-10 フェーズA 設計同期セッション

---

### 対応内容概要

前回のusecase再構成・UC番号体系変更に合わせてfunctions・screens・erを同期更新した。

---

### ドキュメント別変更履歴

#### functions.md
- UC番号を新体系（UC-01〜29）に全面修正
- 生徒機能をF-S01〜F-S17に再整理（資料詳細取得・各一覧確認・図書館間貸出関連を追加）
- 図書委員機能をF-C01〜F-C08に再整理（予約キャンセル代理を追加）
- 司書機能をF-L01〜F-L19に再整理（資料情報更新・発送登録等を追加）
- 管理者機能をF-A01〜F-A07に再整理（生徒詳細取得を追加）
- 貸出延長はF-EX04（課題2）に留置

#### screens.md
- 詳細セクションを削除しインデックス形式に変更・詳細ファイル列を追加
- 個別ファイル17本をscreens/ディレクトリに新規作成
- SCR-09に資料情報更新操作を追加（UC-24対応）

#### er.md
- books.status遷移にreserved→inter_libraryを追加
- inter_library_requests.statusのキャンセル可能範囲をpending・confirmedのみに確定・明記

---

### 次回対応予定（未完了事項）

| 項目 | 内容 |
|------|------|
| 貸出延長（UC-28）設計確定 | 延長回数上限・延長期間・操作画面・権限を確認後、er.md / loans.md / screens.md / role_matrix.mdに反映 |
| users.mdのパス記法修正 | 絶対パスを相対パスに統一 |
| auth_session.mdの401フロー図整形 | フロー図形式に修正 |
| フェーズA-7 Docker環境構築 | Viteプロジェクト初期化（`--template vue-ts`）含む |
| フェーズA-8 Alembic環境構築 | マイグレーションファイル作成 |
| フェーズA-9 バックエンド環境構築 | `db.py`・`.env`作成 |

---



## 2026-04-09 フェーズA 設計精査セッション

---

### 対応内容概要

インターンシップ開始（4月13日）に向けて、フェーズAの設計ドキュメント全7点を精査・更新した。
また、ユースケースおよびAPI設計のファイル分割・構造化を実施した。

---

### ドキュメント別変更履歴

#### usecase.md
- ロール定義に図書委員（`is_committee`フラグ方式・案B）を追加
- UC-02の対象ロールを生徒のみ→全ロールに変更
- UC-03のタイトルを「同校」→「自校蔵書」に変更、他校資料はUC-12経由を明記
- UC-04の「誰が」に司書・図書委員を追加
- UC-05に貸出前提条件（予約者確認・他校含む）を追記
- UC-06に返却先の柔軟性（どの学校でも可）を明記
- UC-08の登録項目に学年・クラスを追加、メール通知→手渡しに変更
- UC-10のNDL連携→手入力方式に変更
- 最小限画面一覧をSCR番号付きで全17画面に更新
- **ファイル分割**：ドメインごとに以下へ分割
  - `auth.md`（UC-01〜04）
  - `search.md`（UC-05〜06、UC-35）
  - `reservation.md`（UC-07〜10、UC-31〜32）
  - `loan.md`（UC-11〜13、UC-28貸出延長※未確定）
  - `interlibrary.md`（UC-17〜22）
  - `librarian.md`（UC-23〜25）
  - `admin.md`（UC-26〜29）
  - `system.md`（システム自動処理）
  - `usecase.md`（インデックス・画面一覧）

#### functions.md
- 生徒機能にログイン・パスワードリセット・予約キャンセル（自校・図書館間）を追加、F-S01〜F-S13に整理
- 図書委員追加機能セクションを新設（F-C01〜F-C07）
- 司書機能にログイン・代理操作・貸出管理・延滞CSV出力等を追加（F-L01〜F-L15）
- 管理者機能にログイン・パスワード変更・リセット申請を追加（F-A01〜F-A06）
- システム自動処理に貸出上限チェック（F-SYS05）・延滞制限チェック（F-SYS06）を追加
- 課題2候補にF-EX07（権限テーブル方式移行）を追加

#### er.md
- `users`テーブルに`grade`・`class_name`・`is_committee`カラムを追加
- `password_reset_tokens`テーブルを新規追加
- `books.status`遷移に`reserved`→`inter_library`の遷移を追加
- `inter_library_requests.status`遷移にキャンセル可能範囲を明記
- 採番ルール（バーコード統合方針）を追記

#### screens.md
- SCR-02をstudent・committee共通化、図書委員向け代理操作メニューを追加
- SCR-03（司書DB）に代理操作メニューを追加
- SCR-05/06を全ロール対象に変更
- SCR-06に締め切り後メッセージ・貸出上限・延滞制限の表示制御を追加
- SCR-06に代理操作UI（committee / librarianのみ表示）を追加
- SCR-07に対応ロールを明記
- SCR-09の資料追加フォームの入力項目を明記
- SCR-11に学年・クラス・図書委員フラグを追加
- SCR-12/13（パスワードリセット）を新規追加
- SCR-14（貸出管理・図書委員）を新規追加
- SCR-15（貸出管理・司書）を新規追加
- SCR-16（貸出処理）を新規追加
- SCR-17（返却処理）を新規追加
- 貸出ルールセクション（上限5冊・延滞制限）を追加
- 画面遷移図を全17画面対応に更新

#### api.md
- `GET /api/auth/me`を追加（全ロール対象・リロード時の氏名再取得用）
- ログインレスポンスに`is_committee`を追加
- ユーザー登録・一覧レスポンスに`grade`・`class_name`・`is_committee`を追加
- `GET /api/loans`を削除（用途不明確なため）
- `POST /api/loans`・`PATCH /api/loans/{loan_id}/return`をバーコード方式に変更
  - `POST /api/loans/loan-by-barcode`
  - `PATCH /api/loans/return-by-barcode`
- 貸出・予約・図書館間貸出の全エンドポイントに`committee`権限を追加
- `DELETE /api/reservations/{reservation_id}`のキャンセル制限を明記（`waiting`・`ready`のみ）
- `DELETE /api/inter-library/{request_id}`のキャンセル制限を明記（`pending`・`confirmed`のみ）
- `PATCH /api/inter-library/{request_id}/ship`のリクエスト・レスポンスを追加
- `GET /api/loans/management`セクションを「貸出状況管理」として整理
- パスワードリセットエンドポイントを追加
- HTTPメソッド方針・ステータスコード方針を追加
- **ファイル分割**：リソースごとに以下へ分割
  - `auth.md`
  - `users.md`
  - `books.md`
  - `loans.md`
  - `loan-management.md`
  - `reservations.md`
  - `interlibrary.md`
  - `api.md`（概要・方針・一覧インデックス）

#### role_matrix.md
- 図書委員（`committee`）列を追加
- パスワードリセット申請・実行行を追加（全ロール対象）
- マイページ閲覧行を追加（student・committee）
- 司書の自己貸出・返却を❌に変更、補足ルールに明記
- 予約キャンセル代理操作行を追加
- 図書館間貸出キャンセル（自分・代理）行を追加
- 貸出管理・延滞CSV出力行を追加
- 「全貸出一覧閲覧」行を削除
- 貸出ルールセクションを追加
- 補足ルールに管理者アカウント管理方針（seed.sql初期投入）を追記

#### auth_design.md
- 環境別Cookie設定テーブルを追加（開発：SameSite=Lax・Secure無効、本番：SameSite=Strict・Secure有効）
- パスワードリセットのトークン管理セクションを新規追加（生成方式・リセットフロー）
- JWTペイロードに`is_committee`を追加
- `name`の取り扱い方針を追記（JWTには含めず`GET /api/auth/me`で再取得）
- ログアウト時の処理フローを新規追加
- **ファイル分割**：以下へ分割
  - `auth_overview.md`（認証方式・フロー概要）
  - `auth_tokens.md`（トークン設計・Cookie・JWTペイロード）
  - `auth_password.md`（Argon2・リセットトークン管理）
  - `auth_session.md`（リロード復元・自動ログアウト・401処理・ログアウト処理）

---

### 設計上の確定ルール

| ルール | 内容 |
|--------|------|
| 図書委員の権限管理 | `is_committee`フラグ方式（案B）。将来的に権限テーブル方式へ移行を課題2で検討 |
| 貸出上限 | 1人あたり同時5冊まで（図書館間貸出含む） |
| 延滞制限 | 延滞中は新規貸出・予約不可 |
| 予約キャンセル制限 | `waiting`・`ready`のみ可能 |
| 図書館間貸出キャンセル制限 | `pending`・`confirmed`のみ可能（`shipped`以降は不可） |
| 貸出・返却操作 | バーコードスキャン方式（`loan-by-barcode`・`return-by-barcode`） |
| 管理者アカウント管理 | seed.sqlで初期投入。追加はDB直接操作で対応（課題2で管理画面を検討） |
| 司書の自己貸出 | 課題1では対象外（代理操作専任） |
| パスワードリセット | メールリンク方式・トークン有効期限30分・1回使い捨て |

---

### 次回対応予定（未完了事項）

| 項目 | 内容 |
|------|------|
| 貸出延長（UC-28）の設計確定 | 延長回数上限・延長期間・操作画面・権限を確認後、er.md / loans.md / screens.md / role_matrix.mdに反映 |
| users.mdのパス記法修正 | 絶対パスを相対パスに統一 |
| auth_session.mdの401フロー図整形 | フロー図形式に修正 |
| フェーズA-7 Docker環境構築 | Viteプロジェクト初期化（`--template vue-ts`）含む |
| フェーズA-8 Alembic環境構築 | マイグレーションファイル作成 |
| フェーズA-9 バックエンド環境構築 | `db.py`・`.env`作成 |

---

### 設計方針メモ（次回引き継ぎ用）

- role_matrixはusecaseと並走させて早期に仮定義するとその後の手戻りが減る（今回の教訓）
- TypeScriptはViteプロジェクト初期化時に`--template vue-ts`で設定する
- デプロイ先はOracle Cloud Always Free（Ubuntu VM・既存環境流用）
  - SSH: `ssh -i C:\Users\hanip\Downloads\ssh-key-2026-03-22.key ubuntu@168.138.193.7`
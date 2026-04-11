# CHANGELOG

## 2026-04-11 フェーズB 事前準備セッション

### 対応内容概要
フェーズB（モックUI実装）の開始に向けて、型定義・定数・Composables・
状態管理・ルーティング・ダミーデータの作成を行った。

### 作成ファイル

| ファイル | 内容 |
|---------|------|
| `types/index.ts` | 各ドメイン型の re-export |
| `domains/*/types.ts` | ドメイン別型定義（user / book / loan / reservation / interLibrary / school / auth） |
| `domains/*/constants.ts` | ドメイン別定数定義（ステータス値・ラベル・Bootstrapカラークラス） |
| `shared/constants/route.ts` | ロール別デフォルトルート・ログインルート |
| `shared/types/api.ts` | ApiError・PaginatedResponse |
| `constants/index.ts` | 各ドメイン定数の re-export |
| `composables/useAuth.ts` | 認証状態・ロール判定 |
| `composables/usePermission.ts` | 貸出上限・延滞制限・キャンセル可否チェック |
| `composables/useLoanStatus.ts` | 貸出状態の表示変換・返却期限算出 |
| `composables/useInterlibraryDeadline.ts` | 図書館間貸出 金曜15:00締切判定 |
| `stores/auth.ts` | 認証状態管理（Pinia）・localStorage によるトークン保持 |
| `router/index.ts` | ロール別ルート構成・ナビゲーションガード・ページタイトル更新 |
| `router/types.ts` | RouteMeta 型拡張 |
| `dummyData/index.ts` | 全ロール・全ステータスのダミーデータ（ユーザー・資料・貸出・予約・図書館間貸出） |
| `views/**/*.vue` | 17画面の空ファイル作成 |

### 確定した実装方針

| 項目 | 内容 |
|------|------|
| 言語 | TypeScript（モック段階から `.ts` で統一） |
| CSSフレームワーク | Bootstrap（バッジは `bg-*` クラスで統一） |
| トークン管理 | モック段階は localStorage / Pinia。本番は HttpOnly Cookie

## 2026-04-11 フェーズA 見直し・修正セッション

### 対応内容概要

フェーズAの計画書との照合を実施し、未対応事項の対応および各ファイルの修正を行った。

### 対応内容

#### auth_session.md
- 401エラー処理フローをMermaid flowchart形式に整形

#### alembic_guide.md
- 「初回セットアップ（ローカル作業）」セクションを追加
  - `alembic init` はDockerビルド前にローカルで一度だけ実施する旨を明記
  - `alembic.ini` / `env.py` の編集手順・マイグレーションファイル作成手順を追記
  - `--autogenerate` はDB接続が必要なため初回不可である旨を注記
- 構成概要をモデルファイル分割後の実際の構造に更新
- 未完了事項から対応済み項目を削除

#### app/models/（school / user / book / reservation / inter_library）
- `created_at` / `updated_at` を `DateTime + onupdate=datetime.utcnow` から
  `sa.TIMESTAMP + server_default` に変更（MySQL側で `ON UPDATE CURRENT_TIMESTAMP` を管理）
- `user.py` の `from sqlalchemy import` から不要になった `DateTime` を削除

#### alembic/versions/001_initial_.py
- `created_at` / `updated_at` を `sa.TIMESTAMP() + server_default` に更新
  （モデル定義との整合を確保）

#### backend/.env（新規作成）
- ルートの `.env` との整合を取り統合版として作成
  - `DATABASE_URL` / `SECRET_KEY` / `ACCESS_TOKEN_EXPIRE_MINUTES` をルートに統一
  - `MAIL_BACKEND=console` を追加

#### backend/app/db.py
- フォールバックURLのユーザー名・パスワードを `library_user:library_password` に統一
- コメント行の古い接続情報を修正

#### alembic.ini
- `sqlalchemy.url` を `library_user:library_password` に統一

#### scripts/seed_users.py
- フォールバックURL・コメントのローカル実行例を `library_user:library_password` に統一

#### scripts/wait_for_db.py
- `urllib.parse.urlparse` による安全なURLパースに刷新
  （`?charset=utf8mb4` がDB名に混入する問題を解消）
- `DATABASE_URL` 未設定時の明示的な `sys.exit(1)` 追加
- `DB_MAX_RETRIES` / `DB_RETRY_INTERVAL` を環境変数で制御可能に変更
- `connect_timeout=5` によるハング防止を追加
- `if __name__ == "__main__":` によりモジュールとしてのimportも可能に変更

### 次回対応予定

- フェーズB 実装開始

## 2026-04-10 フェーズA-8・A-9 Alembic環境構築・バックエンド環境構築セッション

### 対応内容概要

フェーズA-8のAlembic環境構築・マイグレーションファイル作成、
およびフェーズA-9のバックエンド環境構築を実施した。
あわせてモデル定義のレビューと修正を行った。

### 作成・修正ファイル

| ファイル | 内容 |
|---------|------|
| `backend/alembic.ini` | sqlalchemy.url を正しい接続先に設定 |
| `backend/alembic/env.py` | 全モデルファイルをimport・metadata登録・DATABASE_URL上書き対応 |
| `backend/alembic/versions/001_initial_.py` | 全7テーブルの初期マイグレーション（token_hash=String(64)） |
| `backend/app/models/base.py` | declarative_base のみ定義 |
| `backend/app/models/` 各ファイル | モデルをファイル分割（school / user / book / loan / reservation / inter_library / password_reset_token） |
| `backend/app/models/user.py` | loans・reservations・inter_library_requests に foreign_keys 追加、password_reset_tokens に cascade="all, delete-orphan" 設定 |
| `backend/app/models/password_reset_token.py` | relationship復活（cascade は user.py 側に移動済み） |
| `backend/app/db.py` | エンジン・SessionLocal・get_db() 定義 |
| `backend/requirements.txt` | 全依存パッケージ定義 |
| `mysql/seed.sql` | 初期データ（5校・管理者・司書・テスト生徒） |
| `scripts/seed_users.py` | Argon2ハッシュ生成・seed.sql投入スクリプト |
| `scripts/wait_for_db.py` | DB起動待機スクリプト |

### 次回対応予定（未完了事項）

| 項目 | 内容 |
|------|------|
| users.md のパス記法修正 | 絶対パスを相対パスに統一 |
| auth_session.md の401フロー図整形 | フロー図形式に修正 |
| UC-28 貸出延長の設計確定 | 延長回数上限・延長期間・操作画面・権限確定後、各ドキュメントに反映 |

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



## 2026-04-10 フェーズA-7 Docker環境構築・ドキュメント整理セッション

---

### 対応内容概要

フェーズA-7のDocker環境構築ファイルを一式作成した。
あわせて課題1・課題2の分離方針に基づきドキュメントを整理した。

---

### 作成ファイル（Docker環境構築）

| ファイル | 内容 |
|---------|------|
| `docker-compose.yml` | 共通サービス定義 |
| `docker-compose.dev.yml` | 開発環境設定（ホットリロード・ポート公開） |
| `docker-compose.prod.yml` | 本番環境設定（nginx・ビルド） |
| `mysql/Dockerfile` | MySQL 8.0 |
| `mysql/conf.d/my.cnf` | utf8mb4_unicode_ci設定 |
| `backend/Dockerfile` | FastAPI用 |
| `backend/.env` | 開発用環境変数 |
| `backend/app/db.py` | SQLAlchemy DB接続設定 |
| `frontend/Dockerfile.dev` | Vue/Vite開発用 |
| `frontend/Dockerfile.prod` | マルチステージビルド |
| `frontend/nginx.conf` | Vue Router対応・APIプロキシ |
| `frontend/.env` | 開発環境変数 |
| `frontend/.env.production` | 本番環境変数（VITE_API_URL空） |
| `frontend/vite.config.ts` | usePolling・@エイリアス設定済み |
| `frontend/index.html` | エントリーHTML |
| `frontend/package.json` | 依存パッケージ定義 |
| `frontend/tsconfig*.json` | TypeScript設定 |
| `frontend/src/main.ts` | Pinia・Vue Router初期化 |
| `frontend/src/App.vue` | ルートコンポーネント |
| `frontend/src/router/index.ts` | ルーター基本構成 |
| `scripts/wait_for_db.py` | DB起動待機スクリプト |
| `.gitignore` | env・node_modules・db_data等を除外 |

**注意：** `npm create vite@latest`後に`npm install pinia vue-router axios`の実行が必要

---

### ドキュメント整理（課題1・課題2の分離）

#### functions.md
- 課題2機能候補セクション（F-EX01〜F-EX07）を削除

#### role_matrix.md
- 補足ルールから課題2に関する記述を削除
  - `is_committee`フラグの権限テーブル移行に関するコメント
  - 管理者アカウント管理画面の課題2での検討に関するコメント

#### docs/memo/phase2_ideas.md（新規作成）
- functions.mdの課題2機能候補を移動
- role_matrix.mdの課題2改善提案を移動

---

### 次回対応予定（未完了事項）

| 項目 | 内容 |
|------|------|
| フェーズA-8 | Alembic環境構築・マイグレーションファイル作成 |
| フェーズA-9 | `requirements.txt`作成 |
| 貸出延長（UC-28）設計確定 | 延長回数上限・延長期間・操作画面・権限を確認後、各ドキュメントに反映 |
| users.mdのパス記法修正 | 絶対パスを相対パスに統一 |
| auth_session.mdの401フロー図整形 | フロー図形式に修正 |



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
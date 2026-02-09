# Backend Changelog

## 2026/02/06
### Changed
- ログインレスポンス設計を整理し、教師ユーザー向けに以下の情報構造を明確化
  - 教師の全割当情報（ teacher_assignments ）
  - 一覧表示用の代表割当（ primary_assignment ）を分離
- `LoginResponse` / `AdminUserListResponse` に `primary_assignment` を追加し、一覧表示用と詳細編集用の責務を分離
- 教師割当の代表選択ロジックを `resolve_teacher_primary_assignment` に集約し、ロール判定や表示ロジックの重複を解消

### Fixed
- 教師ログイン時に発生していた
  `AttributeError: 'tuple' object has no attribute 'assignment_type'` を修正
- 割当取得処理を TeacherAssignmentSummary に統一
- 割当未存在時の空配列処理を追加

### Refactored
- 教師割当データ整形を `service` 層に集約
- `login_user` を単純なパイプライン構造に整理


## 2026/02/05
### Changed
- 管理者向けユーザー一覧取得ロジックを再設計
  - 教師の複数割当（担任・学年主任・教科担当など）に対応
  - DB の結合結果を user_id 単位で集約する `aggregate_admin_user_rows()` を追加
  - 教師割当を一覧表示用データと内部判断用データに分離

- 教師割当の責務分離を実施
  - `TeacherAssignmentSummary`: 教師が持つ各割当の事実データ（複数件）を表現
  - `UserPrimaryAssignment`: 複数割当の中から優先度に基づき代表1件を決定する表示・判定用モデル
  - 一覧表示・権限制御でのロジック簡略化を実現

- 教師の代表割当決定ロジックを service 層に集約
  - `resolve_teacher_primary_assignment()` を追加
  - 割当種別・主担当フラグに基づく優先順位ルールを明示化
  - フロントエンド側に割当解釈ロジックを持たせない設計に変更

- `AdminUserListResponse` のレスポンス構造を拡張
  - `primary_assignment` を追加し、ユーザー一覧での役割表示を安定化
  - `teacher_assignments` は詳細・管理用途として保持
  - 生徒・教師・管理者でレスポンス構造が破綻しないよう条件分岐を整理

### Fixed
- outer join 結果における `None` 値を考慮したデータ構築処理を改善
  - クラス未紐付けの教師割当でも Pydantic バリデーションエラーが発生しないよう調整
  
## 2026/02/04
### Added
- `scripts/create_journal_via_api.py` を追加
- `backend/requirements.txt` に `requests>=2.31.0` を追加

### Changed
- ログイン時のユーザー情報取得仕様を調整
  - 生徒：現在の学年・クラスを返却
  - 教師：`teacher_assignments` を基に担当情報を返却

### Design
- `teacher_assignments` は常に list として扱う設計に統一

### Infrastructure
- `docker-compose.dev.yml` を更新
  - 開発環境で `scripts/` をコンテナから参照可能にするため volume を追加

## 2026/02/03
### Changed
- 開発環境におけるデータ投入方針を整理
  - テーブル定義・マスタ構造とテストデータを分離する方針を明確化
  - `seed.sql` は「DB初期化に必要な最小構成」に限定
  - 日付依存・増加前提のデータは `seed.sql` に含めない方針とした

- `seed.sql` を修正
  - DB 再作成前提とし、`DELETE文` を削除
  - `subjects` の登録はマイグレーション側で管理する前提に変更
  - 学年・クラス・ユーザー・教師割当・生徒割当の初期サンプルデータ構成を整理

### Fixed
- `teacher_assignments` 登録時に `grade_id` が `NULL` になる問題を修正
  - `class_id` から `grade_id` を明示的に取得する形に修正
  - 担任・教科担当・学年主任それぞれの割当構造を ER 図 と整合させた

## 2026/02/02
### Changed
- `__init__.py` をすべて空ファイルに変更
  - モジュール再 export による循環 import を防止するため、明示的 import のみに統一

- 認証関連の責務分離を実施
  - `routers/auth.py` からビジネスロジックを分離し、`services/auth_service.py` に集約
  - 認証依存関係（ログインユーザー取得・トークン検証）を `dependencies/` 配下へ分離
  - 共通処理を `utils/` 配下へ整理

- トークン関連処理の再構成
  - `dependencies.py` を廃止し、トークン処理を新規作成した `utils/token_utils.py` に統合
  - トークン生成・検証ロジックを一元管理する構成へ変更

## 2026/02/01
### Changed
- 認証初期化処理（initAuth）の設計を改善
  - アプリ起動時のアクセストークンリフレッシュ処理を整理
  - 未ログイン状態では refresh API の失敗をエラーとして扱わないように変更
  - 認証状態に応じた初期化フローを明確化

- 管理者向けユーザー一覧取得処理（get_admin_user_list）の内部構造を整理
  - ユーザー単位での集約処理を関数化し、SQL結果の責務を明確化
  - 教師ロール判定（担任・副担任・学年主任等）の業務ロジックを分離
  - 表示用レスポンス生成処理を切り出し、可読性・保守性を向上

## 2026/01/26
### Changed
- 認証方式を interceptor 中心に変更
- `refresh token` を `HttpOnly Cookie` 管理に移行


## 2026/01/24
### Changed
- 認証処理を interceptor による 401 ハンドリング中心の構成へ移行
  ※ docs/design/auth-design.md を参照

## 2026/01/23
### Changed
- 教師の担当情報管理ロジック改善に伴い、関連モデルを更新
  - 教師・学年・クラス・教科の関係を明確化
  - DBスキーマ変更に対応するため `/models/user.py` `/models/class_model.py` を修正

## 2026/01/20
### Changed
- `get_admin_user_list` API のユーザー一覧取得ロジックを修正
  - 教師の `role` を `assignment_type` に基づき担任、副担任、学年主任、教科担当などに変換して返すよう変更
- `AdminUserListResponse` スキーマの `role` フィールドを `str` に修正


## 2026/01/16
### Changed
- `auth_service.py` を更新し、アクセストークンおよびリフレッシュトークンを発行
- 認証ルーター（`auth.py`）を更新
  - ログイン時に refresh_token を HttpOnly Cookie に設定
  - ログアウト時に refresh_token Cookie を削除
- `user.py`（ユーザーモデル）関連を更新
  - リフレッシュトークン対応に伴うアクセストークン生成ロジックを修正

## 2026/01/07
### Changed
- 再びPython 3.12 環境において passlib + bcrypt の組み合わせで発生していた認証エラーを確認したため修正
  - ハッシュ化を bcrypt から argon2 に変更

## 2026/01/06
### Changed
- 仮想環境の作成方法を `python -m venv venv` から `uv venv .venv` に変更


## 2025/12/24
### Changed
- `requirements.txt` を重複や不足を確認したため、更新
- ターミナルからのログイン認証が成功しないため、パスワードハッシュおよび認証処理の調査を実施中。

### Fixed
- Python 3.12 環境において passlib + bcrypt の組み合わせで発生していた認証エラーを修正
- Python バージョンを 3.11 に変更
- bcrypt を 3.2.2、passlib を 1.7.4 に固定し、互換性問題を解消

## 2025/12/23

### Changed
- `email-validator` の導入時のエラーを対処
  - `pip install email-validator` の再実行で解決
- Pydantic モデルを集約し、import を簡潔にしつつ、パッケージの公開インターフェースを明確にするため、`app/` 配下にある `__init__.py` を全て更新
- `models` 配下の `journal.py` `user.py` を更新、 `class_model.py` を作成
- `schemas` 配下の `journal.py` `user.py` を更新
- `routers` 配下の `journal.py` `user.py` を更新、 `teachers.py` `users.py` を作成
- `services` 配下の `journal_service.py` `user_service.py` を更新、 `teacher_service.py` `user_service.py` を作成
- `app` 配下の `db.py` `dependencies.py` `main.py` を更新

## 2025/12/22
### Added
- 初期 admin アカウント登録のため、 `4cd0c6be197e_add_initial_admin_user.py` を作成の上、反映
- `init.sql` にて作成した `renrakucho_db` を削除
- admin アカウント情報 メールアドレス:`admin@school.ac.jp` パスワード: `password123`
- `models` 配下に `journal.py` `user.py` を作成
- `schemas` 配下に `journal.py` `user.py` を作成
- `routers` 配下に `journal.py` `user.py` を作成
- `services` 配下に `journal_service.py` `user_service.py` を作成
- `app` 配下に `db.py` `dependencies.py` を作成、`main.py` を更新
- `email-validator` の導入を開始
  - 12/22 現在、以下のエラーが表示される状態で原因調査中
    ImportError: email-validator is not installed, run `pip install pydantic[email]`

## 2025/12/20
### Added
- FastAPI をベースとしたバックエンド初期構成を作成
- `app/` 配下に以下のレイヤ構造を定義
  - `models`：ORM モデル管理用ディレクトリ
  - `schemas`：Pydantic スキーマ管理用ディレクトリ
  - `routers`：API ルーティング管理用ディレクトリ
  - `services`：ビジネスロジック分離用ディレクトリ
- DB 接続管理用 `db.py` を追加
- アプリケーションエントリポイントとして `main.py` を追加
- Python 仮想環境（venv）および `requirements.txt` を導入

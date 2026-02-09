# Database Changelog

## 2026/01/26
### Migration
- Alembic マイグレーション `d29c0dfc9e24` を作成・実行
  - `subjects` テーブルに初期教科データを登録
    - 国語、社会、数学、理科、音楽、美術、保健体育、技術・家庭、英語
  - 既存データが存在する場合も安全に挿入（`INSERT IGNORE` 使用）
  - `downgrade` 実行時には該当データを削除

## 2026/01/22
### Migration
- `subjects` テーブル追加
- `teacher_assignments` の教科管理方式変更
  - 詳細は `docs/design/teacher-assignment-design.md` を参照

## 2026/01/21
### Changed
- classes 初期データ登録処理における文字化けを修正

## 2026/01/16
### Fixed
- MySQLコンテナの文字コード設定を修正
  - PowerShell の `Get-Content` で UTF-8 BOM付き出力した場合の文字化けを回避
  - 初期データ投入コマンド：
```cmd
    docker compose exec -T db mysql -u root -proot --default-character-set=utf8mb4 journal_system < seed.sql
```

## 2026/01/15
## Changed
- init.sql とマイグレーションの役割を整理し、テーブル定義の重複を解消
- テストデータ投入専用として seed.sql を新規作成
- 表記上の問題で ER図.pdf を削除、er_diagram.mmd に変更

### Fixed
- seed.sql 実行時に発生していた外部キー制約エラーを修正
- AUTO_INCREMENT ID の直指定を廃止し、サブクエリによる参照方式に変更
- MySQLコンテナの文字コード設定を修正
  - seed.sql実行時の文字化けを解消するため、MySQL設定ファイル(my.cnf)でutf8mb4を指定
  - `mysql/Dockerfile`と`mysql/conf.d/my.cnf`を新規作成
  - `docker-compose.yml`のdbサービスをbuild方式に変更

## 2025/12/20
### Added
- Alembic を導入し、データベーススキーマのマイグレーション管理を開始
- DB 初期化用 `init.sql` を追加
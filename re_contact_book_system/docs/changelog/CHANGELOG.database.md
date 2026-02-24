# Database Changelog

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
## 2026/02/24

### Fixed
- `001_initial_schema.py`
  - `subjects` テーブルに `created_at` カラムを追加（他テーブルとの統一）

### Changed
- `seed.sql`
  - `CREATE DATABASE` 文を削除（役割の境界を整理）
  - `grades` の年度を固定値（`2025`）から `YEAR(CURDATE())` による自動取得に変更
  - `grades` の INSERT を `ON DUPLICATE KEY UPDATE` 付きの形式に変更

- `docs/er_diagram.mmd`
  - `teacher_assignments.assignment_type` から `administrator` を削除
    （`homeroom / subject / grade_head` の3値に修正）
    
## 2026/02/10
### Changed
- 教師の担当情報設計を整理し、`teacher_assignments.assignment_type` から `administrator` を削除
  - 管理者権限は `users.role = admin` に集約
  - ※ 既存データがある場合は migration 実行前に該当値の洗い替えが必要

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
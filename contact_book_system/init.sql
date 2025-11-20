-- ============================================
-- 連絡帳管理システム - データベース初期化スクリプト
-- ============================================
-- 説明: Ubuntu環境でのMySQL構築用init.sql
-- 実行順序: 1. データベース作成 2. テーブル作成 3. 初期データ投入
-- ============================================
-- ============================================
-- 文字コード設定（最重要）
-- ============================================
-- SET NAMES 'utf8mb4';
-- SET CHARACTER SET utf8mb4;
-- SET collation_connection = 'utf8mb4_unicode_ci';

USE renrakucho_db;

CREATE EVENT IF NOT EXISTS yearly_delete_expired_renrakucho
ON SCHEDULE EVERY 1 YEAR
STARTS '2026-04-01 03:00:00'
COMMENT 'Yearly deletion of expired renrakucho entries (5+ years)'
DO
    CALL delete_expired_renrakucho(5);

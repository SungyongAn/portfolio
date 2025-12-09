-- ============================================
-- 連絡帳管理システム - データベース初期化スクリプト
-- ============================================
-- 説明: Ubuntu環境でのMySQL構築用init.sql
-- 実行順序: 1. データベース作成 2. テーブル作成 3. 初期データ投入
-- ============================================
-- ============================================
-- 文字コード設定（最重要）
-- ============================================
SET NAMES 'utf8mb4';
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

-- ============================================
-- データベース作成
-- ============================================
CREATE DATABASE IF NOT EXISTS renrakucho_db 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE renrakucho_db;

-- USE 後に文字コード再設定
SET NAMES 'utf8mb4';
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

-- ============================================
-- テーブル定義
-- ============================================

-- 教員区分マスタテーブル
CREATE TABLE IF NOT EXISTS teacher_roles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '教員区分ID',
    code VARCHAR(50) NOT NULL COMMENT '役職コード',
    name VARCHAR(50) NOT NULL COMMENT '役職名',
    description TEXT COMMENT '説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教員区分マスタ';

-- 科目マスタテーブル
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '科目ID',
    code VARCHAR(50) NOT NULL COMMENT '教科コード',
    name VARCHAR(50) NOT NULL COMMENT '教科名'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='科目マスタ';

-- アカウントテーブル
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'アカウントID',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT 'メールアドレス（ログインID）',
    last_name VARCHAR(50) NOT NULL COMMENT '姓',
    first_name VARCHAR(50) NOT NULL COMMENT '名',
    password VARCHAR(255) NOT NULL COMMENT 'パスワード（bcryptハッシュ化）',
    role ENUM('admin', 'teacher', 'student', 'school_nurse') NOT NULL DEFAULT 'student' COMMENT 'アカウント種別',
    status ENUM('enrolled', 'graduated', 'transferred', 'on_leave', 'other') NOT NULL DEFAULT 'enrolled' COMMENT '在籍状況',
    grade INT NOT NULL COMMENT '学年（1-3、教師は0）',
    class_name VARCHAR(10) NOT NULL COMMENT 'クラス（A/B/C、教師は0）',
    enrollment_year INT NOT NULL COMMENT '入学年または採用年',
    graduation_year INT NULL COMMENT '卒業予定年（教師はNULL）',
    teacher_role_id INT NULL COMMENT '教員区分ID（教師のみ）',
    subject_id INT NULL COMMENT '担当教科ID（教師のみ）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',

    FOREIGN KEY (teacher_role_id) REFERENCES teacher_roles(id) ON DELETE SET NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci 
COMMENT='アカウント情報';

-- 連絡帳エントリーテーブル
CREATE TABLE IF NOT EXISTS renrakucho_entries (
    renrakucho_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '連絡帳ID',
    student_id INT NOT NULL COMMENT '生徒ID',
    submitted_date DATE NOT NULL COMMENT '提出日',
    target_date DATE NOT NULL COMMENT '対象日',
    physical_condition TINYINT NOT NULL COMMENT '体調（1-5）',
    mental_state TINYINT NOT NULL COMMENT 'メンタル（1-5）',
    physical_mental_notes TEXT COMMENT '体調・メンタルメモ',
    daily_reflection TEXT NOT NULL COMMENT '1日の振り返り',
    is_read BOOLEAN NOT NULL DEFAULT FALSE COMMENT '既読フラグ',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    FOREIGN KEY (student_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='連絡帳エントリー';

-- チャットルームテーブル
CREATE TABLE IF NOT EXISTS chat_rooms (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ルームID',
    name VARCHAR(100) NOT NULL COMMENT 'ルーム名',
    description TEXT COMMENT 'ルームの説明',
    creator_id INT NOT NULL COMMENT '作成者ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    FOREIGN KEY (creator_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='チャットルーム';

-- チャット参加者テーブル
CREATE TABLE IF NOT EXISTS chat_participants (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '参加者ID',
    room_id INT NOT NULL COMMENT 'ルームID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '参加日時',
    FOREIGN KEY (room_id) REFERENCES chat_rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='チャット参加者';

-- チャットメッセージテーブル
CREATE TABLE IF NOT EXISTS chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'メッセージID',
    room_id INT NOT NULL COMMENT 'ルームID',
    sender_id INT NOT NULL COMMENT '送信者ID',
    message TEXT NOT NULL COMMENT 'メッセージ本文',
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '送信日時',
    FOREIGN KEY (room_id) REFERENCES chat_rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='チャットメッセージ';

-- チャット既読状態テーブル
CREATE TABLE IF NOT EXISTS chat_read_status (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '既読ID',
    message_id INT NOT NULL COMMENT 'メッセージID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    read_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '既読日時',
    FOREIGN KEY (message_id) REFERENCES chat_messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='チャット既読状態';

-- ============================================
-- 初期データ投入
-- ============================================

-- 既存データのクリア（必要に応じてコメントアウト）
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE chat_read_status;
TRUNCATE TABLE chat_messages;
TRUNCATE TABLE chat_participants;
TRUNCATE TABLE chat_rooms;
TRUNCATE TABLE renrakucho_entries;
TRUNCATE TABLE accounts;
TRUNCATE TABLE teacher_roles;
TRUNCATE TABLE subjects;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 1. マスタデータ投入
-- ============================================

-- 教員区分マスタ
INSERT INTO teacher_roles (id, code, name, description) VALUES
(1, 'homeroom_teacher', '担任', 'クラス担任'),
(2, 'assistant_teacher', '副担任', 'クラス副担任'),
(3, 'subject_teacher', '教科担当', '教科のみ担当'),
(4, 'grade_leader', '学年主任', '学年全体の統括責任者');

-- 科目マスタ
INSERT INTO subjects (id, code, name) VALUES
(1, 'Japanese', '国語'),
(2, 'Mathematics', '数学'),
(3, 'English', '英語'),
(4, 'Science', '理科'),
(5, 'SocialStudies', '社会'),
(6, 'PE', '保健体育'),
(7, 'Music', '音楽'),
(8, 'Art', '美術'),
(9, 'TechnologyHomeEconomics', '技術・家庭');

-- 連絡帳のアーカイブテーブルを作成
CREATE TABLE renrakucho_entries_archive (
    renrakucho_id INT NOT NULL COMMENT '連絡帳ID',
    student_id INT NOT NULL COMMENT '生徒ID',
    submitted_date DATE NOT NULL COMMENT '提出日',
    target_date DATE NOT NULL COMMENT '対象日',
    physical_condition TINYINT NOT NULL COMMENT '体調（1-5）',
    mental_state TINYINT NOT NULL COMMENT 'メンタル（1-5）',
    physical_mental_notes TEXT DEFAULT NULL COMMENT '体調・メンタルメモ',
    daily_reflection TEXT NOT NULL COMMENT '1日の振り返り',
    is_read BOOLEAN NOT NULL COMMENT '既読フラグ',
    created_at DATETIME NOT NULL COMMENT '作成日時',
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'アーカイブ日時',
    
    PRIMARY KEY (renrakucho_id, target_date),
    INDEX idx_student_id (student_id),
    INDEX idx_target_date (target_date),
    INDEX idx_archived_at (archived_at)
) ENGINE=InnoDB 
  ROW_FORMAT=COMPRESSED 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='アーカイブされた連絡帳データ（3-5年分）';


-- 連絡帳の削除ログテーブルを作成
CREATE TABLE data_deletion_log (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ログID',
    deletion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '削除実行日時',
    table_name VARCHAR(100) NOT NULL COMMENT '対象テーブル名',
    records_deleted INT NOT NULL COMMENT '削除件数',
    date_range_from DATE COMMENT '削除対象期間（開始）',
    date_range_to DATE COMMENT '削除対象期間（終了）',
    reason VARCHAR(255) COMMENT '削除理由',
    executed_by VARCHAR(100) DEFAULT 'SYSTEM' COMMENT '実行者',
    backup_file VARCHAR(255) COMMENT 'バックアップファイル名',
    
    INDEX idx_deletion_date (deletion_date),
    INDEX idx_table_name (table_name)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='データ削除の監査ログ';



DELIMITER $$
-- アーカイブプロシージャ
CREATE PROCEDURE archive_old_renrakucho(
    IN archive_years INT
)
BEGIN
    DECLARE archive_date DATE;
    DECLARE affected_rows INT DEFAULT 0;
    DECLARE exit_handler_called BOOLEAN DEFAULT FALSE;
    
    -- エラーハンドラー
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET exit_handler_called = TRUE;
        ROLLBACK;
    END;
    
    -- アーカイブ対象日を計算（デフォルト: 3年前）
    IF archive_years IS NULL OR archive_years < 1 THEN
        SET archive_years = 3;
    END IF;
    
    SET archive_date = DATE_SUB(CURDATE(), INTERVAL archive_years YEAR);
    
    -- トランザクション開始
    START TRANSACTION;
    
    -- アーカイブテーブルに挿入（重複を避けるためNOT EXISTS使用）
    INSERT INTO renrakucho_entries_archive 
        (renrakucho_id, student_id, submitted_date, target_date, 
         physical_condition, mental_state, physical_mental_notes, 
         daily_reflection, is_read, created_at)
    SELECT 
        r.renrakucho_id, 
        r.student_id, 
        r.submitted_date, 
        r.target_date,
        r.physical_condition, 
        r.mental_state, 
        r.physical_mental_notes,
        r.daily_reflection, 
        r.is_read, 
        r.created_at
    FROM renrakucho_entries r
    WHERE r.target_date < archive_date
    AND NOT EXISTS (
        SELECT 1 
        FROM renrakucho_entries_archive a 
        WHERE a.renrakucho_id = r.renrakucho_id
    );
    
    SET affected_rows = ROW_COUNT();
    
    -- 元のテーブルから削除
    DELETE FROM renrakucho_entries
    WHERE target_date < archive_date;
    
    -- エラーチェック
    IF exit_handler_called THEN
        SELECT 
            FALSE AS success,
            'Archive failed due to error' AS message,
            0 AS records_archived;
    ELSE
        -- コミット
        COMMIT;
        
        -- 結果を返す
        SELECT 
            TRUE AS success,
            CONCAT('Successfully archived records before ', archive_date) AS message,
            affected_rows AS records_archived,
            archive_date AS cutoff_date;
    END IF;
    
END$$

-- 削除プロシージャ
CREATE PROCEDURE delete_expired_renrakucho(
    IN retention_years INT
)
BEGIN
    DECLARE delete_date DATE;
    DECLARE deleted_count INT DEFAULT 0;
    DECLARE backup_filename VARCHAR(255);
    DECLARE exit_handler_called BOOLEAN DEFAULT FALSE;
    
    -- エラーハンドラー
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET exit_handler_called = TRUE;
        ROLLBACK;
    END;
    
    -- 保管期間を計算（デフォルト: 5年）
    IF retention_years IS NULL OR retention_years < 1 THEN
        SET retention_years = 5;
    END IF;
    
    SET delete_date = DATE_SUB(CURDATE(), INTERVAL retention_years YEAR);
    SET backup_filename = CONCAT('archive_before_', delete_date, '_', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s'), '.sql.gz');
    
    -- トランザクション開始
    START TRANSACTION;
    
    -- アーカイブテーブルから削除（削除前にカウント）
    SELECT COUNT(*) INTO deleted_count
    FROM renrakucho_entries_archive
    WHERE target_date < delete_date;
    
    -- 実際に削除
    DELETE FROM renrakucho_entries_archive
    WHERE target_date < delete_date;
    
    -- 削除ログを記録
    INSERT INTO data_deletion_log 
        (table_name, records_deleted, date_range_to, reason, backup_file)
    VALUES (
        'renrakucho_entries_archive',
        deleted_count,
        delete_date,
        CONCAT(retention_years, ' years retention policy'),
        backup_filename
    );
    
    -- エラーチェック
    IF exit_handler_called THEN
        SELECT 
            FALSE AS success,
            'Deletion failed due to error' AS message,
            0 AS records_deleted;
    ELSE
        -- コミット
        COMMIT;
        
        -- 結果を返す
        SELECT 
            TRUE AS success,
            CONCAT('Successfully deleted records before ', delete_date) AS message,
            deleted_count AS records_deleted,
            delete_date AS cutoff_date,
            backup_filename AS backup_file;
    END IF;
    
END$$

-- データ統計取得プロシージャ（管理画面用）
CREATE PROCEDURE get_archive_statistics()
BEGIN
    -- アクティブデータの統計
    SELECT
        'active' AS data_type,
        COUNT(*) AS record_count,
        MIN(target_date) AS oldest_date,
        MAX(target_date) AS newest_date,
        ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS size_mb
    FROM renrakucho_entries
    JOIN information_schema.TABLES 
        ON TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'renrakucho_entries'
        
    
    UNION ALL
    
    -- アーカイブデータの統計
    SELECT 
        'archive' AS data_type,
        COUNT(*) AS record_count,
        MIN(target_date) AS oldest_date,
        MAX(target_date) AS newest_date,
        ROUND(
            (DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2
        ) AS size_mb
    FROM renrakucho_entries_archive
    JOIN information_schema.TABLES 
        ON TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'renrakucho_entries_archive';


-- 毎年4月1日 午前2時にアーカイブを実行
CREATE EVENT IF NOT EXISTS yearly_archive_renrakucho
ON SCHEDULE EVERY 1 YEAR
STARTS '2026-04-01 02:00:00'
COMMENT 'Yearly archiving of old renrakucho entries (3+ years)'
DO
    CALL archive_old_renrakucho(3);


-- 毎年4月1日 午前3時に削除を実行（アーカイブの1時間後）
CREATE EVENT IF NOT EXISTS yearly_delete_expired_renrakucho
ON SCHEDULE EVERY 1 YEAR
STARTS '2026-04-01 03:00:00'
COMMENT 'Yearly deletion of expired renrakucho entries (5+ years)'
DO
    CALL delete_expired_renrakucho(5);


-- 毎年4月1日 午前1時に3年のstatusを卒業に変更、他生徒の学年を＋1
CREATE EVENT promote_students
ON SCHEDULE EVERY 1 YEAR
    STARTS '2025-04-01 01:00:00'
DO
BEGIN
    -- 1. 元の3年生を卒業扱いにする（学生のみ）
    UPDATE accounts 
        SET status = 'graduated'
        WHERE role = 'student' 
          AND grade = 3;

    -- 2. 1〜2年の学生のみ進級させる
    UPDATE accounts
        SET grade = grade + 1
        WHERE role = 'student'
          AND grade < 3;

END$$

DELIMITER ;

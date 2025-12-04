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
    name VARCHAR(100) NOT NULL COMMENT '氏名',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='アカウント情報';

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
(1, 'homeroom', '担任', 'クラス担任'),
(2, 'assistant_homeroom', '副担任', 'クラス副担任'),
(3, 'subject_teacher', '教科担当', '教科のみ担当'),
(4, 'grade_leader', '学年主任', '学年全体の統括責任者');

-- 科目マスタ
INSERT INTO subjects (id, code, name) VALUES
(1, 'japanese', '国語'),
(2, 'math', '数学'),
(3, 'english', '英語'),
(4, 'science', '理科'),
(5, 'social', '社会'),
(6, 'pe', '体育'),
(7, 'music', '音楽'),
(8, 'art', '美術'),
(9, 'tech', '技術'),
(10, 'home_ec', '家庭科');


CREATE EVENT IF NOT EXISTS yearly_delete_expired_renrakucho
ON SCHEDULE EVERY 1 YEAR
STARTS '2026-04-01 03:00:00'
COMMENT 'Yearly deletion of expired renrakucho entries (5+ years)'
DO
    CALL delete_expired_renrakucho(5);

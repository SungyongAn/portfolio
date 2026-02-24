-- ====================================
-- 連絡帳管理システム データベース初期化
-- ====================================

-- データベースの作成（既に存在する場合はスキップ）
CREATE DATABASE IF NOT EXISTS journal_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE journal_system;

-- 既存テーブルの削除（開発用：本番では注意）
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS teacher_notes;
DROP TABLE IF EXISTS journal_entries;
DROP TABLE IF EXISTS teacher_assignments;
DROP TABLE IF EXISTS student_class_assignments;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- ====================================
-- 1. ユーザーテーブル
-- ====================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE COMMENT 'ログイン用メールアドレス',
    password_hash VARCHAR(255) NOT NULL COMMENT 'ハッシュ化されたパスワード',
    role ENUM('student', 'teacher', 'admin') NOT NULL COMMENT 'ユーザーロール',
    name VARCHAR(100) NOT NULL COMMENT '氏名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザー（生徒・教師・管理者）';

-- ====================================
-- 2. 学年テーブル
-- ====================================
CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grade_number INT NOT NULL COMMENT '学年番号（1,2,3）',
    year INT NOT NULL COMMENT '年度（2025,2026...）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_grade_year (grade_number, year),
    INDEX idx_year (year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学年';

-- ====================================
-- 3. クラステーブル
-- ====================================
CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grade_id INT NOT NULL COMMENT '学年ID',
    class_name VARCHAR(50) NOT NULL COMMENT 'クラス名（A組,B組）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grade_id) REFERENCES grades(id) ON DELETE CASCADE,
    UNIQUE KEY uk_grade_class (grade_id, class_name),
    INDEX idx_grade_id (grade_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='クラス';

-- ====================================
-- 4. 生徒クラス割当テーブル
-- ====================================
CREATE TABLE student_class_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL COMMENT '生徒ID',
    class_id INT NOT NULL COMMENT 'クラスID',
    is_current BOOLEAN DEFAULT TRUE COMMENT '現在のクラスか',
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '割当日時',
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    INDEX idx_student_id (student_id),
    INDEX idx_class_id (class_id),
    INDEX idx_is_current (is_current)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='生徒クラス割当';

-- ====================================
-- 5. 教師割当テーブル
-- ====================================
CREATE TABLE teacher_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL COMMENT '教師ID',
    assignment_type ENUM('homeroom', 'subject', 'grade_head', 'administrator') NOT NULL COMMENT '割当種別',
    grade_id INT NULL COMMENT '学年ID（学年主任・教科担当の場合）',
    class_id INT NULL COMMENT 'クラスID（担任の場合）',
    subject_name VARCHAR(50) NULL COMMENT '教科名（教科担当の場合）',
    is_primary BOOLEAN DEFAULT FALSE COMMENT '主担任フラグ',
    permission_level ENUM('read', 'write', 'admin') DEFAULT 'read' COMMENT '権限レベル',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (grade_id) REFERENCES grades(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    INDEX idx_teacher_id (teacher_id),
    INDEX idx_assignment_type (assignment_type),
    INDEX idx_class_id (class_id),
    INDEX idx_grade_id (grade_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教師割当';

-- ====================================
-- 6. 連絡帳エントリテーブル
-- ====================================
CREATE TABLE journal_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL COMMENT '生徒ID',
    entry_date DATE NOT NULL COMMENT '記入対象日（前登校日）',
    submission_date DATE NOT NULL COMMENT '提出日',
    physical_condition VARCHAR(50) NOT NULL COMMENT '体調（よかった/ふつう/疲れ気味/悪い）',
    mental_condition VARCHAR(50) NOT NULL COMMENT 'メンタル（元気/ふつう/落ち込んでいる）',
    reflection_text TEXT COMMENT '振り返り内容',
    is_read BOOLEAN DEFAULT FALSE COMMENT '既読フラグ',
    read_by INT NULL COMMENT '既読した教師ID',
    read_at TIMESTAMP NULL COMMENT '既読日時',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (read_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_student_id (student_id),
    INDEX idx_entry_date (entry_date),
    INDEX idx_submission_date (submission_date),
    INDEX idx_is_read (is_read),
    INDEX idx_read_by (read_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='連絡帳エントリ';

-- ====================================
-- 7. 教師メモテーブル（課題2用）
-- ====================================
CREATE TABLE teacher_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL COMMENT '作成教師ID',
    student_id INT NOT NULL COMMENT '対象生徒ID',
    entry_id INT NULL COMMENT '関連連絡帳ID（任意）',
    note_text TEXT NOT NULL COMMENT 'メモ内容',
    is_shared BOOLEAN DEFAULT FALSE COMMENT '学年共有フラグ',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (entry_id) REFERENCES journal_entries(id) ON DELETE SET NULL,
    INDEX idx_teacher_id (teacher_id),
    INDEX idx_student_id (student_id),
    INDEX idx_entry_id (entry_id),
    INDEX idx_is_shared (is_shared),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教師メモ（学年会議用）';

-- ====================================
-- テストデータ投入
-- ====================================

-- パスワードハッシュの定義
-- 以下のハッシュ値はbcryptで生成されています
-- すべてのパスワードは "password123" です
-- 
-- 生成方法（Python）:
-- from passlib.context import CryptContext
-- pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
-- print(pwd_context.hash("password123"))

SET @admin_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oc2BdNpw5uze';
SET @teacher_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oc2BdNpw5uze';
SET @student_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oc2BdNpw5uze';

-- 管理者アカウント
INSERT INTO users (email, password_hash, role, name) VALUES
('admin@school.ac.jp', @admin_password, 'admin', 'システム管理者');

-- 学年・クラスの作成
INSERT INTO grades (grade_number, year) VALUES
(1, 2025),
(2, 2025),
(3, 2025);

INSERT INTO classes (grade_id, class_name) VALUES
(1, 'A組'),
(1, 'B組'),
(2, 'A組'),
(2, 'B組'),
(3, 'A組');

-- 教師アカウント
INSERT INTO users (email, password_hash, role, name) VALUES
('tanaka.teacher@school.ac.jp', @teacher_password, 'teacher', '田中 一郎'),
('suzuki.teacher@school.ac.jp', @teacher_password, 'teacher', '鈴木 次郎'),
('yamamoto.teacher@school.ac.jp', @teacher_password, 'teacher', '山本 三郎');

-- 教師割当
-- 田中先生: 1年A組 担任
INSERT INTO teacher_assignments (teacher_id, assignment_type, class_id, is_primary, permission_level) VALUES
((SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'), 'homeroom', 1, TRUE, 'write');

-- 鈴木先生: 1年B組 担任 & 学年主任
INSERT INTO teacher_assignments (teacher_id, assignment_type, class_id, is_primary, permission_level) VALUES
((SELECT id FROM users WHERE email = 'suzuki.teacher@school.ac.jp'), 'homeroom', 2, TRUE, 'write');

INSERT INTO teacher_assignments (teacher_id, assignment_type, grade_id, permission_level) VALUES
((SELECT id FROM users WHERE email = 'suzuki.teacher@school.ac.jp'), 'grade_head', 1, 'admin');

-- 山本先生: 数学教科担当（1年全体）
INSERT INTO teacher_assignments (teacher_id, assignment_type, grade_id, subject_name, permission_level) VALUES
((SELECT id FROM users WHERE email = 'yamamoto.teacher@school.ac.jp'), 'subject', 1, '数学', 'read');

-- 生徒アカウント（1年A組: 3名）
INSERT INTO users (email, password_hash, role, name) VALUES
('yamada.taro@school.ac.jp', @student_password, 'student', '山田 太郎'),
('sato.hanako@school.ac.jp', @student_password, 'student', '佐藤 花子'),
('tanaka.jiro@school.ac.jp', @student_password, 'student', '田中 次郎');

-- 1年B組: 2名
INSERT INTO users (email, password_hash, role, name) VALUES
('suzuki.ichiro@school.ac.jp', @student_password, 'student', '鈴木 一郎'),
('watanabe.yuki@school.ac.jp', @student_password, 'student', '渡辺 由紀');

-- 生徒クラス割当
INSERT INTO student_class_assignments (student_id, class_id, is_current) VALUES
((SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'), 1, TRUE),
((SELECT id FROM users WHERE email = 'sato.hanako@school.ac.jp'), 1, TRUE),
((SELECT id FROM users WHERE email = 'tanaka.jiro@school.ac.jp'), 1, TRUE),
((SELECT id FROM users WHERE email = 'suzuki.ichiro@school.ac.jp'), 2, TRUE),
((SELECT id FROM users WHERE email = 'watanabe.yuki@school.ac.jp'), 2, TRUE);

-- サンプル連絡帳エントリ（山田太郎）
INSERT INTO journal_entries (student_id, entry_date, submission_date, physical_condition, mental_condition, reflection_text, is_read, read_by, read_at) VALUES
((SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'), 
 '2025-04-07', '2025-04-08', 'よかった', '元気', 
 '数学の授業で二次関数を学んだ。完全に理解した。部活ではバッティング練習を中心に行った。', 
 TRUE, (SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'), '2025-04-08 16:30:00');

INSERT INTO journal_entries (student_id, entry_date, submission_date, physical_condition, mental_condition, reflection_text, is_read) VALUES
((SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'), 
 '2025-04-08', '2025-04-09', '疲れ気味', '元気', 
 '体育で頑張り過ぎて午後は眠かった。そろそろ運動会もあるのでダッシュの練習でもしようかな。', 
 FALSE);

-- サンプル連絡帳エントリ（佐藤花子）
INSERT INTO journal_entries (student_id, entry_date, submission_date, physical_condition, mental_condition, reflection_text, is_read, read_by, read_at) VALUES
((SELECT id FROM users WHERE email = 'sato.hanako@school.ac.jp'), 
 '2025-04-07', '2025-04-08', 'ふつう', 'ふつう', 
 '英語の授業で新しい文法を学んだ。少し難しかったけど、復習すれば大丈夫そう。', 
 TRUE, (SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'), '2025-04-08 16:45:00');

-- サンプル教師メモ
INSERT INTO teacher_notes (teacher_id, student_id, entry_id, note_text, is_shared) VALUES
((SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'),
 (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'),
 1,
 '数学の理解度が高い。次回のテストで好成績が期待できそう。',
 FALSE);

-- ====================================
-- 確認用クエリ
-- ====================================

-- テーブル一覧
SELECT 
    'テーブル作成完了' AS status,
    COUNT(*) AS table_count 
FROM information_schema.tables 
WHERE table_schema = 'journal_system';

-- ユーザー数確認
SELECT role, COUNT(*) AS count FROM users GROUP BY role;

-- クラス一覧
SELECT 
    g.grade_number AS 学年,
    c.class_name AS クラス,
    COUNT(sca.student_id) AS 生徒数
FROM classes c
JOIN grades g ON c.grade_id = g.id
LEFT JOIN student_class_assignments sca ON c.id = sca.class_id AND sca.is_current = TRUE
GROUP BY g.grade_number, c.class_name
ORDER BY g.grade_number, c.class_name;

-- ====================================
-- 完了メッセージ
-- ====================================
SELECT '
====================================
データベース初期化完了！

テストアカウント:
- 管理者: admin@school.ac.jp / password123
- 担任: tanaka.teacher@school.ac.jp / password123
- 生徒: yamada.taro@school.ac.jp / password123
====================================
' AS message;

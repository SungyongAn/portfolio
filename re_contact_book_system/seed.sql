-- ====================================
-- seed.sql（初期データ投入用・UTF-8対応）
-- ====================================

-- クライアント→サーバ間の文字コードを明示
SET NAMES 'utf8mb4';

-- データベース作成
CREATE DATABASE IF NOT EXISTS journal_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE journal_system;

-- ====================================
-- seed 再投入用：既存テストデータ削除
-- ====================================

SET FOREIGN_KEY_CHECKS = 0;

-- 教師メモ
DELETE FROM teacher_notes;

-- 連絡帳
DELETE FROM journal_entries;

-- 割当系
DELETE FROM student_class_assignments;
DELETE FROM teacher_assignments;

-- テスト用ユーザー（管理者は残す）
DELETE FROM users
WHERE role IN ('teacher', 'student')
  AND email LIKE '%@school.ac.jp';

SET FOREIGN_KEY_CHECKS = 1;

-- ====================================
-- テストデータ投入
-- ====================================

-- パスワードハッシュの定義
SET @teacher_password = '$argon2id$v=19$m=65536,t=3,p=4$n/P+P+d8r/V+7907x/j/fw$a8baIAcJW/o+HX5nCpoC9GjN5L1MeTDsDeXrKz+ZeYo';
SET @student_password = '$argon2id$v=19$m=65536,t=3,p=4$n/P+P+d8r/V+7907x/j/fw$a8baIAcJW/o+HX5nCpoC9GjN5L1MeTDsDeXrKz+ZeYo';

-- 学年・クラスの作成
INSERT IGNORE INTO grades (grade_number, year) VALUES
(1, 2025),
(2, 2025),
(3, 2025);

INSERT IGNORE INTO classes (grade_id, class_name) VALUES
((SELECT id FROM grades WHERE grade_number = 1 AND year = 2025), 'A組'),
((SELECT id FROM grades WHERE grade_number = 1 AND year = 2025), 'B組'),
((SELECT id FROM grades WHERE grade_number = 2 AND year = 2025), 'A組'),
((SELECT id FROM grades WHERE grade_number = 2 AND year = 2025), 'B組'),
((SELECT id FROM grades WHERE grade_number = 3 AND year = 2025), 'A組');

-- 教師アカウント
INSERT INTO users (email, password_hash, role, name) VALUES
('tanaka.teacher@school.ac.jp', @teacher_password, 'teacher', '田中 一郎'),
('suzuki.teacher@school.ac.jp', @teacher_password, 'teacher', '鈴木 次郎'),
('yamamoto.teacher@school.ac.jp', @teacher_password, 'teacher', '山本 三郎');

-- 教師割当
INSERT INTO teacher_assignments (teacher_id, assignment_type, class_id, is_primary, permission_level) VALUES
((SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'), 'homeroom', 1, TRUE, 'write');

INSERT INTO teacher_assignments (teacher_id, assignment_type, class_id, is_primary, permission_level) VALUES
((SELECT id FROM users WHERE email = 'suzuki.teacher@school.ac.jp'), 'homeroom', 2, TRUE, 'write');

INSERT INTO teacher_assignments (teacher_id, assignment_type, grade_id, permission_level) VALUES
((SELECT id FROM users WHERE email = 'suzuki.teacher@school.ac.jp'), 'grade_head', 1, 'admin');

INSERT INTO teacher_assignments (teacher_id, assignment_type, grade_id, subject_name, permission_level) VALUES
((SELECT id FROM users WHERE email = 'yamamoto.teacher@school.ac.jp'), 'subject', 1, '数学', 'read');

-- 生徒アカウント
INSERT INTO users (email, password_hash, role, name) VALUES
('yamada.taro@school.ac.jp', @student_password, 'student', '山田 太郎'),
('sato.hanako@school.ac.jp', @student_password, 'student', '佐藤 花子'),
('tanaka.jiro@school.ac.jp', @student_password, 'student', '田中 次郎'),
('suzuki.ichiro@school.ac.jp', @student_password, 'student', '鈴木 一郎'),
('watanabe.yuki@school.ac.jp', @student_password, 'student', '渡辺 由紀');

-- 生徒クラス割当
INSERT INTO student_class_assignments (student_id, class_id, is_current) VALUES
((SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'), 1, TRUE),
((SELECT id FROM users WHERE email = 'sato.hanako@school.ac.jp'), 1, TRUE),
((SELECT id FROM users WHERE email = 'tanaka.jiro@school.ac.jp'), 1, TRUE),
((SELECT id FROM users WHERE email = 'suzuki.ichiro@school.ac.jp'), 2, TRUE),
((SELECT id FROM users WHERE email = 'watanabe.yuki@school.ac.jp'), 2, TRUE);

-- サンプル連絡帳エントリ
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

-- サンプル教師メモ
INSERT INTO teacher_notes (teacher_id, student_id, entry_id, note_text, is_shared)
VALUES
(
  (SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'),
  (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'),
  (
    SELECT id
    FROM journal_entries
    WHERE student_id = (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp')
      AND entry_date = '2025-04-07'
    LIMIT 1
  ),
  '数学の理解度が高い。次回のテストで好成績が期待できそう。',
  FALSE
);

-- ====================================
-- 完了メッセージ（任意確認用）
-- ====================================
SELECT 'データベース初期化・テストデータ投入完了' AS message;

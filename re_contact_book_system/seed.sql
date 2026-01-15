-- ====================================
-- seed.sql（初期データ投入用）
-- ====================================

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
-- 以下のハッシュ値はargon2で生成されています
-- すべてのパスワードは "password123" です

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

-- -- ====================================
-- -- 確認用クエリ
-- -- ====================================

-- -- テーブル一覧
-- SELECT 
--     'テーブル作成完了' AS status,
--     COUNT(*) AS table_count 
-- FROM information_schema.tables 
-- WHERE table_schema = 'journal_system';

-- -- ユーザー数確認
-- SELECT role, COUNT(*) AS count FROM users GROUP BY role;

-- -- クラス一覧
-- SELECT 
--     g.grade_number AS 学年,
--     c.class_name AS クラス,
--     COUNT(sca.student_id) AS 生徒数
-- FROM classes c
-- JOIN grades g ON c.grade_id = g.id
-- LEFT JOIN student_class_assignments sca ON c.id = sca.class_id AND sca.is_current = TRUE
-- GROUP BY g.grade_number, c.class_name
-- ORDER BY g.grade_number, c.class_name;

-- -- ====================================
-- -- 完了メッセージ
-- -- ====================================
-- SELECT '
-- ====================================
-- データベース初期化完了！

-- テストアカウント:
-- - 管理者: admin@school.ac.jp / password123
-- - 担任: tanaka.teacher@school.ac.jp / password123
-- - 生徒: yamada.taro@school.ac.jp / password123
-- ====================================
-- ' AS message;

-- ====================================
-- seed.sql（ER図準拠・テストデータ投入）
-- ====================================

SET NAMES 'utf8mb4';

USE journal_system;

-- ====================================
-- パスワードハッシュ（共通）
-- ====================================
SET @password_hash =
'$argon2id$v=19$m=65536,t=3,p=4$n/P+P+d8r/V+7907x/j/fw$a8baIAcJW/o+HX5nCpoC9GjN5L1MeTDsDeXrKz+ZeYo';

-- ====================================
-- 学年
-- ====================================
INSERT INTO grades (grade_number, year)
SELECT 1, YEAR(CURDATE()) UNION ALL
SELECT 2, YEAR(CURDATE()) UNION ALL
SELECT 3, YEAR(CURDATE())
ON DUPLICATE KEY UPDATE grade_number = grade_number;

-- ====================================
-- クラス
-- ====================================
INSERT INTO classes (grade_id, class_name) VALUES
((SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE())), 'A組'),
((SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE())), 'B組'),
((SELECT id FROM grades WHERE grade_number = 2 AND year = YEAR(CURDATE())), 'A組'),
((SELECT id FROM grades WHERE grade_number = 2 AND year = YEAR(CURDATE())), 'B組'),
((SELECT id FROM grades WHERE grade_number = 3 AND year = YEAR(CURDATE())), 'A組');

-- ====================================
-- ユーザー（教師）
-- ====================================
INSERT INTO users (email, password_hash, role, name) VALUES
('tanaka.teacher@school.ac.jp', @password_hash, 'teacher', '田中 一郎'),
('suzuki.teacher@school.ac.jp', @password_hash, 'teacher', '鈴木 次郎'),
('yamamoto.teacher@school.ac.jp', @password_hash, 'teacher', '山本 三郎');

-- ====================================
-- ユーザー（生徒）
-- ====================================
INSERT INTO users (email, password_hash, role, name) VALUES
('yamada.taro@school.ac.jp', @password_hash, 'student', '山田 太郎'),
('sato.hanako@school.ac.jp', @password_hash, 'student', '佐藤 花子'),
('tanaka.jiro@school.ac.jp', @password_hash, 'student', '田中 次郎'),
('suzuki.ichiro@school.ac.jp', @password_hash, 'student', '鈴木 一郎'),
('watanabe.yuki@school.ac.jp', @password_hash, 'student', '渡辺 由紀');

-- ====================================
-- 教師割当
-- ====================================

-- 担任
INSERT INTO teacher_assignments
(teacher_id, assignment_type, grade_id, class_id, is_primary, permission_level)
VALUES
(
  (SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'),
  'homeroom',
  (SELECT grade_id FROM classes WHERE class_name = 'A組' AND grade_id = (
      SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()) LIMIT 1
  ) LIMIT 1),
  (SELECT id FROM classes WHERE class_name = 'A組' AND grade_id = (
      SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()) LIMIT 1
  ) LIMIT 1),
  TRUE,
  'write'
);

INSERT INTO teacher_assignments
(teacher_id, assignment_type, grade_id, class_id, is_primary, permission_level)
VALUES
(
  (SELECT id FROM users WHERE email = 'suzuki.teacher@school.ac.jp'),
  'homeroom',
  (SELECT grade_id FROM classes WHERE class_name = 'B組' AND grade_id = (
      SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()) LIMIT 1
  ) LIMIT 1),
  (SELECT id FROM classes WHERE class_name = 'B組' AND grade_id = (
      SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()) LIMIT 1
  ) LIMIT 1),
  TRUE,
  'write'
);
-- 学年主任
INSERT INTO teacher_assignments
(teacher_id, assignment_type, grade_id, permission_level)
VALUES
(
  (SELECT id FROM users WHERE email = 'suzuki.teacher@school.ac.jp'),
  'grade_head',
  (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE())),
  'admin'
);

-- 教科担当
INSERT INTO teacher_assignments
(teacher_id, assignment_type, grade_id, class_id, subject_id, permission_level)
VALUES
(
  (SELECT id FROM users WHERE email = 'yamamoto.teacher@school.ac.jp'),
  'subject',
  (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()) LIMIT 1),
  (SELECT id FROM classes WHERE class_name = 'A組' 
      AND grade_id = (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()) LIMIT 1) 
      LIMIT 1),
  (SELECT id FROM subjects WHERE name = '数学' LIMIT 1),
  'read'
);

-- ====================================
-- 生徒クラス割当
-- ====================================
INSERT INTO student_class_assignments
(student_id, class_id, is_current)
VALUES
(
  (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'),
  (SELECT id FROM classes WHERE class_name = 'A組'
    AND grade_id = (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()))),
  TRUE
),
(
  (SELECT id FROM users WHERE email = 'sato.hanako@school.ac.jp'),
  (SELECT id FROM classes WHERE class_name = 'A組'
    AND grade_id = (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()))),
  TRUE
),
(
  (SELECT id FROM users WHERE email = 'tanaka.jiro@school.ac.jp'),
  (SELECT id FROM classes WHERE class_name = 'A組'
    AND grade_id = (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()))),
  TRUE
),
(
  (SELECT id FROM users WHERE email = 'suzuki.ichiro@school.ac.jp'),
  (SELECT id FROM classes WHERE class_name = 'B組'
    AND grade_id = (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()))),
  TRUE
),
(
  (SELECT id FROM users WHERE email = 'watanabe.yuki@school.ac.jp'),
  (SELECT id FROM classes WHERE class_name = 'B組'
    AND grade_id = (SELECT id FROM grades WHERE grade_number = 1 AND year = YEAR(CURDATE()))),
  TRUE
);

-- ====================================
-- 連絡帳
-- ====================================
INSERT INTO journal_entries
(student_id, entry_date, submission_date, physical_condition,
 mental_condition, reflection_text, is_read, read_by, read_at)
VALUES
(
  (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'),
  '2025-04-07',
  '2025-04-08',
  'よかった',
  '元気',
  '数学の授業で二次関数を学んだ。完全に理解した。',
  TRUE,
  (SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'),
  '2025-04-08 16:30:00'
);

-- ====================================
-- 教師メモ
-- ====================================
INSERT INTO teacher_notes
(teacher_id, student_id, entry_id, note_text, is_shared)
VALUES
(
  (SELECT id FROM users WHERE email = 'tanaka.teacher@school.ac.jp'),
  (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp'),
  (SELECT id FROM journal_entries
    WHERE entry_date = '2025-04-07'
      AND student_id =
        (SELECT id FROM users WHERE email = 'yamada.taro@school.ac.jp')
    LIMIT 1),
  '数学の理解度が非常に高い。',
  FALSE
);

-- ====================================
SELECT 'seed 完了（ER図準拠）' AS message;

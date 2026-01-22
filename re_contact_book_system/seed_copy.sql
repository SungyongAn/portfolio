-- ====================================
-- seed_classes.sql（classes 再投入用）
-- ====================================

SET NAMES utf8mb4;

USE journal_system;

SET FOREIGN_KEY_CHECKS = 0;

-- 既存クラスを全削除
DELETE FROM classes;

-- 再投入
INSERT INTO classes (grade_id, class_name) VALUES
((SELECT id FROM grades WHERE grade_number = 1 AND year = 2025), 'A組'),
((SELECT id FROM grades WHERE grade_number = 1 AND year = 2025), 'B組'),
((SELECT id FROM grades WHERE grade_number = 2 AND year = 2025), 'A組'),
((SELECT id FROM grades WHERE grade_number = 2 AND year = 2025), 'B組'),
((SELECT id FROM grades WHERE grade_number = 3 AND year = 2025), 'A組');

SET FOREIGN_KEY_CHECKS = 1;

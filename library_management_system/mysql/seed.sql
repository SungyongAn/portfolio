-- ============================================================
-- seed.sql  初期データ投入
-- 実行方法（Docker起動後）:
--   docker compose exec db mysql -u libuser -plibpass library_db < mysql/seed.sql
-- ============================================================

SET NAMES utf8mb4;
SET time_zone = '+09:00';

-- ──────────────────────────────────────────
-- schools  (5校)
-- ──────────────────────────────────────────
INSERT INTO schools (id, name, code, created_at, updated_at) VALUES
  (1, 'A高校', 'A', NOW(), NOW()),
  (2, 'B高校', 'B', NOW(), NOW()),
  (3, 'C高校', 'C', NOW(), NOW()),
  (4, 'D高校', 'D', NOW(), NOW()),
  (5, 'E高校', 'E', NOW(), NOW());

-- ──────────────────────────────────────────
-- users
-- パスワードはすべて "Password1!" の Argon2id ハッシュ
-- 実運用では seed 実行後に各自パスワード変更を行うこと
--
-- ※ 実際のハッシュ値はアプリ起動時に argon2-cffi で生成する。
--   ここでは placeholder として '{ARGON2_HASH}' を記載。
--   初期投入スクリプト (scripts/seed_users.py) で置換すること。
-- ──────────────────────────────────────────

-- 管理者 (各校1名)
INSERT INTO users
  (school_id, email, password_hash, name, barcode, grade, class_name, role, is_committee, is_active, created_at, updated_at)
VALUES
  (1, 'admin.a@school-a.example.jp', '{ARGON2_HASH}', 'A校管理者', NULL, NULL, NULL, 'admin', FALSE, TRUE, NOW(), NOW()),
  (2, 'admin.b@school-b.example.jp', '{ARGON2_HASH}', 'B校管理者', NULL, NULL, NULL, 'admin', FALSE, TRUE, NOW(), NOW()),
  (3, 'admin.c@school-c.example.jp', '{ARGON2_HASH}', 'C校管理者', NULL, NULL, NULL, 'admin', FALSE, TRUE, NOW(), NOW()),
  (4, 'admin.d@school-d.example.jp', '{ARGON2_HASH}', 'D校管理者', NULL, NULL, NULL, 'admin', FALSE, TRUE, NOW(), NOW()),
  (5, 'admin.e@school-e.example.jp', '{ARGON2_HASH}', 'E校管理者', NULL, NULL, NULL, 'admin', FALSE, TRUE, NOW(), NOW());

-- 司書 (各校1名)
INSERT INTO users
  (school_id, email, password_hash, name, barcode, grade, class_name, role, is_committee, is_active, created_at, updated_at)
VALUES
  (1, 'librarian.a@school-a.example.jp', '{ARGON2_HASH}', 'A校司書',  NULL, NULL, NULL, 'librarian', FALSE, TRUE, NOW(), NOW()),
  (2, 'librarian.b@school-b.example.jp', '{ARGON2_HASH}', 'B校司書',  NULL, NULL, NULL, 'librarian', FALSE, TRUE, NOW(), NOW()),
  (3, 'librarian.c@school-c.example.jp', '{ARGON2_HASH}', 'C校司書',  NULL, NULL, NULL, 'librarian', FALSE, TRUE, NOW(), NOW()),
  (4, 'librarian.d@school-d.example.jp', '{ARGON2_HASH}', 'D校司書',  NULL, NULL, NULL, 'librarian', FALSE, TRUE, NOW(), NOW()),
  (5, 'librarian.e@school-e.example.jp', '{ARGON2_HASH}', 'E校司書',  NULL, NULL, NULL, 'librarian', FALSE, TRUE, NOW(), NOW());

-- 生徒 (テスト用 各校2名 / うち1名は図書委員)
INSERT INTO users
  (school_id, email, password_hash, name, barcode, grade, class_name, role, is_committee, is_active, created_at, updated_at)
VALUES
  -- A校
  (1, 'student1.a@school-a.example.jp', '{ARGON2_HASH}', 'A校生徒1', 'A-STU-00001', 1, '1-A', 'student', FALSE, TRUE, NOW(), NOW()),
  (1, 'student2.a@school-a.example.jp', '{ARGON2_HASH}', 'A校生徒2（図書委員）', 'A-STU-00002', 2, '2-B', 'student', TRUE,  TRUE, NOW(), NOW()),
  -- B校
  (2, 'student1.b@school-b.example.jp', '{ARGON2_HASH}', 'B校生徒1', 'B-STU-00001', 1, '1-A', 'student', FALSE, TRUE, NOW(), NOW()),
  (2, 'student2.b@school-b.example.jp', '{ARGON2_HASH}', 'B校生徒2（図書委員）', 'B-STU-00002', 3, '3-C', 'student', TRUE,  TRUE, NOW(), NOW()),
  -- C校
  (3, 'student1.c@school-c.example.jp', '{ARGON2_HASH}', 'C校生徒1', 'C-STU-00001', 2, '2-A', 'student', FALSE, TRUE, NOW(), NOW()),
  (3, 'student2.c@school-c.example.jp', '{ARGON2_HASH}', 'C校生徒2（図書委員）', 'C-STU-00002', 1, '1-D', 'student', TRUE,  TRUE, NOW(), NOW()),
  -- D校
  (4, 'student1.d@school-d.example.jp', '{ARGON2_HASH}', 'D校生徒1', 'D-STU-00001', 3, '3-A', 'student', FALSE, TRUE, NOW(), NOW()),
  (4, 'student2.d@school-d.example.jp', '{ARGON2_HASH}', 'D校生徒2（図書委員）', 'D-STU-00002', 2, '2-B', 'student', TRUE,  TRUE, NOW(), NOW()),
  -- E校
  (5, 'student1.e@school-e.example.jp', '{ARGON2_HASH}', 'E校生徒1', 'E-STU-00001', 1, '1-A', 'student', FALSE, TRUE, NOW(), NOW()),
  (5, 'student2.e@school-e.example.jp', '{ARGON2_HASH}', 'E校生徒2（図書委員）', 'E-STU-00002', 3, '3-B', 'student', TRUE,  TRUE, NOW(), NOW());
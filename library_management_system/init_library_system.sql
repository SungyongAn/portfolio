-- init_library_system.sql
CREATE DATABASE IF NOT EXISTS library_system
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE library_system;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '利用者ID',
    username VARCHAR(100) NOT NULL COMMENT 'ユーザー名',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT 'メールアドレス',
    enrollment_year YEAR NOT NULL COMMENT '入学年(西暦)',
    graduation_year YEAR NOT NULL COMMENT '卒業予定年(西暦)',
    password_hash VARCHAR(255) NOT NULL COMMENT 'パスワード(ハッシュ化推奨)',
    school_name VARCHAR(255) NOT NULL COMMENT '所属(学校名)',
    role ENUM('student','staff','admin') DEFAULT 'student' COMMENT '権限'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


USE library_system;

CREATE TABLE Materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,       -- 資料ID（自動採番）
    registration_date DATE NOT NULL,                  -- 登録日
    title VARCHAR(255) NOT NULL,                      -- タイトル
    author VARCHAR(255),                              -- 著者名
    publisher VARCHAR(255),                           -- 出版社
    ndc_code CHAR(3),                                 -- 分類(NDC)
    type_id INT,                                      -- 種別ID（material_typesテーブル参照）
    location VARCHAR(100),                             -- 所在（学校名＋棚など）
    loan_status ENUM('在架', '貸出中', '延滞', '紛失') DEFAULT '在架',  -- 貸出状況
    barcode VARCHAR(50) UNIQUE NOT NULL               -- 一元バーコード番号
);

-- CREATE TABLE accounts (
--     user_id        VARCHAR(50) PRIMARY KEY COMMENT '利用者ID',
--     username       VARCHAR(100) NOT NULL COMMENT 'ユーザー名',
--     email          VARCHAR(255) UNIQUE NOT NULL COMMENT 'メールアドレス',
--     admission_year YEAR NOT NULL COMMENT '入学年(西暦)',
--     graduation_year YEAR NOT NULL COMMENT '卒業予定年(西暦)',
--     password       VARCHAR(255) NOT NULL COMMENT 'パスワード(ハッシュ化推奨)',
--     affiliation    VARCHAR(255) NOT NULL COMMENT '所属(学校名)',
--     role ENUM('ユーザー', '図書委員', '司書', '管理者') NOT NULL DEFAULT 'ユーザー' COMMENT '権限',
--     created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- INSERT INTO accounts (user_id, username, email, admission_year, graduation_year, password, affiliation, role) VALUES
-- -- ユーザー（一般利用者）- パスワード未登録
-- ('user001', '田中太郎', 'user001@a-school.ac.jp', 2023, 2027, '', 'A校', 'ユーザー'),

-- -- 図書委員
-- ('committee001', '佐藤花子', 'committee001@a-school.ac.jp', 2022, 2026, 'testcommit', 'A校', '図書委員'),

-- -- 司書
-- ('librarian001', '山田次郎', 'librarian001@a-school.ac.jp', 2020, 2024, 'testlibrarian', 'A校', '司書'),

-- -- 管理者
-- ('admin001', '鈴木三郎', 'admin001@a-school.ac.jp', 2019, 2023, 'testadmin', 'A校', '管理者');


USE library_system;

-- UPDATE MaterialType SET type_name='図書' WHERE type_id=1;
-- UPDATE MaterialType SET type_name='雑誌' WHERE type_id=2;
-- UPDATE MaterialType SET type_name='新聞' WHERE type_id=3;
-- UPDATE MaterialType SET type_name='視聴覚資料' WHERE type_id=4;
-- UPDATE MaterialType SET type_name='電子資料' WHERE type_id=5;

-- UPDATE LoanStatus SET status_name='在庫あり' WHERE status_code='AVAILABLE';
-- UPDATE LoanStatus SET status_name='移動中' WHERE status_code='MOVING';
-- UPDATE LoanStatus SET status_name='貸出中' WHERE status_code='ON_LOAN';
-- UPDATE LoanStatus SET status_name='予約中' WHERE status_code='RESERVED';

-- UPDATE NDC SET ndc_name='総記' WHERE ndc_code='000';
-- UPDATE NDC SET ndc_name='哲学' WHERE ndc_code='100';
-- UPDATE NDC SET ndc_name='歴史' WHERE ndc_code='200';
-- UPDATE NDC SET ndc_name='社会科学' WHERE ndc_code='300';
-- UPDATE NDC SET ndc_name='自然科学' WHERE ndc_code='400';
-- UPDATE NDC SET ndc_name='技術・工学' WHERE ndc_code='500';
-- UPDATE NDC SET ndc_name='農業' WHERE ndc_code='600';
-- UPDATE NDC SET ndc_name='工業' WHERE ndc_code='700';
-- UPDATE NDC SET ndc_name='言語' WHERE ndc_code='800';
-- UPDATE NDC SET ndc_name='文学' WHERE ndc_code='900';
-- UPDATE NDC SET ndc_name='未分類' WHERE ndc_code='999';

-- INSERT IGNORE INTO NDC (ndc_code, ndc_name) VALUES
-- ('000', '総記'),
-- ('100', '哲学'),
-- ('200', '歴史'),
-- ('300', '社会科学'),
-- ('400', '自然科学'),
-- ('500', '技術・工学'),
-- ('600', '産業'),
-- ('700', '芸術'),
-- ('800', '言語'),
-- ('900', '文学'),
-- ('999', '未分類');


-- INSERT INTO Materials
-- (barcode, title, author, publisher, ndc_code, type_id, affiliation, shelf, loan_status, registration_date)
-- VALUES
-- ('BC0001', 'はじめてのPython', '山田太郎', '出版社A', '000', 1, 'A校', 'A1', 'AVAILABLE', '2025-09-29'),
-- ('BC0002', '世界の歴史', '佐藤花子', '出版社B', '200', 1, 'B校', 'B1', 'ON_LOAN', '2025-09-28'),
-- ('BC0003', '哲学入門', '田中一郎', '出版社C', '100', 2, 'C校', 'C1', 'AVAILABLE', '2025-09-27');

INSERT INTO NDC (ndc_code, ndc_name) VALUES
('000', '総記'),
('100', '哲学'),
('200', '歴史'),
('300', '社会科学'),
('400', '自然科学'),
('500', '技術・工学'),
('600', '産業'),
('700', '芸術'),
('800', '言語'),
('900', '文学'),
('999', '未分類'); -- 追加

-- NDC分類テーブル
CREATE TABLE NDC (
    ndc_code VARCHAR(10) PRIMARY KEY,
    ndc_name VARCHAR(100) NOT NULL
);

INSERT INTO MaterialType (type_name) VALUES
('図書'), ('雑誌'), ('新聞'), ('視聴覚資料'), ('電子資料');

-- 資料種別テーブル
CREATE TABLE MaterialType (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE
);


INSERT INTO LoanStatus (status_code, status_name) VALUES
('AVAILABLE', '在庫あり'),
('ON_LOAN', '貸出中'),
('RESERVED', '予約中'),
('MOVING', '移動中');

-- 貸出状況テーブル
CREATE TABLE LoanStatus (
    status_code VARCHAR(20) PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);



-- Materials テーブル
CREATE TABLE Materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(50) NOT NULL UNIQUE COMMENT '一元バーコード番号',
    title VARCHAR(255) NOT NULL COMMENT '書籍タイトル',
    author VARCHAR(100) COMMENT '著者名',
    publisher VARCHAR(100) COMMENT '出版社',
    ndc_code VARCHAR(10) NOT NULL COMMENT '分類(NDC)',
    type_id INT NOT NULL COMMENT '種別',
    affiliation VARCHAR(255) NOT NULL COMMENT '学校名',
    shelf VARCHAR(50) COMMENT '棚版',
    loan_status VARCHAR(20) NOT NULL COMMENT '貸出状況',
    registration_date DATE NOT NULL COMMENT '登録日',
    FOREIGN KEY (ndc_code) REFERENCES NDC(ndc_code),
    FOREIGN KEY (type_id) REFERENCES MaterialType(type_id),
    FOREIGN KEY (loan_status) REFERENCES LoanStatus(status_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='図書資料テーブル';

-- Materials_Loans テーブル
CREATE TABLE Materials_Loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL COMMENT 'ユーザーID',
    material_id INT NOT NULL COMMENT '資料ID',
    loan_date DATE NOT NULL COMMENT '貸出日',
    due_date DATE NOT NULL COMMENT '返却予定日',
    return_date DATE COMMENT '返却日',
    overdue_flag TINYINT(1) DEFAULT 0 COMMENT '延滞状況',
    affiliation VARCHAR(255) NOT NULL COMMENT '学校名',
    FOREIGN KEY (material_id) REFERENCES Materials(material_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='貸出履歴テーブル';

-- Materials_Reservations テーブル
CREATE TABLE Materials_Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL COMMENT 'ユーザーID',
    material_id INT NOT NULL COMMENT '資料ID',
    reservation_date DATE NOT NULL COMMENT '予約した日',
    reservation_order INT NOT NULL COMMENT '順番',
    school_moving_flag TINYINT(1) DEFAULT 0 COMMENT '学校間移動の有無',
    from_affiliation VARCHAR(255) NOT NULL COMMENT '発送元学校名',
    to_affiliation VARCHAR(255) NOT NULL COMMENT '発送先学校名',
    FOREIGN KEY (material_id) REFERENCES Materials(material_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='資料予約テーブル';




アカウントテーブル
CREATE TABLE accounts (
    user_id VARCHAR(50) NOT NULL COMMENT 'ユーザーID',
    username       VARCHAR(100) NOT NULL COMMENT 'ユーザー名',
    email          VARCHAR(255) UNIQUE NOT NULL COMMENT 'メールアドレス',
    admission_year YEAR NOT NULL COMMENT '入学年(西暦)',
    graduation_year YEAR NOT NULL COMMENT '卒業予定年(西暦)',
    password       VARCHAR(255) NOT NULL COMMENT 'パスワード(ハッシュ化推奨)',
    affiliation    VARCHAR(255) NOT NULL COMMENT '所属(学校名)',
    role ENUM('ユーザー', '図書委員', '司書', '管理者') NOT NULL DEFAULT 'ユーザー' COMMENT '権限',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- INSERT INTO accounts (user_id, username, email, admission_year, graduation_year, password, affiliation, role) VALUES
-- -- ユーザー（一般利用者）- パスワード未登録
-- ('user001', '田中太郎', 'user001@a-school.ac.jp', 2023, 2027, '', 'A校', 'ユーザー'),

-- -- 図書委員
-- ('committee001', '佐藤花子', 'committee001@a-school.ac.jp', 2022, 2026, 'testcommit', 'A校', '図書委員'),

-- -- 司書
-- ('librarian001', '山田次郎', 'librarian001@a-school.ac.jp', 2020, 2024, 'testlibrarian', 'A校', '司書'),

-- -- 管理者
-- ('admin001', '鈴木三郎', 'admin001@a-school.ac.jp', 2019, 2023, 'testadmin', 'A校', '管理者');

-- データベースを選択
USE accounts;

INSERT INTO users (user_id, username, email, admission_year, graduation_year, password, affiliation, role)
VALUES ('s12345', '山田太郎', 'taro@example.com', 2023, 2027, 
        '$2b$12$Wz7Fz6x5zM0pXvN1c4kzpeRfTfI3nbCn1Qqf5s7B6sQXlVRmFQd2a', -- ← "testpass" のbcrypt例
        '○○大学', 'ユーザー');

-- usersテーブルを作成
-- CREATE TABLE users (
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

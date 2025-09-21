7/25
・MySQLはOSverが古いためインストール不可を確認
・dockerを使用してMySQLの学習をすることに。

＜dockerでのMySQL起動手順＞
# MySQL 8.0を起動（初回）
docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD= \
  -p 3306:3306 \
  -d mysql:8.0

# 停止中のコンテナを再起動　※7/26 追記※
docker start mysql-server

# コンテナ内でmysqlクライアントを使用
docker exec -it mysql-server mysql -u root -p

# または外部のmysqlクライアントから接続
mysql -h 127.0.0.1 -P 3306 -u root -p

-- データベース作成
CREATE DATABASE #名称;

-- ユーザー作成
CREATE USER 'webuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mywebsite.* TO 'webuser'@'%';

# クライアントからのログアウト
exit;

7/26
MySQL操作コマンド関連まとめサイト
・https://qiita.com/yuzooho/items/5d608f3b84a2037cada0
・https://qiita.com/CyberMergina/items/f889519e6be19c46f5f4

7/27
・MySQLでmywebsite_dbを作成
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| username      | varchar(255) | NO   |     | NULL    |                |
| email_address | varchar(255) | NO   | UNI | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+


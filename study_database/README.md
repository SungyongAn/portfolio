7/25
・MySQLはOSverが古いためインストール不可を確認
・dockerを使用してMySQLの学習をすることに。

＜一部操作手順＞
# MySQL 8.0を起動
docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD= \
  -p 3306:3306 \
  -d mysql:8.0

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


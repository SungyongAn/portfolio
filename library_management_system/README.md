9/5
・Excelファイルにて設計案の作成を開始
■作業時間:4時間

9/8
・設計案の作成をWordファイルに変更
■作業時間：6時間（計10時間）

9/9
・9/8の続き設計案の作成
・マニュアルにも活用できるように構成を変更
■作業時間：5時間半（計15時間半）

9/10
・設計案の作成を完了
■作業時間：5時間（計20時間半）

9/11
・ログイン、ログアウト機能の作成開始
・DockerでMySQLを使用
・python3でのMySQLへのアクセスのため pip install mysql-connector-python を実行
・pip install sqlalchemy, pip install PyMySQL, pip install passlib

・MySQLで日本語入力が行えないため、ファイルからテーブル関係の操作を実施
docker exec -i mysql mysql -u root -prootpass --default-character-set=utf8mb4 accounts < create_users.sql        
■作業時間：5時間（計25時間）

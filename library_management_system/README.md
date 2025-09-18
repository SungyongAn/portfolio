9/5
・Excelファイルにて設計案の作成を開始

9/8
・設計案の作成をWordファイルに変更

9/9
・9/8の続き設計案の作成
・マニュアルにも活用できるように構成を変更

9/10
・設計案の作成を完了

9/11
・ログイン、ログアウト機能の作成開始
・DockerでMySQLを使用
・python3でのMySQLへのアクセスのため pip install mysql-connector-python を実行
・pip install sqlalchemy, pip install PyMySQL, pip install passlib 実施

・MySQLで日本語入力が行えないため、ファイルからテーブル関係の操作を実施
docker exec -i mysql mysql -u root -prootpass --default-character-set=utf8mb4 accounts < create_users.sql        

9/12
・作成したログイン、ログアウト機能を参考に作業工程表を作成
・作業工程表を元にissueの作成を開始

9/17
・pip install aiosmtplib apscheduler sqlalchemy pymysql 実施

9/18
・issue完成
・コードの作成を開始

■やったこと
・frontend, backendのディレクトリ作成
・index.html, app.jsのファイル作成
・TOPページの作成、サイドメニューにTOPページ、tsetのボタンを設置して各ボタンを押した時、メイン画面がそれぞれの指定した表示内容になるように設定と動作確認を実施
・のMySQLによるデータベースの作成のためdocker-compose.yml, .envを作成
・DB名:library_system を作成
・テーブル:accountsを作成（詳細はinit_library_system.sql参照）

■次回やること
・テーブル:accounts で権限：司書が漏れていたため追加
・４つ権限それぞれでテスト用のアカウントを登録から再開
※権限：student、staffはパスワード未登録で作成、他は全項目を登録

■問題点や課題、困っていることなど
・現状の問題点はなし
・今回苦労したのはDB作成時に学習用に作成したDBで同じポートを使用していたため、
　削除など手間がかかったのと、久しぶりのDocker操作のため忘れていた部分を思い出すのに手間取った

■作業時間
1時間40分＋日報10分

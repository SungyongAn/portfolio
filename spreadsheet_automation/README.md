7/17
・gspreadをインストール
・Google Cloud Consoleで、Google Drive APIとGoogle Sheets APIを有効化
・Google Cloud Consoleでサービスアカウントを作成し、認証用のJSONファイルをダウンロード

7/18
・google-api-python-clientをインストール
・スプレットシートのID情報の位置を確認
例）https://docs.google.com/spreadsheets/d/1DWh31MX〜〜〜〜〜〜88zJqWJk8/edit?gid=0#gid=0
この場合は「https://docs.google.com/spreadsheets/d/」と「/edit?gid=0#gid=0」の間の「1DWh31MX〜〜〜〜〜〜88zJqWJk8」が該当
・作成済みのスプレットシートへのアクセスに成功

7/19
・OAuthのクライントを作成、認証キーを取得
・新規スプレットシートをpython3で自動作成する手順に苦戦するものの、以下のサイトと知人の作成してくれたマニュアルを元に指定したアカウントのドライブへの作成に成功
https://mori-memo.hateblo.jp/entry/2023/05/07/160626
https://qiita.com/plumfield56/items/dab6230512f3381fdcad

7/20
・pydriveをインストール
・Googleドライブへのフォルダ作成に成功
※注意※
# フォルダのメタデータを定義の際、mimeTypeを指定しない場合、空のファイルとして作成されるので注意
# ただ、mimeTypeの種類は多数あるが、対象フォルダに保存できるファイルは固定されずあらゆるファイルを保存できる
file_metadata = {
    'name': folder_name,
    'mimeType': 'application/vnd.google-apps.folder'
    }


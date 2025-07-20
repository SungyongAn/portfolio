from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# サービスアカウントキーファイル
KEY_FILE = 'json'

# 認証
credentials = Credentials.from_service_account_file(KEY_FILE)
service = build('sheets', 'v4', credentials=credentials)

# スプレッドシートID
SPREADSHEET_ID = ''

# データを読み取る
sheet = service.spreadsheets()
result = sheet.values().get(
    spreadsheetId=SPREADSHEET_ID,
    range='シート1!A1:C10'
).execute()

values = result.get('values', [])
print('データ:', values)

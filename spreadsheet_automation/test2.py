import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

KEY_FILE = 'json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

# 新しいスプレッドシートを作成
spreadsheet = gc.create('フォルダ内のスプレッドシート')

# 特定のフォルダに移動（フォルダIDが必要）
folder_id = 'マイドライブフォルダID'

# Google Drive APIを使用してフォルダに移動
drive_service = build('drive', 'v3', credentials=credentials)

# ファイルをフォルダに移動
file = drive_service.files().get(fileId=sfolder_id, fields='parents').execute()

previous_parents = ','.join(file.get('parents'))
result = drive_service.files().update(
    fileId=spreadsheet.id,
    addParents=folder_id,
    removeParents=previous_parents,
    fields='id, parents',
    ).execute()
    
print(f'✅ フォルダ内にスプレッドシートが作成されました')
print(f'URL: {spreadsheet.url}')
print(f'ファイルID: {result["id"]}')
print(f'親フォルダ: {result["parents"]}')

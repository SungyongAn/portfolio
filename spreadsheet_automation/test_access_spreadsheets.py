from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pathlib import Path


def access_sheet(json_path, sheet_id):
    # サービスアカウントキーファイル
    KEY_FILE = json_path

    # 認証
    credentials = Credentials.from_service_account_file(KEY_FILE)
    service = build('sheets', 'v4', credentials=credentials)

    # スプレッドシートID
    SPREADSHEET_ID = sheet_id

    # データを読み取る
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='シート1!A1:C10'
    ).execute()

    values = result.get('values', [])
    return print('データ:', values)


if __name__ == "__main__":
    json_path = Path.home()
    sheet_id = ""
    access_sheet(json_path, sheet_id)

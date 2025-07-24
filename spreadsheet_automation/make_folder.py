import gspread
from googleapiclient.discovery import build
from pathlib import Path

# gspread での認証
gc = gspread.oauth(
    credentials_filename= Path.home() / "Desktop" / "hale-safeguard-431900-e2-50938872b873.json",
)

# gspreadの認証情報を使ってGoogle Drive APIサービスを構築
drive_service = build('drive', 'v3', credentials=gc.http_client.auth)


def create_drive_folder(folder_name, parent_folder_id=None):

    # フォルダのメタデータを定義
    # mimeTypeを指定しない場合、空のファイルとして作成されるので注意
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # 親フォルダが指定されている場合は追加（parent_folder_id=Noneの場合はスルー）
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    try:
        # フォルダを作成
        folder = drive_service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()

        folder_id = folder.get('id')
        print(f'フォルダ "{folder_name}" を作成しました。')
        print(f'フォルダID: {folder_id}')
        print(f'フォルダURL: https://drive.google.com/drive/folders/{folder_id}')

        return folder_id

    except Exception as e:
        print(f'フォルダ作成エラー: {e}')
        return None


if __name__ == "__main__":
    # 新しいフォルダを作成
    new_folder_id = create_drive_folder("Python")
    
    # サブフォルダも作成する場合（上で作成したフォルダの中に）
    # if new_folder_id:
    #     sub_folder_id = create_drive_folder("サブフォルダ", new_folder_id)

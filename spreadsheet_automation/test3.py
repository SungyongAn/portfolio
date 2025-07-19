import gspread
from google.auth import default
creds, _ = default()

# 認証処理
gc = gspread.authorize(creds)

import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

# -----------------------------
# ログイン情報（開発用）
# -----------------------------
EMAIL = "sato.hanako@school.ac.jp"
PASSWORD = "password123"  # seed.sql で設定した平文に対応するもの

# -----------------------------
# 1. ログインしてトークン取得
# -----------------------------
login_res = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "email": EMAIL,
        "password": PASSWORD
    }
)

login_res.raise_for_status()
token = login_res.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("✅ ログイン成功")

# -----------------------------
# 2. 連絡帳データ作成
# -----------------------------
journal_payload = {
    "entry_date": (date.today() - timedelta(days=1)).isoformat(),
    "physical_condition": "良好",
    "mental_condition": "元気",
    "reflection_text": "Pythonスクリプトから自動投稿テスト"
}

journal_res = requests.post(
    f"{BASE_URL}/api/journals/",
    json=journal_payload,
    headers=headers
)

journal_res.raise_for_status()

journal = journal_res.json()

print("✅ 連絡帳登録成功")
print(f"  ID: {journal['id']}")
print(f"  日付: {journal['entry_date']}")

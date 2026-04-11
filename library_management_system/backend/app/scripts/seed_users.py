#!/usr/bin/env python3
"""
scripts/seed_users.py
seed.sql 内の '{ARGON2_HASH}' プレースホルダーを
Argon2id ハッシュに置換して MySQL に投入するスクリプト。

実行方法:
  # Docker コンテナ内 (backend サービス) で実行する場合
  docker compose exec backend python scripts/seed_users.py

  # ローカルで直接実行する場合（DB が起動済みであること）
  DATABASE_URL=mysql+pymysql://library_user:library_password@127.0.0.1:3306/library_db \
    python scripts/seed_users.py
"""
import os
import sys
import re

# argon2-cffi が必要: pip install argon2-cffi
try:
    from argon2 import PasswordHasher
except ImportError:
    print("[ERROR] argon2-cffi が未インストールです。")
    print("  pip install argon2-cffi  を実行してください。")
    sys.exit(1)

try:
    import pymysql  # noqa: F401
    from sqlalchemy import create_engine, text
except ImportError:
    print("[ERROR] sqlalchemy / pymysql が未インストールです。")
    sys.exit(1)

# ── 設定 ──────────────────────────────────────────────────────────────
DEFAULT_PASSWORD = "Password1!"  # 初期パスワード（全ユーザー共通）
SEED_SQL_PATH = "/mysql/seed.sql"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://library_user:library_password@db:3306/library_db?charset=utf8mb4",
)

# ── Argon2id ハッシュ生成 ──────────────────────────────────────────────
ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16,
)
hashed = ph.hash(DEFAULT_PASSWORD)
print(f"[INFO] Generated Argon2id hash for '{DEFAULT_PASSWORD}'")

# ── seed.sql 読み込み・プレースホルダー置換 ──────────────────────────
with open(SEED_SQL_PATH, encoding="utf-8") as f:
    sql_raw = f.read()

# MySQL では '$' が特殊文字になる場合があるため文字列エスケープ
hashed_escaped = hashed.replace("\\", "\\\\").replace("'", "\\'")
sql_replaced = sql_raw.replace("{ARGON2_HASH}", hashed_escaped)

# ── DB 接続・実行 ──────────────────────────────────────────────────────
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SQL を文単位に分割（コメント行・空行を除外）
statements = [
    s.strip()
    for s in re.split(r";[ \t]*\n", sql_replaced)
    if s.strip() and not s.strip().startswith("--")
]

print(f"[INFO] Executing {len(statements)} SQL statements...")
with engine.connect() as conn:
    for stmt in statements:
        if stmt:
            conn.execute(text(stmt + ";"))
    conn.commit()

print("[INFO] seed.sql の投入が完了しました。")
print(f"[INFO] 初期パスワード: {DEFAULT_PASSWORD}")
print("[WARN] 本番環境では必ず各ユーザーにパスワード変更を促してください。")

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# 環境変数から DATABASE_URL を取得
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

print(f"DATABASE_URL from environment: {DATABASE_URL.split('@')[0]}@...")  # パスワード部分を隠して表示

# mysql:// を mysql+pymysql:// に変換
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# 既存のクエリパラメータを削除（クリーンな状態から開始）
if "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

# PlanetScale用の設定
# connect_args で SSL を設定（URL パラメータではなく）
connect_args = {}
if "psdb.cloud" in DATABASE_URL:
    connect_args = {
        "ssl": {
            "ssl_mode": "REQUIRED"  # これは connect_args 内でのみ有効
        }
    }

print(f"Connecting to: {DATABASE_URL.split('@')[1]}")  # ホスト部分のみ表示

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

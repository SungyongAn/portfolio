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

# mysql:// を mysql+pymysql:// に変換
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# PlanetScale用のSSL設定
# URLパラメータをクリーンにして、必要なSSLパラメータのみ追加
if "psdb.cloud" in DATABASE_URL:
    # 既存のクエリパラメータを削除
    if "?" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.split("?")[0]
    
    # 正しいSSLパラメータを追加
    DATABASE_URL += "?ssl_mode=REQUIRED"

print(f"Connecting to: {DATABASE_URL.split('@')[1]}")  # パスワード部分を隠して表示

# エンジン作成
engine = create_engine(
    DATABASE_URL,
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

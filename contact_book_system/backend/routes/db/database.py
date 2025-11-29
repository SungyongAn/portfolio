import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# mysql:// を mysql+pymysql:// に変換
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# クエリパラメータをクリア
if "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

# PlanetScale用の SSL 設定（検証を無効化）
connect_args = {}
if "psdb.cloud" in DATABASE_URL:
    connect_args = {
        "ssl": True  # シンプルに True のみ
    }

print(f"Connecting to: {DATABASE_URL.split('@')[1]}")

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

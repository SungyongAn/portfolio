import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .envファイルを読み込み
load_dotenv()

# 環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

# または個別に取得
if not DATABASE_URL:
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_USER = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "rootpass")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "renrakucho_db")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
    
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

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
        "ssl": {}
    }

print(f"Connecting to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Unknown'}")

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from dotenv import load_dotenv

# .env の読み込み
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

print(f"DATABASE_URL from environment: {DATABASE_URL}")

# mysql:// → mysql+pymysql:// に変換
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# PlanetScale の場合、SSL を明示的に有効化（pymysql）
connect_args = {}
if "psdb.cloud" in DATABASE_URL:
    connect_args = {
        "ssl": {
            "ssl": True
        }
    }
    print("✓ SSL config enabled for PlanetScale")

# SQLAlchemy エンジン作成
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,   # 接続断対策
    pool_recycle=3600,    # MySQL の 8 時間制限対策
    echo=False
)

# セッション生成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル基底クラス
Base = declarative_base()

# FastAPI の依存注入用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

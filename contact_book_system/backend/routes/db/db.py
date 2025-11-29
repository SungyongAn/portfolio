import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# 環境変数から DATABASE_URL を取得
DATABASE_URL = os.getenv("DATABASE_URL")

# mysql:// を mysql+pymysql:// に変換
if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# PlanetScale用の接続設定
# SSLパラメータをURL内で指定
if DATABASE_URL and "psdb.cloud" in DATABASE_URL:
    # URLに ssl_disabled=False を追加（PlanetScaleはSSL必須）
    if "?" in DATABASE_URL:
        DATABASE_URL += "&ssl_disabled=false"
    else:
        DATABASE_URL += "?ssl_disabled=false"

# エンジン作成（connect_args は使わない）
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

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# docker-compose の backend/.env から読み込まれる想定
# DATABASE_URL=mysql+pymysql://library_user:library_password@db:3306/library_db
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://library_user:library_password@db:3306/library_db?charset=utf8mb4",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 接続死活確認
    pool_recycle=3600,  # 1時間でコネクション再生成
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI の Depends で利用する DB セッションジェネレータ"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

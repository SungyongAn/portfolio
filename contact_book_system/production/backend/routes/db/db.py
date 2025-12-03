from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# データベース接続URL（環境に応じて変更）
DATABASE_URL = "mysql+pymysql://appuser:apppass@localhost:3306/renrakucho_db?charset=utf8mb4"


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # 開発時のみTrue
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

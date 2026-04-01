from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベース接続URL
# 環境変数から取得、なければデフォルト値を使用
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@db:3306/baseball_talent_manager?charset=utf8mb4"
)

# SQLAlchemyエンジンの作成
# echo=True: SQLログを出力（開発時のみ推奨）
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 本番環境ではFalse推奨
    pool_pre_ping=True,  # 接続の有効性を確認
    pool_recycle=3600,  # 1時間ごとに接続をリサイクル
)

# セッションファクトリーの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# モデルのベースクラス
Base = declarative_base()


# 依存性注入用のDB取得関数
def get_db():
    """
    FastAPIの依存性注入で使用するDB接続取得関数
    
    使用例:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

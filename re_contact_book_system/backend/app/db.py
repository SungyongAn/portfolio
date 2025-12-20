"""
データベース接続とセッション管理
"""
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
    "mysql+pymysql://journal_user:journal_pass@localhost:3306/journal_system"
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


# データベース初期化関数（テーブル作成）
def init_db():
    """
    すべてのモデルのテーブルを作成する
    
    注意: 本番環境ではAlembicを使用すること
    開発・テスト環境でのみ使用
    """
    from app.models import user, journal, class_model  # noqa
    Base.metadata.create_all(bind=engine)
    print("✅ データベーステーブルを作成しました")


# データベーステスト接続関数
def test_db_connection():
    """
    データベース接続をテストする
    
    Returns:
        bool: 接続成功ならTrue、失敗ならFalse
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ データベース接続成功")
        return True
    except Exception as e:
        print(f"❌ データベース接続失敗: {e}")
        return False


# スタンドアロン実行時のテスト
if __name__ == "__main__":
    print("=== データベース接続テスト ===")
    print(f"接続先: {DATABASE_URL}")
    
    if test_db_connection():
        print("\n=== テーブル作成 ===")
        init_db()
    else:
        print("\n⚠️ データベースに接続できません")
        print("1. MySQLが起動しているか確認してください")
        print("2. 接続情報が正しいか確認してください")
        print("3. データベースが作成されているか確認してください")

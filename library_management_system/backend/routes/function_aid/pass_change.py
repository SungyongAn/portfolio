import sys, os
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# このファイルの親ディレクトリ (backend) を sys.path に追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.models import Account  # これでOK

# ====== DB接続設定 ======
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppass") 
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "library_system")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# ====== パスワード更新関数 ======
def update_password(db: Session, user_id: str, new_password: str):
    user = db.query(Account).filter(Account.user_id == user_id.strip()).first()

    if not user:
        return {"success": False, "reason": "user_not_found"}

    # 新しいパスワードをハッシュ化
    hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user.password = hashed_pw
    db.commit()

    return {"success": True, "message": "password_updated"}


# ====== テスト実行 ======
if __name__ == "__main__":
    db = SessionLocal()

    target_user = "admin001"
    new_password = "testadmin"

    result = update_password(db, target_user, new_password)
    print(result)

    db.close()

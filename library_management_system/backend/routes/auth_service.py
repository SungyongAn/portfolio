import bcrypt
from sqlalchemy.orm import Session
from routes.models import Account


def authenticate(db: Session, user_id: str, password: str):
    # 認証成功時に権限のみを返す
    user = db.query(Account).filter(Account.user_id == user_id).first()
    
    print(user_id)

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user.role  # 権限のみを返す

    return None  # 認証失敗

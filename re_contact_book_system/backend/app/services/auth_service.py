from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

# パスワードハッシュ化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


# パスワード検証
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# パスワードのハッシュ化
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ユーザー認証
def authenticate_user(db: Session, email: str, password: str):
    # メールアドレスを小文字に統一
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    JWTトークンを生成
    
    Args:
        data: トークンに含めるデータ
        expires_delta: 有効期限
    
    Returns:
        str: JWTトークン
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    JWTトークンをデコード
    
    Args:
        token: JWTトークン
    
    Returns:
        dict: デコードされたペイロード
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

# パスワードハッシュ化設定（Argon2）
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# JWT設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-please-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 3600)
)  # 1時間
REFRESH_TOKEN_EXPIRE_SECONDS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", 604800)
)  # 7日間


def hash_password(password: str) -> str:
    """パスワードをArgon2でハッシュ化する"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証する"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    """アクセストークンを生成する"""
    expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """リフレッシュトークンを生成する"""
    expire = datetime.now(timezone.utc) + timedelta(
        seconds=REFRESH_TOKEN_EXPIRE_SECONDS
    )
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """トークンをデコードする。無効な場合はNoneを返す"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

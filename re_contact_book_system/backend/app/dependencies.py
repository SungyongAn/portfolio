from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User, RoleEnum
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    JWTトークンから現在のユーザーを取得
    
    Args:
        credentials: HTTPベアラー認証情報
        db: データベースセッション
    
    Returns:
        User: 現在のユーザー
    
    Raises:
        HTTPException: 認証失敗時
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が無効です",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    現在のアクティブユーザーを取得
    
    Args:
        current_user: 現在のユーザー
    
    Returns:
        User: アクティブユーザー
    """
    # 将来的にユーザーの有効/無効フラグを追加する場合はここで確認
    return current_user


def require_role(allowed_roles: list[RoleEnum]):
    """
    特定のロールを要求するデコレータ
    
    Args:
        allowed_roles: 許可するロールのリスト
    
    Returns:
        関数: 依存性注入用の関数
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"この操作には{', '.join([role.value for role in allowed_roles])}の権限が必要です"
            )
        return current_user
    return role_checker


# ロール別の依存性注入
def get_current_student(current_user: User = Depends(get_current_active_user)) -> User:
    """生徒ユーザーを取得"""
    if current_user.role != RoleEnum.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作は生徒のみ実行できます"
        )
    return current_user


def get_current_teacher(current_user: User = Depends(get_current_active_user)) -> User:
    """教師ユーザーを取得"""
    if current_user.role != RoleEnum.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作は教師のみ実行できます"
        )
    return current_user


def get_current_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """管理者ユーザーを取得"""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作は管理者のみ実行できます"
        )
    return current_user


def get_current_teacher_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """教師または管理者を取得"""
    if current_user.role not in [RoleEnum.teacher, RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作は教師または管理者のみ実行できます"
        )
    return current_user

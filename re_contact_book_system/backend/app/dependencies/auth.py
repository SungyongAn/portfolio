from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User, RoleEnum
from app.utils.token_utils import decode_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    アクセストークンから現在のユーザーを取得
    """
    token = credentials.credentials

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証情報が無効です",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str | None = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証情報が無効です",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーが存在しません",
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    現在のアクティブユーザーを取得
    （将来 is_active フラグなどを確認する想定）
    """
    return current_user


def require_role(allowed_roles: list[RoleEnum]):
    """
    特定ロールを要求する依存関数
    """
    def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="権限がありません",
            )
        return current_user

    return role_checker


# ロール別ショートカット
def get_current_student(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != RoleEnum.student:
        raise HTTPException(status_code=403, detail="生徒のみ許可されています")
    return current_user


def get_current_teacher(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != RoleEnum.teacher:
        raise HTTPException(status_code=403, detail="教師のみ許可されています")
    return current_user


def get_current_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="管理者のみ許可されています")
    return current_user

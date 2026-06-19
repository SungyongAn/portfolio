from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import hash_password
from typing import List


def create_user(db: Session, user_data: UserCreate) -> UserResponse:
    """ユーザーを作成する"""
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に使用されています",
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        department_id=user_data.department_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


def get_users(db: Session) -> List[UserResponse]:
    """全ユーザー一覧を返す"""
    users = db.query(User).all()
    return [UserResponse.model_validate(u) for u in users]


def get_user_by_id(db: Session, user_id: int) -> UserResponse:
    """IDでユーザーを取得する"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが見つかりません",
        )
    return UserResponse.model_validate(user)


def get_users_by_department(db: Session, department_id: int) -> list[UserResponse]:
    """部門メンバー一覧取得"""
    users = db.query(User).filter(User.department_id == department_id).all()
    return [UserResponse.model_validate(u) for u in users]

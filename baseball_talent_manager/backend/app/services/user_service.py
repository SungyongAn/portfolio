from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import (
    UserCreateRequest,
    UserListItem,
    UserListResponse,
    UserResponse,
    UserStatusUpdateRequest,
)
from app.utils.security import get_password_hash


# ユーザーを作成
def create_user(db: Session, user_data: UserCreateRequest) -> User:
    # メールアドレスを小文字に統一
    email = user_data.email.lower()

    # メールアドレスの重複チェック
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に使用されています",
        )

    # パスワードをハッシュ化
    password_hash = get_password_hash(user_data.password)

    user = User(
        email=email,
        password_hash=password_hash,
        name=user_data.name,
        grade=user_data.grade,
        role=user_data.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# メールアドレスでユーザーを取得
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


# ユーザー一覧を取得
def get_user_list(
    db: Session,
    role: str,
    limit: int = 500,
    offset: int = 0,
) -> UserListResponse:

    query = db.query(
        User.id,
        User.name,
        User.email,
        User.grade,
        User.role,
    )

    if role:
        query = query.filter(User.role == role)

    query = query.filter(User.status == "active")

    results = query.limit(limit).offset(offset).all()

    user_list = [
        UserListItem(
            user_id=row.id,
            email=row.email,
            name=row.name,
            grade=row.grade,
            role=row.role,
        )
        for row in results
    ]
    return UserListResponse(users=user_list)

#　引退・退部処理
def update_user_status(
    db: Session, user_id: int, status_data: UserStatusUpdateRequest
) -> UserResponse:

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたユーザーが存在しません",
        )

    user.status = status_data.status
    db.commit()

    return UserResponse(message="退部・引退に変更しました。")

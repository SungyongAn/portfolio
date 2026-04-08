from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies.auth import require_roles
from app.models.user import User
from app.schemas.user import (
    UserCreateRequest,
    UserListResponse,
    UserResponse,
    UserStatusUpdateRequest,
)
from app.services.user_service import create_user, get_user_list, update_user_status

router = APIRouter(prefix="/api/users", tags=["ユーザー管理"])


# ユーザーを作成
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["coach", "director"])),
):

    # ユーザー作成
    create_user(db, user_data)

    return UserResponse(message="ユーザーを作成しました")


# ユーザー一覧を取得
@router.get("/", response_model=UserListResponse)
def get_users(
    role: str | None = None,
    limit: int = 500,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["manager", "coach", "director"])),
):

    users = get_user_list(db, role=role, limit=limit, offset=offset)

    return users


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status_endpoint(
    user_id: int,
    status_data: UserStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["coach", "director"])),
):

    result = update_user_status(db, user_id, status_data)

    return result

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
import app.services.user_service as user_service
from app.dependencies.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/users", tags=["ユーザー"])


@router.post("", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.HQ_MANAGER])),
):
    """ユーザー作成（本部管理者のみ）"""
    return user_service.create_user(db, user_data)


@router.get("", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.HQ_MANAGER])),
):
    """ユーザー一覧取得（本部管理者のみ）"""
    return user_service.get_users(db)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """ログイン中のユーザー情報取得"""
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.HQ_MANAGER])),
):
    """ユーザー詳細取得（本部管理者のみ）"""
    return user_service.get_user_by_id(db, user_id)


@router.get("/department/{department_id}", response_model=list[UserResponse])
def get_department_users(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """部門メンバー一覧取得"""
    # 本部管理者は全部門を参照可能
    if current_user.role == UserRole.HQ_MANAGER:
        return user_service.get_users_by_department(db, department_id)
    # 部門管理者・申請者・メンバーは自分の部門のみ参照可能
    if current_user.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="他部門のメンバー情報は参照できません",
        )
    return user_service.get_users_by_department(db, department_id)

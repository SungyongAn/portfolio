from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserWithClassResponse
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
    get_students_by_class
)
from app.dependencies import get_current_admin, get_current_user
from app.models.user import User, RoleEnum
from app.models.class_model import StudentClassAssignment
from typing import List

router = APIRouter(prefix="/api/users", tags=["ユーザー管理"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    ユーザーを作成
    
    管理者のみが実行可能。生徒、教師、管理者を作成できる。
    """
    # メールアドレスの重複チェック
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に使用されています"
        )
    
    # ロールのバリデーション
    valid_roles = [role.value for role in RoleEnum]
    if user_data.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"無効なロールです。有効な値: {', '.join(valid_roles)}"
        )
    
    # ユーザー作成
    user = create_user(db, user_data)
    
    return user


@router.get("/", response_model=List[UserResponse])
def get_users(
    role: str = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    ユーザー一覧を取得
    
    管理者のみが実行可能。ロールでフィルタリング可能。
    """
    users = get_all_users(db, role=role, limit=limit, offset=offset)
    return users


@router.get("/students/by-class/{class_id}", response_model=List[UserWithClassResponse])
def get_students_in_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    クラスの生徒一覧を取得
    
    教師、管理者が実行可能。
    """
    if current_user.role not in [RoleEnum.teacher, RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作は教師または管理者のみ実行できます"
        )
    
    students = get_students_by_class(db, class_id)
    
    # クラス情報を追加
    result = []
    for student in students:
        student_class = db.query(StudentClassAssignment).filter(
            StudentClassAssignment.student_id == student.id,
            StudentClassAssignment.class_id == class_id,
            StudentClassAssignment.is_current == True
        ).first()
        
        response = UserWithClassResponse(
            id=student.id,
            email=student.email,
            name=student.name,
            role=student.role.value,
            class_name=student_class.class_obj.class_name if student_class else None,
            grade_number=student_class.class_obj.grade.grade_number if student_class else None,
            created_at=student.created_at
        )
        result.append(response)
    
    return result


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ユーザー情報を取得
    
    自分自身または管理者のみが実行可能。
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが見つかりません"
        )
    
    # 権限チェック: 自分自身または管理者のみ
    if current_user.id != user_id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="他のユーザーの情報を閲覧する権限がありません"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_info(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ユーザー情報を更新
    
    自分自身または管理者のみが実行可能。
    """
    # 権限チェック: 自分自身または管理者のみ
    if current_user.id != user_id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="他のユーザーの情報を更新する権限がありません"
        )
    
    user = update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが見つかりません"
        )
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    ユーザーを削除
    
    管理者のみが実行可能。
    """
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが見つかりません"
        )
    
    return None

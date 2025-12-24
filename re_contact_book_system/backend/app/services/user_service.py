
from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import get_password_hash
from typing import Optional, List


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    ユーザーを作成
    
    Args:
        db: データベースセッション
        user_data: ユーザー作成データ
    
    Returns:
        User: 作成されたユーザー
    """
    # メールアドレスを小文字に統一
    email = user_data.email.lower()
    
    # パスワードをハッシュ化
    password_hash = get_password_hash(user_data.password)
    
    user = User(
        email=email,
        password_hash=password_hash,
        name=user_data.name,
        role=RoleEnum(user_data.role)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    メールアドレスでユーザーを取得
    
    Args:
        db: データベースセッション
        email: メールアドレス
    
    Returns:
        User: ユーザー（見つからない場合はNone）
    """
    return db.query(User).filter(User.email == email.lower()).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    IDでユーザーを取得
    
    Args:
        db: データベースセッション
        user_id: ユーザーID
    
    Returns:
        User: ユーザー（見つからない場合はNone）
    """
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(
    db: Session,
    role: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[User]:
    """
    ユーザー一覧を取得
    
    Args:
        db: データベースセッション
        role: ロールでフィルタ（省略時は全ユーザー）
        limit: 取得件数
        offset: オフセット
    
    Returns:
        List[User]: ユーザーリスト
    """
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    return query.order_by(User.created_at.desc()).limit(limit).offset(offset).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """
    ユーザー情報を更新
    
    Args:
        db: データベースセッション
        user_id: ユーザーID
        user_data: 更新データ
    
    Returns:
        User: 更新されたユーザー
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if user_data.name is not None:
        user.name = user_data.name
    
    if user_data.password is not None:
        user.password_hash = get_password_hash(user_data.password)
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """
    ユーザーを削除
    
    Args:
        db: データベースセッション
        user_id: ユーザーID
    
    Returns:
        bool: 削除成功ならTrue
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True


def get_students_by_class(db: Session, class_id: int) -> List[User]:
    """
    クラスに所属する生徒一覧を取得
    
    Args:
        db: データベースセッション
        class_id: クラスID
    
    Returns:
        List[User]: 生徒リスト
    """
    from app.models.class_model import StudentClassAssignment
    
    return db.query(User).join(
        StudentClassAssignment, User.id == StudentClassAssignment.student_id
    ).filter(
        StudentClassAssignment.class_id == class_id,
        StudentClassAssignment.is_current == True,
        User.role == RoleEnum.student
    ).order_by(User.name).all()

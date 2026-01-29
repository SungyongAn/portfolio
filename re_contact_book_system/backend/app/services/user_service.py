
from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.models.class_model import Class, Grade, StudentClassAssignment, TeacherAssignment
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import get_password_hash
from app.schemas.user import AdminUserListResponse


# ユーザーを作成
def create_user(db: Session, user_data: UserCreate) -> User:
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


# メールアドレスでユーザーを取得
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


# IDでユーザーを取得
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


# ユーザー一覧を取得
def get_admin_user_list(
    db: Session,
    role: str | None = None,
    limit: int = 500,
    offset: int = 0,
) -> list[AdminUserListResponse]:
    query = (
        db.query(
            User.id,
            User.name,
            User.email,
            User.role,
            Class.class_name,
            Grade.grade_number,
            TeacherAssignment.assignment_type
        )
        .outerjoin(
            StudentClassAssignment,
            (StudentClassAssignment.student_id == User.id)
            & (StudentClassAssignment.is_current == True)
        )
        .outerjoin(Class, Class.id == StudentClassAssignment.class_id)
        .outerjoin(Grade, Grade.id == Class.grade_id)
        .outerjoin(
            TeacherAssignment,
            TeacherAssignment.teacher_id == User.id
        )
        .filter(User.role != RoleEnum.admin)
    )

    if role:
        query = query.filter(User.role == role)

    results = query.limit(limit).offset(offset).all()

    base_role_map = {
        'student': '生徒',
        'teacher': '教師',
        'admin': '管理者'
    }

    assignment_map = {
        'homeroom': '担任',
        'vice_homeroom': '副担任',
        'grade_head': '学年主任',
        'subject': '教科担当'
    }

    # ここで role を置き換えてスキーマに整形 
    user_list = []
    for u in results:
        # 教師の場合、assignment_type があれば置き換え
        if u.role == RoleEnum.teacher and u.assignment_type:
            display_role = assignment_map.get(u.assignment_type, '教師')
        else:
            display_role = base_role_map.get(u.role.value, u.role.value)  # student/admin

        user_list.append(AdminUserListResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            role=display_role,
            grade_number=u.grade_number,
            class_name=u.class_name
        ))

    return user_list


# ユーザー情報を更新
def update_user(db: Session, user_id: int, user_data: UserUpdate) ->  User | None:
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


# ユーザーを削除
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True


# クラスに所属する生徒一覧を取得
def get_students_by_class(db: Session, class_id: int) -> list[User]:
    
    return db.query(User).join(
        StudentClassAssignment, User.id == StudentClassAssignment.student_id
    ).filter(
        StudentClassAssignment.class_id == class_id,
        StudentClassAssignment.is_current == True,
        User.role == RoleEnum.student
    ).order_by(User.name).all()

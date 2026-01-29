from sqlalchemy.orm import aliased, Session
from app.models.user import User, RoleEnum
from app.models.class_model import (
    AssignmentTypeEnum,
    Class,
    Grade,
    StudentClassAssignment,
    TeacherAssignment
    )
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import get_password_hash
from app.schemas.user import AdminUserListResponse
from app.models.class_model import 

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
    
    # 教師用の Grade と Class を別名で定義（生徒用と区別するため）
    TeacherGrade = aliased(Grade)
    TeacherClass = aliased(Class)
    
    query = (
        db.query(
            User.id,
            User.name,
            User.email,
            User.role,
            # 生徒用の学年・クラス
            Class.class_name.label('student_class_name'),
            Grade.grade_number.label('student_grade_number'),
            # 教師用の割当情報
            TeacherAssignment.assignment_type,
            TeacherAssignment.is_primary,
            TeacherGrade.grade_number.label('teacher_grade_number'),
            TeacherClass.class_name.label('teacher_class_name'),
        )
        # 生徒のクラス割当
        .outerjoin(
            StudentClassAssignment,
            (StudentClassAssignment.student_id == User.id)
            & (StudentClassAssignment.is_current == True)
        )
        .outerjoin(Class, Class.id == StudentClassAssignment.class_id)
        .outerjoin(Grade, Grade.id == Class.grade_id)
        # 教師の割当（複数ある場合は複数行返る）
        .outerjoin(
            TeacherAssignment,
            TeacherAssignment.teacher_id == User.id
        )
        .outerjoin(TeacherGrade, TeacherGrade.id == TeacherAssignment.grade_id)
        .outerjoin(TeacherClass, TeacherClass.id == TeacherAssignment.class_id)
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
        AssignmentTypeEnum.homeroom: '担任',
        AssignmentTypeEnum.grade_head: '学年主任',
        AssignmentTypeEnum.subject: '教科担当',
        AssignmentTypeEnum.administrator: '管理職',
    }

    # 教師の優先度を定義（数値が小さいほど優先）
    assignment_priority = {
        AssignmentTypeEnum.grade_head: 1,        # 学年主任が最優先
        AssignmentTypeEnum.homeroom: 2,          # 担任が次
        AssignmentTypeEnum.subject: 3,           # 教科担当
        AssignmentTypeEnum.administrator: 4,     # 管理職
    }

    # ユーザーごとにグルーピング
    user_dict = aggregate_users(query)

    # レスポンス用リストを作成
    user_list = build_admin_user_list(
    user_dict: dict[int, dict],
    assignment_priority: dict,
    assignment_map: dict,
    base_role_map: dict,
    )

    return user_list


# ユーザーごとにグルーピング
def aggregate_users(rows) -> dict[int, dict]:
    user_dict = {}

    for row in rows:
        user_id = row.id

        # 初回登録
        if user_id not in user_dict:
            user_dict[user_id] = {
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'role': row.role,
                'student_grade_number': row.student_grade_number,
                'student_class_name': row.student_class_name,
                'teacher_assignments': []
            }

        # 教師の割当情報を追加
        if row.role == RoleEnum.teacher and row.assignment_type:
            user_dict[user_id]['teacher_assignments'].append({
                'assignment_type': row.assignment_type,
                'is_primary': row.is_primary,
                'grade_number': row.teacher_grade_number,
                'class_name': row.teacher_class_name,
            })

    return user_dict


# レスポンス用リストを作成
def build_admin_user_list(
    user_dict: dict[int, dict],
    assignment_priority: dict,
    assignment_map: dict,
    base_role_map: dict,
) -> list[AdminUserListResponse]:

    user_list = []
    
    for user_data in user_dict.values():
        role = user_data['role']

        # 生徒の場合
        if role == RoleEnum.student:
            display_role = base_role_map['student']
            grade_number = user_data['student_grade_number']
            class_name = user_data['student_class_name']

        # 教師の場合
        elif role == RoleEnum.teacher:
            display_role, grade_number, class_name = resolve_teacher_display(
                user_data['teacher_assignments'],
                assignment_priority,
                assignment_map,
            )

        else:
            display_role = base_role_map.get(role.value, role.value)
            grade_number = None
            class_name = None

        user_list.append(
            AdminUserListResponse(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                role=display_role,
                grade_number=grade_number,
                class_name=class_name,
            )
        )

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
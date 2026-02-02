
from sqlalchemy.orm import Session, aliased
from app.models.user import User, RoleEnum
from app.models.class_model import (
    Class,
    Grade,
    StudentClassAssignment,
    TeacherAssignment,
    AssignmentTypeEnum
    )
from app.schemas.user import UserCreate, UserUpdate
from app.utils.password_utils import get_password_hash, verify_password
from app.schemas.user import AdminUserListResponse


# メールアドレス・パスワードでユーザーを認証
def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user

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


# user_id 単位で
def aggregate_admin_user_rows(results):
    user_dict: dict[int, dict] = {}

    for row in results:
        user_id = row.id

        if user_id not in user_dict:
            user_dict[user_id] = {
                "id": row.id,
                "name": row.name,
                "email": row.email,
                "role": row.role,
                "student_grade_number": row.student_grade_number,
                "student_class_name": row.student_class_name,
                "teacher_assignments": [],
            }

        if row.role == RoleEnum.teacher and row.assignment_type:
            user_dict[user_id]["teacher_assignments"].append({
                "assignment_type": row.assignment_type,
                "is_primary": row.is_primary,
                "grade_number": row.teacher_grade_number,
                "class_name": row.teacher_class_name,
            })

    return user_dict


# 教師の割当一覧から表示用 role / grade / class を決定
def resolve_teacher_display_role(assignments):

    if not assignments:
        return "教師", None, None

    assignment_priority = {
        AssignmentTypeEnum.grade_head: 1,
        AssignmentTypeEnum.homeroom: 2,
        AssignmentTypeEnum.subject: 3,
        AssignmentTypeEnum.administrator: 4,
    }

    assignment_map = {
        AssignmentTypeEnum.homeroom: "担任",
        AssignmentTypeEnum.grade_head: "学年主任",
        AssignmentTypeEnum.subject: "教科担当",
        AssignmentTypeEnum.administrator: "管理職",
    }

    sorted_assignments = sorted(
        assignments,
        key=lambda x: (
            assignment_priority.get(x["assignment_type"], 99),
            not x["is_primary"],
        )
    )

    primary = sorted_assignments[0]

    role_label = assignment_map.get(primary["assignment_type"], "教師")

    if (
        primary["assignment_type"] == AssignmentTypeEnum.homeroom
        and not primary["is_primary"]
    ):
        role_label = "副担任"

    return role_label, primary["grade_number"], primary["class_name"]



def build_admin_user_list(user_dict):
    base_role_map = {
        RoleEnum.student: "生徒",
        RoleEnum.teacher: "教師",
        RoleEnum.admin: "管理者",
    }

    user_list: list[AdminUserListResponse] = []

    for user in user_dict.values():
        if user["role"] == RoleEnum.student:
            display_role = base_role_map[RoleEnum.student]
            grade_number = user["student_grade_number"]
            class_name = user["student_class_name"]

        elif user["role"] == RoleEnum.teacher:
            display_role, grade_number, class_name = resolve_teacher_display_role(
                user["teacher_assignments"]
            )

        else:
            display_role = base_role_map.get(user["role"], user["role"].value)
            grade_number = None
            class_name = None

        user_list.append(
            AdminUserListResponse(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                role=display_role,
                grade_number=grade_number,
                class_name=class_name,
            )
        )

    return user_list


# ユーザー一覧を取得
def get_admin_user_list(
    db: Session,
    role: str | None = None,
    limit: int = 500,
    offset: int = 0,
) -> list[AdminUserListResponse]:


    TeacherGrade = aliased(Grade)
    TeacherClass = aliased(Class)

    query = (
        db.query(
            User.id,
            User.name,
            User.email,
            User.role,
            Class.class_name.label("student_class_name"),
            Grade.grade_number.label("student_grade_number"),
            TeacherAssignment.assignment_type,
            TeacherAssignment.is_primary,
            TeacherGrade.grade_number.label("teacher_grade_number"),
            TeacherClass.class_name.label("teacher_class_name"),
        )
        .outerjoin(
            StudentClassAssignment,
            (StudentClassAssignment.student_id == User.id)
            & (StudentClassAssignment.is_current == True),
        )
        .outerjoin(Class, Class.id == StudentClassAssignment.class_id)
        .outerjoin(Grade, Grade.id == Class.grade_id)
        .outerjoin(TeacherAssignment, TeacherAssignment.teacher_id == User.id)
        .outerjoin(TeacherGrade, TeacherGrade.id == TeacherAssignment.grade_id)
        .outerjoin(TeacherClass, TeacherClass.id == TeacherAssignment.class_id)
        .filter(User.role != RoleEnum.admin)
    )

    if role:
        query = query.filter(User.role == role)

    results = query.limit(limit).offset(offset).all()

    user_dict = aggregate_admin_user_rows(results)
    return build_admin_user_list(user_dict)


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


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
from app.schemas.user import (
    AdminUserListResponse, 
    StudentClassSummary,
    UserPrimaryAssignment, 
    TeacherAssignmentSummary
    )


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
                "permission_level": row.permission_level,
            })

    return user_dict



# 教師の割当一覧から表示用 role / grade / class を決定
def resolve_teacher_primary_assignment(
    assignments: list[TeacherAssignmentSummary],
) -> UserPrimaryAssignment | None:

    if not assignments:
        return None

    assignment_priority = {
        AssignmentTypeEnum.grade_head: 1,
        AssignmentTypeEnum.homeroom: 2,
        AssignmentTypeEnum.subject: 3,
    }

    sorted_assignments = sorted(
        assignments,
        key=lambda x: (
            assignment_priority.get(x.assignment_type, 99),
            not x.is_primary,
        )
    )

    primary = sorted_assignments[0]

    return UserPrimaryAssignment(
        assignment_type=primary.assignment_type,
        grade_number=primary.grade_number,
        class_name=primary.class_name,
    )



def build_admin_user_list(user_dict):
    user_list: list[AdminUserListResponse] = []

    for user in user_dict.values():
        if user["role"] == RoleEnum.student:
            student_class = (
                StudentClassSummary(
                    grade_number=user["student_grade_number"],
                    class_name=user["student_class_name"]
                )
                if user["student_grade_number"] is not None else None
            )
            primary_assignment = None

        elif user["role"] == RoleEnum.teacher:
            teacher_assignments = [
                TeacherAssignmentSummary.model_validate(a)
                for a in user["teacher_assignments"]
                ]
            primary_assignment = resolve_teacher_primary_assignment(
                teacher_assignments
                )

            student_class = None

        else:
            # 管理者
            student_class = None
            primary_assignment = None

        user_list.append(
            AdminUserListResponse(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                role=user["role"],
                student_class=student_class,
                primary_assignment=primary_assignment,
                teacher_assignments=user["teacher_assignments"],
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
            TeacherAssignment.permission_level,
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


def get_student_class_summary(db: Session, user_id: int):
    row = (
        db.query(
            Grade.grade_number,
            Class.class_name,
        )
        .join(StudentClassAssignment, StudentClassAssignment.class_id == Class.id)
        .join(Grade, Grade.id == Class.grade_id)
        .filter(
            StudentClassAssignment.student_id == user_id,
            StudentClassAssignment.is_current == True,
        )
        .first()
    )

    if not row:
        return None

    return {
        "grade_number": row.grade_number,
        "class_name": row.class_name,
    }



def get_teacher_assignment_summaries(db: Session, user_id: int):
    rows = (
        db.query(
            TeacherAssignment.assignment_type,
            TeacherAssignment.is_primary,
            TeacherAssignment.permission_level,
            Grade.grade_number,
            Class.class_name,
        )
        .outerjoin(Grade, Grade.id == TeacherAssignment.grade_id)
        .outerjoin(Class, Class.id == TeacherAssignment.class_id)
        .filter(TeacherAssignment.teacher_id == user_id)
        .all()
    )

    return [
        TeacherAssignmentSummary(
            assignment_type=r.assignment_type,
            is_primary=r.is_primary,
            permission_level=r.permission_level,
            grade_number=r.grade_number,
            class_name=r.class_name,
        )
        for r in rows
    ]

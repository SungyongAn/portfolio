from app.models.class_model import AssignmentTypeEnum, PermissionLevelEnum
from app.models.user import RoleEnum
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ログインリクエスト
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=6, description="パスワード")


# クラス情報付きユーザーレスポンス
class UserWithClassResponse(BaseModel):
    id: int
    email: str
    name: str
    role: RoleEnum
    class_name: str | None = None
    grade_number: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True

# 生徒のユーザー情報取得時の学年、クラス情報
class StudentClassSummary(BaseModel):
    grade_number: int
    class_name: str

    class Config:
        from_attributes = True


# 教師のユーザー情報取得時の情報
class TeacherAssignmentSummary(BaseModel):
    grade_number: int | None = None
    class_name: str | None = None

    assignment_type: AssignmentTypeEnum  # homeroom / subject / grade_head
    is_primary: bool
    permission_level: PermissionLevelEnum

    class Config:
        from_attributes = True

class UserPrimaryAssignment(BaseModel):
    assignment_type: AssignmentTypeEnum  # homeroom / subject / grade_head
    grade_number: int | None = None
    class_name: str | None = None

    class Config:
        from_attributes = True

# ログインレスポンス
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

    user_id: int
    name: str
    role: RoleEnum

    # 学籍・担当情報（ロールによって使い分け）
    student_class: StudentClassSummary | None = None
    
    # 教師の場合の代表割当（一覧表示用）
    primary_assignment: UserPrimaryAssignment | None = None

    # 教師の場合の全割当（編集・詳細画面用）
    teacher_assignments: list[TeacherAssignmentSummary] = Field(default_factory=list)


# トークンリフレッシュレスポンス
class TokenRefreshResponse(BaseModel):
    access_token: str = Field(..., description="新しいアクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    expires_in: int = Field(..., description="有効期限（秒）")


# ユーザー作成リクエスト
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=6, description="パスワード")
    name: str = Field(..., min_length=1, max_length=100, description="氏名")
    role: str = Field(..., description="ユーザーロール (student/teacher/admin)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@school.ac.jp",
                "password": "password123",
                "name": "山田 太郎",
                "role": "student"
            }
        }


# ユーザー更新リクエスト
class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100, description="氏名")
    password: str | None = Field(None, min_length=6, description="新しいパスワード")


# ユーザー情報レスポンス
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True


# 管理者権限でのユーザー検索
class AdminUserListResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum  # student / teacher / admin

    # 生徒の場合のクラス情報
    student_class: StudentClassSummary | None = None

    # 教師の場合の代表割当（一覧表示用）
    primary_assignment: UserPrimaryAssignment | None = None

    # 教師の場合の全割当（編集・詳細画面用）
    teacher_assignments: list[TeacherAssignmentSummary] = Field(default_factory=list)

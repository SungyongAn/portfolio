from pydantic import BaseModel, ConfigDict


# アカウント登録リクエスト
class AccountRegisterRequest(BaseModel):
    role: str
    name: str
    grade: int
    class_name: str
    password: str
    enrollment_year: int
    graduation_year: int | None = None
    teacher_role: str | None = None  # ✅ codeで受け取る
    subject: str | None = None       # ✅ codeで受け取る


class AccountData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    role: str
    grade: int
    class_name: str
    enrollment_year: int
    graduation_year: int
    status: str
    teacher_role: str | None = None
    subject: str | None = None


class AccountRegisterResponse(BaseModel):
    success: bool
    message: str
    data: AccountData | None = None


# アカウント検索
class AccountSearchPayload(BaseModel):
    studentStaffNumber: str | None = None
    role: str | None = None
    fullName: str | None = None
    grade: int | None = None
    class_name: str | None = None
    teacher_role: str | None = None  # codeで受け取る
    subject: str | None = None       # codeで受け取る
    enrollment_year: int | None = None
    status: str | None = None


class AccountSearchResponse(BaseModel):
    success: bool
    message: str | None = None
    data: list[dict] | None = None


# アカウント更新用
class AccountUpdatePayload(BaseModel):
    id: int
    role: str
    fullName: str
    grade: int
    className: str
    status: str
    teacher_role: str | None = None  # ✅ codeで受け取る
    subject: str | None = None       # ✅ codeで受け取る
    enrollmentYear: int | None = None


class AccountUpdateResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None

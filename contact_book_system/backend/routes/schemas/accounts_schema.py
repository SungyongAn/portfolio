from pydantic import BaseModel, ConfigDict


# アカウント登録リクエスト
class AccountRegisterRequest(BaseModel):
    role: str
    email: str
    last_name: str
    first_name: str
    grade: int
    class_name: str
    password: str
    enrollment_year: int
    graduation_year: int | None = None
    teacher_role: str | None = None  
    subject: str | None = None       


class AccountData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: str
    last_name: str
    first_name: str
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
    email: str | None = None
    role: str | None = None
    last_name: str | None = None
    first_name: str | None = None
    grade: int | None = None
    class_name: str | None = None
    teacher_role: str | None = None
    subject: str | None = None
    enrollment_year: int | None = None
    status: str | None = None


class AccountSearchResponse(BaseModel):
    success: bool
    message: str | None = None
    data: list[dict] | None = None


# アカウント更新用
class AccountUpdatePayload(BaseModel):
    email: str
    role: str
    last_name: str
    first_name: str
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

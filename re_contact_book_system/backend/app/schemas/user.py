from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ログインリクエスト
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=6, description="パスワード")


# ログインレスポンス
class LoginResponse(BaseModel):
    token: str = Field(..., description="JWTトークン")
    role: str = Field(..., description="ユーザーロール")
    name: str = Field(..., description="ユーザー名")
    user_id: int = Field(..., description="ユーザーID")


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
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# クラス情報付きユーザーレスポンス
class UserWithClassResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    class_name: str | None = None
    grade_number: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True

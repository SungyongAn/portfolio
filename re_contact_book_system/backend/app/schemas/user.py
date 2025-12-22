from pydantic import BaseModel, EmailStr
from datetime import datetime


# ログインリクエスト
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ログインレスポンス
class LoginResponse(BaseModel):
    token: str
    role: str
    name: str


# ユーザー作成
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str


# ユーザー情報
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # SQLAlchemyモデルから変換可能に

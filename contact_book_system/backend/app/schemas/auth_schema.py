from pydantic import BaseModel, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = None


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetResponse(BaseModel):
    success: bool
    message: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class PasswordResetToken(BaseModel):
    """データベースに保存するトークン情報"""
    id: int | None = None
    email: str
    token: str
    created_at: datetime
    expires_at: datetime
    used: bool = False

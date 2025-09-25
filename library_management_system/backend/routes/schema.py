from pydantic import BaseModel
from typing import Optional


class LoginRequestPayload(BaseModel):
    userId: str
    password: str


class LoginResponseGeneric(BaseModel):
    success: bool
    authority: Optional[str] = None  # 認証成功時のみ返す
    username: Optional[str] = None  # 認証成功時のみ返す
    affiliation: Optional[str] = None  # 認証成功時のみ返す
    message: Optional[str] = None    # 認証失敗時のエラーメッセージ


# 初回認証
class FirstAuthRequestPayload(BaseModel):
    userId: str
    email: str


class FirstAuthResponseGeneric(BaseModel):
    success: bool
    username: Optional[str] = None
    message: Optional[str] = None


# パスワード登録
class SetPassRequestPayload(BaseModel):
    userId: str
    password: str


class SetPassResponseGeneric(BaseModel):
    success: bool
    message: str


# ユーザー登録
class UsersRegisterPayload(BaseModel):
    user_id: list[str]
    username: list[str]
    admission_year: list[int]
    graduation_year: list[int]
    email: list[str]
    affiliation: list[str]


# ユーザー情報のスキーマ
class UserInfo(BaseModel):
    userId: str
    username: str
    admission_year: int
    graduation_year: int
    email: str
    affiliation: str


class UsersRegisterGeneric(BaseModel):
    success: bool
    message: str
    users: Optional[list[UserInfo]] = None

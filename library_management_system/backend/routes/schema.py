from pydantic import BaseModel
from typing import Optional


class LoginRequestPayload(BaseModel):
    userId: str
    password: str


class LoginResponseGeneric(BaseModel):
    success: bool
    authority: Optional[str] = None  # 認証成功時のみ返す
    username: Optional[str] = None  # 認証成功時のみ返す
    message: Optional[str] = None    # 認証失敗時のエラーメッセージ


# 初回認証
class FirstAuthRequestPayload(BaseModel):
    userId: str
    email: str


class FirstAuthResponseGeneric(BaseModel):
    success: bool
    username: Optional[str] = None
    message: Optional[str] = None  # エラーメッセージ用


# パスワード登録
class SetPassRequestPayload(BaseModel):
    userId: str
    password: str


class SetPassResponseGeneric(BaseModel):
    success: bool
    message: str

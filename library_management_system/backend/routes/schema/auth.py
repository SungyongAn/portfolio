from pydantic import BaseModel
from typing import Optional


# ログイン受信
class LoginRequestPayload(BaseModel):
    userId: str
    password: str


# ログイン送信
class LoginResponseGeneric(BaseModel):
    success: bool
    authority: Optional[str] = None  # 認証成功時のみ返す
    username: Optional[str] = None  # 認証成功時のみ返す
    affiliation: Optional[str] = None  # 認証成功時のみ返す
    message: Optional[str] = None    # 認証失敗時のエラーメッセージ


# 初回認証受信
class FirstAuthRequestPayload(BaseModel):
    userId: str
    email: str


# 初回認証送信
class FirstAuthResponseGeneric(BaseModel):
    success: bool
    username: Optional[str] = None
    message: Optional[str] = None


# パスワード登録受信
class SetPassRequestPayload(BaseModel):
    userId: str
    password: str


# パスワード登録送信
class SetPassResponseGeneric(BaseModel):
    success: bool
    message: str


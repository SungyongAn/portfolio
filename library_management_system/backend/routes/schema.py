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

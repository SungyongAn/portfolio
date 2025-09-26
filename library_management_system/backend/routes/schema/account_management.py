from pydantic import BaseModel
from typing import Optional


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


class UsersRegisterResponseGeneric(BaseModel):
    success: bool
    message: str
    users: Optional[list[UserInfo]] = None


# ユーザー情報の抽出（ユーザー検索用）
class SearchConditions(BaseModel):
    userId: Optional[str] = None
    username: Optional[str] = None
    admission_year: Optional[int] = None
    graduation_year: Optional[int] = None
    email: Optional[str] = None
    affiliation: Optional[str] = None


# ユーザー検索
class SearchAccountsPayload(BaseModel):
    filters: list[SearchConditions]


# フロントに返すユーザー情報
class SerchUserInfo(BaseModel):
    user_id: str
    username: str
    email: str
    admission_year: int
    graduation_year: int
    affiliation: str
    role: str


class SearchAccountsResponseGeneric(BaseModel):
    users_list: list[SerchUserInfo]


# ユーザー情報削除
class DeleteUsersPayload(BaseModel):
    user_ids: list[str]


class DeleteUsersResponseGeneric(BaseModel):
    success: bool
    message: str

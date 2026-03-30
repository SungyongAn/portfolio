from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    grade: int | None = None
    role: str
    password: str


class UserResponse(BaseModel):
    message: str


class UserListItem(BaseModel):
    user_id: int
    email: EmailStr
    name: str
    grade: int | None = None
    role: str
    status: str
    status_changed_at: datetime | None = None


class UserListResponse(BaseModel):
    users: list[UserListItem]


class UserStatusUpdateRequest(BaseModel):
    status: str

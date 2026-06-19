from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    department_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    department_id: Optional[int] = None

    model_config = {"from_attributes": True}

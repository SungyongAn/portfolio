from pydantic import BaseModel


class FirstLoginRequest(BaseModel):
    userId: str
    email: str


class LoginRequest(BaseModel):
    userId: str
    password: str


class UserResponse(BaseModel):
    success: bool
    message: str
    user_id: str

from pydantic import BaseModel


class LoginRequest(BaseModel):
    id: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = None

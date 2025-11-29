from pydantic import BaseModel


class LoginRequest(BaseModel):
    id: int
    name: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = None

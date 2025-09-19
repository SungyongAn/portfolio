from pydantic import BaseModel


class LoginRequestPayload(BaseModel):
    userId: str
    password: str


class LoginResponseGeneric(BaseModel):
    authority: str

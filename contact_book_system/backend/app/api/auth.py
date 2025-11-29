from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services import auth
from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse
)

router = APIRouter()


# ログイン
@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    result = auth.authenticate_user(db, login_data)
    print(result)
    return result

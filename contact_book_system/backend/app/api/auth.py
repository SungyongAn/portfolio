from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services import auth
from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordResetConfirm
)

router = APIRouter()


# ログイン
@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    result = auth.authenticate_user(db, login_data)
    return result


# パスワードリセット要求
@router.post("/password-reset-request", response_model=PasswordResetResponse)
def password_reset_request(request: PasswordResetRequest, db: Session = Depends(get_db)):
    result = auth.password_reset_request(request, db)
    return result


# トークン検証
@router.get("/password-reset-verify/{token}")
def verify_reset_token(token: str, db: Session = Depends(get_db)):
    result = auth.verify_reset_token(token, db)
    return result


# パスワードリセット実行
@router.post("/password-reset-confirm", response_model=PasswordResetResponse)
def password_reset_confirm(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    result = auth.password_reset_confirm(request, db)
    return result

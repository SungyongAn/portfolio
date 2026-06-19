from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["認証"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ログイン"""
    return auth_service.login(db, request)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    """アクセストークンのリフレッシュ"""
    return auth_service.refresh_access_token(db, request.refresh_token)

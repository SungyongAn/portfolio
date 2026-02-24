from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.user import LoginRequest, LoginResponse, TokenRefreshResponse
from app.services.auth_service import (
    login_user,
    refresh_access_token,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["認証"],
)


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    return login_user(db, request, response)


@router.post("/refresh", response_model=TokenRefreshResponse)
def refresh(
    request: Request,
):
    return refresh_access_token(request)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "ログアウトしました"}

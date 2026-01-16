from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import LoginRequest, LoginResponse, TokenRefreshResponse
from app.services.auth_service import (
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    decode_access_token
)

router = APIRouter(prefix="/api/auth", tags=["認証"])

# ログイン
@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)):

    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています"
        )
    
    # トークン生成
    token_data = {
        "sub": user.email,
        "role": user.role,
        "user_id": user.id
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # 🔐 リフレッシュトークンを Cookie に保存
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,          # 本番では True（HTTPS）
        samesite="Lax",
        max_age=60 * 60 * 24 * 7  # 7日
    )

    # アクセストークンのみを返す
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=900,
        role=user.role,
        name=user.name,
        user_id=user.id
    )


# トークンのリフレッシュ
@router.post("/refresh", response_model=TokenRefreshResponse)
def refresh_token(request: Request, db: Session = Depends(get_db)):

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="リフレッシュトークンがありません"
        )
    
    payload = decode_access_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なリフレッシュトークンです"
        )
    
    # 新しいアクセストークンを発行
    token_data = {
        "sub": payload.get("sub"),
        "role": payload.get("role"),
        "user_id": payload.get("user_id")
    }
    
    new_access_token = create_access_token(token_data)
    
    return TokenRefreshResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=900
    )


# ログアウト
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "ログアウトしました"}
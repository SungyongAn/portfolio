from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import LoginRequest, LoginResponse, UserResponse
from app.services.auth_service import authenticate_user, create_access_token
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["認証"])


# メールアドレスとパスワードでログインし、JWTトークンを取得
@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWTトークン生成
    token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )
    
    return LoginResponse(
        token=token,
        role=user.role.value,
        name=user.name,
        user_id=user.id
    )


# JWTトークンからログイン中のユーザー情報の取得
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout():
    return {"message": "ログアウトしました。クライアント側でトークンを削除してください。"}

from fastapi import HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenRefreshResponse,
)
from app.utils.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)


# ログイン処理
def login_user(
    db: Session,
    request: LoginRequest,
    response: Response,
) -> LoginResponse:

    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています",
        )

    token_data = {
        "sub": user.email,
        "role": user.role,
        "user_id": user.id,
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7,
    )
    

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.id,
        name=user.name,
        grade=user.grade,
        role=user.role,
    )


# リフレッシュトークンからアクセストークンを再発行
def refresh_access_token(
    request: Request,
) -> TokenRefreshResponse:

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="リフレッシュトークンがありません",
        )

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なリフレッシュトークンです",
        )

    token_data = {
        "sub": payload.get("sub"),
        "role": payload.get("role"),
        "user_id": payload.get("user_id"),
    }

    new_access_token = create_access_token(token_data)

    return TokenRefreshResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# メールアドレス・パスワードでユーザーを認証
def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None
    return user

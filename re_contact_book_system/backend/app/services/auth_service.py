from fastapi import HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from app.schemas.user import LoginRequest, LoginResponse, TokenRefreshResponse
from app.services.user_service import authenticate_user
from app.utils.token_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
)

ACCESS_TOKEN_EXPIRE_SECONDS = 900  # 15分

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

    # リフレッシュトークンは Cookie に保存
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # 本番では True
        samesite="Lax",
        max_age=60 * 60 * 24 * 7,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
        role=user.role,
        name=user.name,
        user_id=user.id,
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
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )

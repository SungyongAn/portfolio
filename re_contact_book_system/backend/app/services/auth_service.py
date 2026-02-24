from fastapi import HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.schemas.user import (
    LoginRequest,
    LoginResponse,
    RoleEnum,
    TokenRefreshResponse,
    UserPrimaryAssignment
    )
from app.services.user_service import (
    authenticate_user,
    get_student_class_summary,
    get_teacher_assignment_summaries,
    resolve_teacher_primary_assignment,
    )
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

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7,
    )

    student_class = None
    teacher_assignments = []
    primary_assignment = None

    if user.role == RoleEnum.student:
        student_class = get_student_class_summary(db, user.id)

    elif user.role == RoleEnum.teacher:

        teacher_assignments = get_teacher_assignment_summaries(db, user.id)

        primary_assignment = resolve_teacher_primary_assignment(teacher_assignments)

    return LoginResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
        user_id=user.id,
        name=user.name,
        role=user.role,
        student_class=student_class,
        primary_assignment=primary_assignment,
        teacher_assignments=teacher_assignments,
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

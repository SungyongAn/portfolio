from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from routes import auth_service, first_login
from routes.db import get_db
from routes.schema import (
    LoginRequestPayload,
    LoginResponseGeneric,
    FirstAuthRequestPayload,
    FirstAuthResponseGeneric,
    SetPassRequestPayload,
    SetPassResponseGeneric,
)

router = APIRouter()


# ログイン処理
@router.post("/login", response_model=LoginResponseGeneric)
def login(request: LoginRequestPayload, db: Session = Depends(get_db)):
    try:
        # 認証処理
        result = auth_service.authenticate(
            db=db,
            user_id=request.userId,
            password=request.password
        )

        if result["success"]:
            return LoginResponseGeneric(
                success=True,
                authority=result["role"],
                username=result["username"],
                )
        else:
            return LoginResponseGeneric(success=False, message="ユーザーIDまたはパスワードが違います")

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ログイン処理中にエラーが発生しました"
        )


# 初回パスワード設定前の認証
@router.post("/first-auth", response_model=FirstAuthResponseGeneric)
def make_password(request: FirstAuthRequestPayload, db: Session = Depends(get_db)):
    try:
        # 認証処理
        result = first_login.first_authenticate(
            db=db,
            user_id=request.userId,
            e_mail=request.email,
        )

        if result["success"]:
            return FirstAuthResponseGeneric(
                success=True,
                username=result["username"],
                )
        else:
            return FirstAuthResponseGeneric(success=False, message=result["message"])

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="認証処理中にエラーが発生しました"
        )


# 初回認証確認後のパスワード登録
@router.post("/set-password", response_model=SetPassResponseGeneric)
def set_password(request: SetPassRequestPayload, db: Session = Depends(get_db)):
    try:
        # 認証処理
        result = first_login.set_pass(
            db=db,
            user_id=request.userId,
            password=request.password,
        )

        if result["success"]:
            return SetPassResponseGeneric(
                success=True,
                message=result["message"],
                )
        else:
            return SetPassResponseGeneric(success=False, message="message")

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="認証処理中にエラーが発生しました"
        )

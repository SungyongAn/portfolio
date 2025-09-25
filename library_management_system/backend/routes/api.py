from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from routes import auth_service, first_login, account_registration
from routes.db import get_db
from routes.schema import (
    LoginRequestPayload,
    LoginResponseGeneric,
    FirstAuthRequestPayload,
    FirstAuthResponseGeneric,
    SetPassRequestPayload,
    SetPassResponseGeneric,
    UsersRegisterPayload,
    UsersRegisterGeneric,
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
                affiliation=result["affiliation"],
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


@router.post("/users-register", response_model=UsersRegisterGeneric)
def users_register(request: UsersRegisterPayload, db: Session = Depends(get_db)):
    try:
        # リクエストデータをdictに変換
        users_data = []
        for i in range(len(request.user_id)):
            users_data.append({
                "user_id": request.user_id[i],
                "username": request.username[i],
                "admission_year": request.admission_year[i],
                "graduation_year": request.graduation_year[i],
                "email": request.email[i],
                "affiliation": request.affiliation[i]
            })

        # ユーザー登録処理
        result = account_registration.users_register(db=db, users=users_data)
        
        # 成功時も失敗時もフロントにメッセージを返す
        return UsersRegisterGeneric(
            success=result.get("success", False),
            message=result.get("message", ""),
            users=result.get("users", [])  # 空配列でも返す
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"サーバーエラー: {str(e)}"
        )

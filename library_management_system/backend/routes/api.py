from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from routes import auth_service
from routes.db import get_db
from routes.schema import (
    LoginRequestPayload,
    LoginResponseGeneric,
)

router = APIRouter()

@router.post("/login", response_model=LoginResponseGeneric)
def login(request: LoginRequestPayload, db: Session = Depends(get_db)):
    print(f"Login request: userId={request.userId}")  # 追加
    try:
        # 認証処理
        role = auth_service.authenticate(
            db=db,
            user_id=request.userId,
            password=request.password
        )
        print(f"Authentication result: {role}")  # 追加

        if not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザーIDまたはパスワードが違います"
            )

        return LoginResponseGeneric(authority=role)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Detailed error: {e}")  # 追加
        print(f"Error type: {type(e)}")  # 追加
        import traceback
        traceback.print_exc()  # 追加
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ログイン処理中にエラーが発生しました"
        )

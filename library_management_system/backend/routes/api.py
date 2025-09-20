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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routes.db.database import get_db
from routes.services.account_service import AccountService
from routes.schemas.accounts_schema import (
    AccountRegisterRequest,
    AccountRegisterResponse,
    AccountSearchPayload,
    AccountSearchResponse,
    AccountUpdatePayload,
    AccountUpdateResponse
)

router = APIRouter()


# アカウント登録
@router.post("/register", response_model=AccountRegisterResponse)
def register_new_account(register_data: AccountRegisterRequest, db: Session = Depends(get_db)):
    result = AccountService.register_account(db, register_data)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return AccountRegisterResponse(
        success=True,
        message=result["message"],
        data=result["data"]
    )


# アカウント検索
@router.post("/search", response_model=AccountSearchResponse)
def search_accounts(
    payload: AccountSearchPayload, 
    db: Session = Depends(get_db)
):
    try:
        results = AccountService.search_accounts(db, payload)
        
        return AccountSearchResponse(
            success=True,
            message=f"{len(results)}件見つかりました",
            data=results 
        )
    
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="検索に失敗しました"
        )


# アカウント更新
@router.post("/update", response_model=AccountUpdateResponse)
def update_accounts_endpoint(payload: list[AccountUpdatePayload], db: Session = Depends(get_db)):
    result = AccountService.update_accounts(db, payload)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return AccountUpdateResponse(
        success=True,
        message=result["message"],
        data=result["data"]
    )

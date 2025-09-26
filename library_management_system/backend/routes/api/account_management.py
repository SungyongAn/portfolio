from fastapi import APIRouter, Depends, HTTPException, status
from routes.account_management import account_registration
from sqlalchemy.orm import Session
from routes.db import get_db
from routes.schema.account_management import (
    UsersRegisterPayload,
    UsersRegisterResponseGeneric,
    SearchAccountsPayload,
    SearchAccountsResponseGeneric,
    DeleteUsersPayload,
    DeleteUsersResponseGeneric,
)

router = APIRouter()


@router.post("/users-register", response_model=UsersRegisterResponseGeneric)
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
        return UsersRegisterResponseGeneric(
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


# ユーザー情報の検索
@router.post("/search-accounts", response_model=SearchAccountsResponseGeneric)
def search_accounts(request: SearchAccountsPayload, db: Session = Depends(get_db)):

    try:
        # filtersをdictに変換（入力済みの項目だけ）
        filters_data = [f.dict(exclude_unset=True) for f in request.filters]

        # ユーザー検索処理
        users = account_registration.search_accounts(db=db, filters=filters_data)

        # JSON形式に整形して返す
        users_json = [
            {
                "user_id": u.user_id,
                "username": u.username,
                "email": u.email,
                "admission_year": u.admission_year,
                "graduation_year": u.graduation_year,
                "affiliation": u.affiliation,
                "role": u.role
            }
            for u in users
        ]

        return SearchAccountsResponseGeneric(users_list=users_json)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"サーバーエラー: {str(e)}"
        )


# ユーザー情報の削除
@router.post("/delete-users", response_model=DeleteUsersResponseGeneric)
def delete_users_endpoint(payload: DeleteUsersPayload, db: Session = Depends(get_db)):
    result = account_registration.delete_users(db=db, user_ids=payload.user_ids)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

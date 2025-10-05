from fastapi import APIRouter, HTTPException, status
from routes import test
from routes.schema import (
    AllPayload,
    AllResponseGeneric,
)

router = APIRouter()


@router.post("/test", response_model=AllResponseGeneric)
def test_(all_materials: AllPayload):
    """既存のテストエンドポイント"""
    try:
        result = test.test(all_materials)

        # resultの辞書をAllResponseGenericに変換
        return AllResponseGeneric(
            message=result["message"],
            data=result.get("data")  # dataがあれば含める
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="認証処理中にエラーが発生しました",
        )

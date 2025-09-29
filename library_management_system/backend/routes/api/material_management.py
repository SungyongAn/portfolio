from fastapi import APIRouter, Depends, HTTPException, status
from routes.materials import material_management
from sqlalchemy.orm import Session
from routes.db import get_db
from routes.schema.material_management import (
    CheckBarcodePayload,
    CheckBarcodeResponseGeneric,
)

router = APIRouter()


# ログイン処理
@router.post("/check_barcode", response_model=CheckBarcodeResponseGeneric)
def check_barcode(request: CheckBarcodePayload, db: Session = Depends(get_db)):
    try:

        result = material_management.check_barcode(db=db, barcode=request.barcode)

        if result["success"]:
            return CheckBarcodeResponseGeneric(success=True)
        else:
            return CheckBarcodeResponseGeneric(success=False, message=result["message"])

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="認証処理中にエラーが発生しました"
        )

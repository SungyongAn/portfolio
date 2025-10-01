from fastapi import APIRouter, Depends, HTTPException, status
from routes.services.material_service import MaterialService
from sqlalchemy.orm import Session
from routes.db import get_db
from routes.schema.material_management import (
    CheckBarcodePayload,
    CheckBarcodeResponseGeneric,
    MaterialRegisterPayload,
    MaterialRegisterResponseGeneric,
)

router = APIRouter()


# ログイン処理
@router.post("/check_barcode", response_model=CheckBarcodeResponseGeneric)
def check_barcode(request: CheckBarcodePayload, db: Session = Depends(get_db)):
    try:
        
        service = MaterialService(db)
        result = service.check_barcode_available(barcode=request.barcode)

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


@router.post("/register", response_model=MaterialRegisterResponseGeneric)
def material_register(request: MaterialRegisterPayload, db: Session = Depends(get_db)):
    try:
        print(request)
        service = MaterialService(db)
        result = service.register_material(
            barcode=request.barcode,
            title=request.title,
            author=request.author,
            publisher=request.publisher,
            ndc_code=request.ndc_code,
            type_name=request.type_name,
            affiliation=request.affiliation,
            shelf=request.shelf,
        )
        print(db, request.barcode, request.title, request.author, request.publisher, request.ndc_code, request.type_name, request.affiliation, request.shelf)

        if result["success"]:
            return MaterialRegisterResponseGeneric(
                success=True,
                material=result.get("material")
            )
        else:
            return MaterialRegisterResponseGeneric(
                success=False,
                message=result.get("message")
            )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="資料登録処理中にエラーが発生しました"
        )


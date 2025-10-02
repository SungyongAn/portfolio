from fastapi import APIRouter, Depends, HTTPException, status
from routes.services.material_service import MaterialService
from sqlalchemy.orm import Session
from routes.db import get_db
from routes.schema.material_management import (
    CheckBarcodePayload,
    CheckBarcodeResponseGeneric,
    MaterialRegisterPayload,
    MaterialRegisterResponseGeneric,
    MaterialInfo,
)

router = APIRouter()


@router.post("/check_barcode", response_model=CheckBarcodeResponseGeneric)
def check_barcode(request: CheckBarcodePayload, db: Session = Depends(get_db)):
    try:
        service = MaterialService(db)
        result = service.check_barcode_available(barcode=request.barcode)

        return CheckBarcodeResponseGeneric(
            success=result["success"],
            message=result["message"]
        )

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

        if result["success"]:
            material_data = result.get("material")
            
            # MaterialInfo オブジェクトを作成（辞書をアンパック）
            material_info = MaterialInfo(
                material_id=material_data["material_id"],
                barcode=material_data["barcode"],
                title=material_data["title"],
                author=material_data["author"],
                publisher=material_data.get("publisher"),
                ndc_code=material_data["ndc_code"],
                type_name=material_data["type_name"],
                affiliation=material_data["affiliation"],
                shelf=material_data.get("shelf"),
                registration_date=material_data["registration_date"]
            )

            response = MaterialRegisterResponseGeneric(
                success=True,
                material=material_info
            )
            return response
        else:
            return MaterialRegisterResponseGeneric(
                success=False,
                message=result.get("message", "登録に失敗しました")
            )

    except HTTPException:
        raise

    except Exception as e:
        print(f"ルーターエラー: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"資料登録処理中にエラーが発生しました: {str(e)}"
        )

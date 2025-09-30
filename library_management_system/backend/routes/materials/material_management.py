from sqlalchemy.orm import Session
from routes.models import materials


# バーコードの重複確認
def check_barcode(db: Session, barcode: str):

    existing_material = db.query(materials.Material).filter(
        materials.Material.barcode == barcode,
        ).first()

    # ユーザーID、パスワードが一致しない場合
    if existing_material:
        return {"success": False, "message": "このバーコードは使用されています。"}

    return {"success": True}

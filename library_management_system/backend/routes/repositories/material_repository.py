from sqlalchemy.orm import Session
from typing import Optional
from routes.models.materials import Material


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    # バーコード検索
    def find_by_barcode(self, barcode: str) -> Optional[Material]:
        return self.db.query(Material).filter(
            Material.barcode == barcode
        ).first()

    # バーコードの重複チェック
    def exists_by_barcode(self, barcode: str) -> bool:
        return self.db.query(Material).filter(
            Material.barcode == barcode
        ).first() is not None

    # 資料の新規登録
    def create(self, material: Material) -> Material:
        self.db.add(material)
        self.db.flush()
        self.db.refresh(material)
        return material

    # 資料情報の取得
    def find_all(self, skip: int = 0, limit: int = 100) -> list[Material]:
        return self.db.query(Material).offset(skip).limit(limit).all()

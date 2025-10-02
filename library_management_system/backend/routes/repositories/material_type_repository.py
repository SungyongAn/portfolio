from sqlalchemy.orm import Session
from typing import Optional
from routes.models.materials import MaterialType


class MaterialTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    # 種別名検索
    def find_by_name(self, type_name: str) -> Optional[MaterialType]:
        return self.db.query(MaterialType).filter(
            MaterialType.type_name == type_name
        ).first()

    # 種別で検索
    def find_by_id(self, type_id: int) -> Optional[MaterialType]:
        return self.db.query(MaterialType).filter(
            MaterialType.type_id == type_id
        ).first()

    # 全件取得（追加）
    def find_all(self) -> list[MaterialType]:
        return self.db.query(MaterialType).order_by(MaterialType.type_id).all()

from sqlalchemy.orm import Session
from typing import Optional, Dict
from routes.repositories.material_repository import MaterialRepository
from routes.repositories.material_type_repository import MaterialTypeRepository
from routes.models.materials import Material


class MaterialService:
    def __init__(self, db: Session):
        self.material_repo = MaterialRepository(db)
        self.type_repo = MaterialTypeRepository(db)
        self.db = db

    # バーコードの重複確認
    def check_barcode_available(self, barcode: str) -> Dict:
        # 文字数制限確認
        if len(barcode) > 50:
            return {
                "success": False,
                "message": "バーコードは50文字以内で入力してください。",
            }

        # バーコードの重複確認
        exists = self.material_repo.exists_by_barcode(barcode)

        if exists:
            return {
                "success": False,
                "message": "このバーコードは既に使用されています。",
            }

        return {"success": True, "message": "このバーコードは使用可能です。"}

    # 資料登録
    def register_material(
        self,
        barcode: str,
        title: str,
        author: str,
        type_name: str,
        publisher: str = None,
        ndc_code: str = "999",
        affiliation: str = "A校",
        shelf: str = None,
    ) -> Dict:
        # 入力バリデーション
        if not title or not title.strip():
            return {"success": False, "message": "タイトルは必須です。"}

        if not author or not author.strip():
            return {"success": False, "message": "著者は必須です。"}

        # type_name から type_id を取得
        material_type = self.type_repo.find_by_name(type_name)
        if not material_type:
            return {
                "success": False,
                "message": f"種別「{type_name}」が見つかりません。",
            }

        type_id = material_type.type_id

        # Materialオブジェクト作成
        material = Material(
            barcode=barcode.strip(),
            title=title.strip(),
            author=author.strip(),
            publisher=publisher.strip() if publisher else None,
            ndc_code=ndc_code,
            type_id=type_id,
            affiliation=affiliation,
            shelf=shelf.strip() if shelf else None,
            loan_status="AVAILABLE",
        )

        # 保存（リポジトリ内でflushとrefreshが実行される）
        created_material = self.material_repo.create(material)

        self.db.commit()

        material_dict = {
            "material_id": created_material.material_id,
            "barcode": created_material.barcode,
            "title": created_material.title,
            "author": created_material.author,
            "publisher": created_material.publisher,
            "ndc_code": created_material.ndc_code,
            "type_name": type_name,
            "affiliation": created_material.affiliation,
            "shelf": created_material.shelf,
            "registration_date": created_material.registration_date.isoformat()
            if created_material.registration_date
            else None,
        }

        result = {
            "success": True,
            "message": "資料が正常に登録されました。",
            "material": material_dict,
        }
        return result

    # 資料検索
    def search_material(
        self,
        material_id: Optional[int] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        publisher: Optional[str] = None,
    ) -> list[Material]:
        query = self.db.query(Material)

        if material_id:
            query = query.filter(Material.material_id == material_id)
        if title:
            query = query.filter(Material.title == title)
        if author:
            query = query.filter(Material.author == author)
        if publisher:
            query = query.filter(Material.publisher == publisher)

        result = query.all()

        if not result:  # 一致するものがない場合
            return {
                "success": False,
                "message": "条件に一致する資料は見つかりませんでした。",
                "materials": [],
            }
        # 結果がある場合は辞書に変換して返す
        materials_list = [
            {
                "material_id": m.material_id,
                "barcode": m.barcode,
                "title": m.title,
                "author": m.author,
                "publisher": m.publisher,
                "ndc_code": m.ndc_code,
                "type_id": m.type_id,
                "affiliation": m.affiliation,
                "shelf": m.shelf,
                "loan_status": m.loan_status,
                "registration_date": m.registration_date.isoformat()
                if m.registration_date
                else None,
            }
            for m in result
        ]

        return {
            "success": True,
            "message": f"{len(materials_list)}件の資料が見つかりました。",
            "materials": materials_list,
        }

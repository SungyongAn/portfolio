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

    # バーコードの重複確認、手入時に文字数制限を超えていないか確認
    def check_barcode_available(self, barcode: str) -> Dict:

        # 文字数制限確認
        if len(barcode) > 50:
            return {
                "success": False,
                "message": "バーコードは50文字以内で入力してください。"
            }

        # バーコードの重複確認
        exists = self.material_repo.exists_by_barcode(barcode)

        if exists:
            return {
                "success": False,
                "message": "このバーコードは既に使用されています。"
            }
        
        return {
            "success": True,
            "message": "このバーコードは使用可能です。"
        }

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

        try:
            # 必須項目チェック
            if not title or not title.strip():
                return {
                    "success": False,
                    "message": "タイトルは必須です。"
                }
            
            if not author or not author.strip():
                return {
                    "success": False,
                    "message": "著者は必須です。"
                }
            
            # 種別名から種別IDを取得（別のRepositoryを使用）
            material_type = self.type_repo.find_by_name(type_name)
            
            if not material_type:
                return {
                    "success": False,
                    "message": f"種別「{type_name}」が見つかりません。"
                }
            
            # Materialオブジェクト作成
            material = Material(
                barcode=barcode.strip(),
                title=title.strip(),
                author=author.strip(),
                publisher=publisher.strip() if publisher else None,
                ndc_code=ndc_code,
                type_id=material_type.type_id,
                affiliation=affiliation,
                shelf=shelf.strip() if shelf else None,
                loan_status="AVAILABLE",  # デフォルト値
            )
            
            # 保存（Repositoryを使用）
            created_material = self.material_repo.create(material)
            
            # レスポンス用に変換
            return {
                "success": True,
                "message": "資料が正常に登録されました。",
                "material": self._to_dict(created_material)
            }
        
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"登録中にエラーが発生しました: {str(e)}"
            }

    # 資料情報取得
    def get_material_by_barcode(self, barcode: str) -> Dict:
        """
        バーコードで資料情報を取得（リレーション情報も含む）
        """
        material = self.material_repo.find_by_barcode(barcode)
        
        if not material:
            return {
                "success": False,
                "message": "該当する資料が見つかりません。"
            }
        
        return {
            "success": True,
            "material": self._to_dict_with_relations(material)
        }

    # 資料一覧取得（フィルタ付き）
    def get_materials(
        self,
        affiliation: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict:

        if affiliation:
            materials = self.material_repo.find_by_affiliation(affiliation)
        else:
            materials = self.material_repo.find_all(skip, limit)
        
        total = self.material_repo.count()
        
        return {
            "success": True,
            "total": total,
            "materials": [self._to_dict(m) for m in materials]
        }
    
    # プライベートメソッド: データ変換
    def _to_dict(self, material: Material) -> Dict:
        """Materialオブジェクトを辞書に変換（基本情報のみ）"""
        return {
            "material_id": material.material_id,
            "barcode": material.barcode,
            "title": material.title,
            "author": material.author,
            "publisher": material.publisher,
            "ndc_code": material.ndc_code,
            "type_id": material.type_id,
            "affiliation": material.affiliation,
            "shelf": material.shelf,
            "loan_status": material.loan_status,
            "registration_date": material.registration_date.isoformat()
        }
    
    def _to_dict_with_relations(self, material: Material) -> Dict:
        """Materialオブジェクトを辞書に変換（リレーション情報も含む）"""
        base_dict = self._to_dict(material)
        base_dict.update({
            "ndc_name": material.ndc.ndc_name,
            "type_name": material.material_type.type_name,
            "loan_status_name": material.loan_status_info.status_name,
        })
        return base_dict

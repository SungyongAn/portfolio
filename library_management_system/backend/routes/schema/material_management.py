from pydantic import BaseModel, field_serializer
from typing import Optional, Union, Dict, Any
from datetime import date


# バーコード重複チェック
class CheckBarcodePayload(BaseModel):
    barcode: str


class CheckBarcodeResponseGeneric(BaseModel):
    success: bool
    message: Optional[str] = None


# 単独での資料登録
class MaterialRegisterPayload(BaseModel):
    barcode: str                        # バーコード番号
    title: str                          # 書籍タイトル
    author: str                         # 著者名
    publisher: Optional[str] = None     # 出版社
    ndc_code: str                       # NDC
    type_name: str                      # 種別
    affiliation: str                    # 学校名
    shelf: Optional[str] = None         # 棚版(任意)


class MaterialInfo(BaseModel):
    material_id: int
    barcode: str
    title: str
    author: str
    publisher: Optional[str] = None
    ndc_code: str
    type_name: str  # type_id ではなく type_name を使用
    affiliation: str
    shelf: Optional[str] = None
    registration_date: str  # date から str に変更
    
    class Config:
        from_attributes = True  # SQLAlchemy モデルからの変換を許可


class MaterialRegisterResponseGeneric(BaseModel):
    success: bool
    message: Optional[str] = None
    material: Optional[Union[MaterialInfo, Dict[str, Any]]] = None  # 辞書も許可
    
    class Config:
        arbitrary_types_allowed = True  # 任意の型を許可


# 資料検索
class MaterialSearchPayload(BaseModel):
    material_id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None


class MaterialSearchResponseGeneric(BaseModel):
    success: bool
    message: Optional[str] = None
    materials: list[Union[MaterialInfo, Dict[str, Any]]] = []  # 複数形
    
    class Config:
        arbitrary_types_allowed = True  # 任意の型を許可

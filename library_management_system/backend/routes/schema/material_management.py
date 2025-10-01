from pydantic import BaseModel
from typing import Optional
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
    shelf: Optional[str] = None         # 棚版（任意）


class MaterialInfo(BaseModel):
    material_id: int
    barcode: str
    title: str
    author: str
    publisher: Optional[str] = None
    ndc_code: str
    type_name: str
    affiliation: str
    shelf: Optional[str] = None
    registration_date: date


class MaterialRegisterResponseGeneric(BaseModel):
    success: bool
    message: Optional[str] = None
    material: Optional[MaterialInfo] = None

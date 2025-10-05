from pydantic import BaseModel
from typing import Optional


class AllPayload(BaseModel):
    # ユーザー関連
    user_id: Optional[str] = None
    username: Optional[str] = None
    admission_year: Optional[int] = None
    graduation_year: Optional[int] = None
    email: Optional[str] = None
    affiliation: Optional[str] = None
    password: Optional[str] = None
    
    # 資料関連
    material_id: Optional[int] = None
    barcode: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    ndc_code: Optional[str] = None
    type_name: Optional[str] = None
    shelf: Optional[str] = None
    registration_date: Optional[str] = None


class AllResponseGeneric(BaseModel):
    message: Optional[str] = None
    data: Optional[dict] = None

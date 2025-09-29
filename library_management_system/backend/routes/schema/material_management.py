from pydantic import BaseModel
from typing import Optional


# ログイン受信
class CheckBarcodePayload(BaseModel):
    barcode: str


class CheckBarcodeResponseGeneric(BaseModel):
    success: bool
    message: Optional[str] = None

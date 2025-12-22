from pydantic import BaseModel
from datetime import date, datetime


# 連絡帳作成リクエスト
class JournalCreate(BaseModel):
    entry_date: date
    physical_condition: str
    mental_condition: str
    reflection_text: str


# 連絡帳レスポンス
class JournalResponse(BaseModel):
    id: int
    student_id: int
    entry_date: date
    submission_date: date
    physical_condition: str
    mental_condition: str
    reflection_text: str
    is_read: bool
    read_at: datetime | None = None
    created_at: datetime
    
    class Config:
        from_attributes = True

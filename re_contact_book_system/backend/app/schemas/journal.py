from pydantic import BaseModel, Field
from datetime import date, datetime


# 連絡帳作成リクエスト
class JournalCreate(BaseModel):
    entry_date: date
    physical_condition: str
    mental_condition: str
    reflection_text: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "entry_date": "2025-04-08",
                "physical_condition": "よかった",
                "mental_condition": "元気",
                "reflection_text": "数学の授業で二次関数を学んだ。完全に理解した。"
            }
        }


# 連絡帳更新リクエスト（将来の拡張用）
class JournalUpdate(BaseModel):
    physical_condition: str | None = None
    mental_condition: str | None = None
    reflection_text: str | None = None


# 連絡帳レスポンス
class JournalResponse(BaseModel):
    id: int
    student_id: int
    student_name: str | None = None
    entry_date: date
    submission_date: date
    physical_condition: str
    mental_condition: str
    reflection_text: str | None = None
    is_read: bool
    read_by: int | None = None
    read_at: datetime | None = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# 連絡帳一覧レスポンス
class JournalListResponse(BaseModel):
    total: int
    journals: list[JournalResponse]


# 提出状況レスポンス
class SubmissionStatusResponse(BaseModel):
    student_id: int
    student_name: str
    has_submitted: bool
    is_read: bool
    journal_id: int | None = None
    submission_date: date | None = None

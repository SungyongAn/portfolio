from pydantic import BaseModel


# 養護教諭用）連絡帳詳細取得
class EntryDetailRecord(BaseModel):
    renrakucho_id: int
    student_id: int
    student_name: str
    grade: int
    class_name: str
    submitted_date: str
    target_date: str
    physical_condition: int
    mental_state: int
    physical_mental_notes: str | None = None
    daily_reflection: str
    is_read: bool
    created_at: str | None = None


class EntryDetailResponse(BaseModel):
    success: bool
    message: str
    data: EntryDetailRecord | None = None

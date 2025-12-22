from sqlalchemy.orm import Session
from app.models.journal import JournalEntry
from app.schemas.journal import JournalCreate
from datetime import date, datetime, timedelta


def calculate_entry_date() -> date:
    """前登校日を計算（土日をスキップ）"""
    today = date.today()
    weekday = today.weekday()  # 0=月曜, 6=日曜
    
    if weekday == 0:  # 月曜日
        return today - timedelta(days=3)  # 金曜日
    elif weekday == 6:  # 日曜日
        return today - timedelta(days=2)  # 金曜日
    else:
        return today - timedelta(days=1)  # 前日


def create_journal(db: Session, student_id: int, journal_data: JournalCreate):
    """連絡帳を作成"""
    entry = JournalEntry(
        student_id=student_id,
        entry_date=journal_data.entry_date,
        submission_date=date.today(),
        physical_condition=journal_data.physical_condition,
        mental_condition=journal_data.mental_condition,
        reflection_text=journal_data.reflection_text
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def mark_as_read(db: Session, journal_id: int, teacher_id: int):
    """既読処理"""
    entry = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if entry:
        entry.is_read = True
        entry.read_by = teacher_id
        entry.read_at = datetime.utcnow()
        db.commit()
        db.refresh(entry)
    return entry

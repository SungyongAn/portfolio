from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.schemas.journal import JournalCreate, JournalResponse
from app.services.journal_service import create_journal, calculate_entry_date
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/journals", tags=["連絡帳"])

@router.post("/", response_model=JournalResponse)
def submit_journal(
    journal_data: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """連絡帳を提出"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="生徒のみ提出可能です")
    
    entry = create_journal(db, current_user.id, journal_data)
    return entry

@router.get("/history", response_model=List[JournalResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """過去の連絡帳を取得"""
    from app.models.journal import JournalEntry
    entries = db.query(JournalEntry).filter(
        JournalEntry.student_id == current_user.id
    ).order_by(JournalEntry.entry_date.desc()).all()
    return entries

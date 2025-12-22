from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entry_date = Column(Date, nullable=False)  # 記入対象日
    submission_date = Column(Date, nullable=False)  # 提出日
    physical_condition = Column(String(50))  # 体調
    mental_condition = Column(String(50))  # メンタル
    reflection_text = Column(Text)  # 振り返り
    is_read = Column(Boolean, default=False)  # 既読フラグ
    read_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 既読した教師
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    student = relationship("User", foreign_keys=[student_id])
    teacher = relationship("User", foreign_keys=[read_by])

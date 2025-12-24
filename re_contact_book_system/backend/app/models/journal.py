from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class JournalEntry(Base):
    """
    連絡帳エントリテーブル
    """
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment='生徒ID')
    entry_date = Column(Date, nullable=False, index=True, comment='記入対象日（前登校日）')
    submission_date = Column(Date, nullable=False, index=True, comment='提出日')
    physical_condition = Column(String(50), nullable=False, comment='体調')
    mental_condition = Column(String(50), nullable=False, comment='メンタル')
    reflection_text = Column(Text, comment='振り返り内容')
    is_read = Column(Boolean, default=False, index=True, comment='既読フラグ')
    read_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True, comment='既読した教師ID')
    read_at = Column(DateTime(timezone=True), nullable=True, comment='既読日時')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーション
    student = relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="journal_entries"
    )
    
    reader = relationship(
        "User",
        foreign_keys=[read_by],
        back_populates="read_journals"
    )
    
    # 関連する教師メモ
    teacher_notes = relationship(
        "TeacherNote",
        back_populates="journal_entry",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return (
            f"<JournalEntry(id={self.id}",
            f"student_id={self.student_id}",
            f"entry_date={self.entry_date}",
            f"is_read={self.is_read})>"
            )

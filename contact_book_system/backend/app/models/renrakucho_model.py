from sqlalchemy import Column, Integer, Date, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base import Base


class RenrakuchoEntryModel(Base):
    __tablename__ = "renrakucho_entries"

    renrakucho_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    submitted_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=False)
    physical_condition = Column(TINYINT, nullable=False)
    mental_state = Column(TINYINT, nullable=False)
    physical_mental_notes = Column(Text, nullable=True) 
    daily_reflection = Column(Text, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)

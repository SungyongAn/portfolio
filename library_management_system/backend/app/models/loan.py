"""
図書館システム SQLAlchemy モデル定義
ER設計に基づく全テーブル
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.base import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    loaned_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        comment="代理貸出操作者 (司書/図書委員)",
    )
    loaned_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(Date, nullable=False, comment="返却期限")
    returned_at = Column(DateTime, nullable=True)
    returned_by = Column(
        Integer, ForeignKey("users.id"), nullable=True, comment="代理返却操作者"
    )
    # 将来の延長機能用カラム (UC-28 / 課題2で確定予定)
    extended_count = Column(Integer, nullable=False, default=0, comment="延長回数")

    user = relationship("User", foreign_keys=[user_id], back_populates="loans")
    book = relationship("Book", back_populates="loans")

    __table_args__ = (
        Index("ix_loans_user_id", "user_id"),
        Index("ix_loans_book_id", "book_id"),
        Index("ix_loans_due_date", "due_date"),
        Index("ix_loans_returned_at", "returned_at"),
    )

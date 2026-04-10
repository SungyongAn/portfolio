from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class Reservation(Base):
    """
    自校資料の予約。
    status:
      waiting  → 貸出中につき順番待ち
      ready    → 返却済み・取置き中（貸出可能）
      canceled → キャンセル（waiting / ready のみ可）
      expired  → システム自動失効
      fulfilled→ 貸出完了
    """

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reserved_by = Column(
        Integer, ForeignKey("users.id"), nullable=True, comment="代理予約操作者"
    )
    status = Column(
        Enum(
            "waiting",
            "ready",
            "canceled",
            "expired",
            "fulfilled",
            name="reservation_status",
        ),
        nullable=False,
        default="waiting",
    )
    notified_at = Column(DateTime, nullable=True, comment="準備完了通知日時")
    ready_deadline = Column(DateTime, nullable=True, comment="取置き期限")
    canceled_at = Column(DateTime, nullable=True)
    fulfilled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = relationship("User", foreign_keys=[user_id], back_populates="reservations")
    book = relationship("Book", back_populates="reservations")
    reserved_by_user = relationship(
        "User",
        foreign_keys=[reserved_by],
    )

    __table_args__ = (
        Index("ix_reservations_user_id", "user_id"),
        Index("ix_reservations_book_id", "book_id"),
        Index("ix_reservations_status", "status"),
    )

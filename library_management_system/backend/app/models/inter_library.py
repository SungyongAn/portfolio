import sqlalchemy as sa
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base


class InterLibraryRequest(Base):
    """
    他校資料への図書館間貸出リクエスト。
    status 遷移:
      pending   → 締め切り前（金曜15時）
      confirmed → 締め切り後・発送待ち
      shipped   → 発送済み（キャンセル不可）
      arrived   → 着荷・取置き中
      fulfilled → 貸出完了
      canceled  → キャンセル（pending / confirmed のみ可）
    """

    __tablename__ = "inter_library_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="申請者")
    book_id = Column(
        Integer, ForeignKey("books.id"), nullable=False, comment="対象資料（他校蔵書）"
    )
    requested_by = Column(
        Integer, ForeignKey("users.id"), nullable=True, comment="代理申請者"
    )
    from_school_id = Column(
        Integer, ForeignKey("schools.id"), nullable=False, comment="貸出元学校"
    )
    to_school_id = Column(
        Integer, ForeignKey("schools.id"), nullable=False, comment="届け先学校"
    )
    status = Column(
        Enum(
            "pending",
            "confirmed",
            "shipped",
            "arrived",
            "fulfilled",
            "canceled",
            name="inter_library_status",
        ),
        nullable=False,
        default="pending",
    )
    deadline = Column(DateTime, nullable=True, comment="締め切り日時（金曜15時）")
    shipped_at = Column(DateTime, nullable=True, comment="発送登録日時")
    arrived_at = Column(DateTime, nullable=True, comment="着荷登録日時")
    notified_at = Column(DateTime, nullable=True, comment="着荷通知日時")
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"))
    updated_at = Column(sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship(
        "User", foreign_keys=[user_id], back_populates="inter_library_requests"
    )
    book = relationship("Book", back_populates="inter_library_requests")
    from_school = relationship(
        "School",
        foreign_keys=[from_school_id],
    )

    to_school = relationship(
        "School",
        foreign_keys=[to_school_id],
    )

    __table_args__ = (
        Index("ix_inter_library_requests_user_id", "user_id"),
        Index("ix_inter_library_requests_book_id", "book_id"),
        Index("ix_inter_library_requests_status", "status"),
        Index("ix_inter_library_requests_from_school", "from_school_id"),
        Index("ix_inter_library_requests_to_school", "to_school_id"),
    )
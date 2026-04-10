from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base


class Book(Base):
    """
    物理的な1冊を表すテーブル。
    同一タイトルでも複数冊あればレコードが複数存在する。
    barcode は新採番ルールで全校統一。
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(
        Integer, ForeignKey("schools.id"), nullable=False, comment="所蔵学校"
    )
    barcode = Column(
        String(50), nullable=False, unique=True, comment="資料バーコード (統一採番)"
    )
    isbn = Column(String(20), nullable=True, comment="ISBN-13")
    title = Column(String(500), nullable=False)
    author = Column(String(255), nullable=True)
    publisher = Column(String(255), nullable=True)
    published_year = Column(Integer, nullable=True)
    ndc = Column(String(10), nullable=True, comment="日本十進分類法コード")
    description = Column(Text, nullable=True)
    status = Column(
        Enum(
            "available",  # 貸出可能
            "reserved",  # 予約済み（自校）
            "on_loan",  # 貸出中
            "inter_library",  # 図書館間貸出中
            "discarded",  # 廃棄
            name="book_status",
        ),
        nullable=False,
        default="available",
    )
    discarded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    school = relationship("School", back_populates="books")
    loans = relationship("Loan", back_populates="book")
    reservations = relationship("Reservation", back_populates="book")
    inter_library_requests = relationship("InterLibraryRequest", back_populates="book")


    __table_args__ = (
        Index("ix_books_school_id", "school_id"),
        Index("ix_books_isbn", "isbn"),
        Index("ix_books_status", "status"),
        Index("ix_books_ndc", "ndc"),
    )

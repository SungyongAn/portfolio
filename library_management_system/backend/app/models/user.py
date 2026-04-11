import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    email = Column(
        String(255), nullable=False, unique=True, comment="学校メールアドレス"
    )
    password_hash = Column(String(255), nullable=False, comment="Argon2ハッシュ")
    name = Column(String(100), nullable=False, comment="氏名")
    barcode = Column(
        String(50), nullable=True, unique=True, comment="図書館カードバーコード"
    )
    grade = Column(Integer, nullable=True, comment="学年 (1〜3)")
    class_name = Column(String(20), nullable=True, comment="クラス名")
    role = Column(
        Enum("student", "librarian", "admin", name="user_role"),
        nullable=False,
        default="student",
    )
    is_committee = Column(
        Boolean, nullable=False, default=False, comment="図書委員フラグ"
    )
    is_active = Column(
        Boolean, nullable=False, default=True, comment="退学・卒業フラグ"
    )
    created_at = Column(
        sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        sa.TIMESTAMP,
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    school = relationship("School", back_populates="users")
    loans = relationship("Loan", foreign_keys="Loan.user_id", back_populates="user")
    reservations = relationship(
        "Reservation", foreign_keys="Reservation.user_id", back_populates="user"
    )
    inter_library_requests = relationship(
        "InterLibraryRequest",
        foreign_keys="InterLibraryRequest.user_id",
        back_populates="user",
    )
    password_reset_tokens = relationship(
        "PasswordResetToken", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_users_school_id", "school_id"),
        Index("ix_users_role", "role"),
    )

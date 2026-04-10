from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from app.models.base import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(
        String(64), nullable=False, unique=True, comment="SHA-256ハッシュ済みトークン"
    )
    expires_at = Column(DateTime, nullable=False, comment="有効期限 (発行から30分)")
    used_at = Column(DateTime, nullable=True, comment="使用日時（1回使い捨て）")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="password_reset_tokens")

    __table_args__ = (Index("ix_password_reset_tokens_user_id", "user_id"),)

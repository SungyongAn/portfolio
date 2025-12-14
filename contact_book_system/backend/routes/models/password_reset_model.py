from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from routes.db.base import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="トークンID")
    account_id = Column(
        Integer,
        ForeignKey('accounts.id'),
        nullable=False,
        comment="アカウントID"
    )
    token = Column(String(255), unique=True, nullable=False, comment="リセットトークン")
    used = Column(Boolean, default=False, nullable=False, comment="使用済みフラグ")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
    expires_at = Column(TIMESTAMP, nullable=False, comment="有効期限")

    def __repr__(self):
        return f"<PasswordResetToken(id={self.id}, account_id={self.account_id}, used={self.used})>"

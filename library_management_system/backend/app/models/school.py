"""
図書館システム SQLAlchemy モデル定義
ER設計に基づく全テーブル
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="学校名")
    code = Column(String(10), nullable=False, unique=True, comment="学校コード (A〜E)")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    users = relationship("User", back_populates="school")
    books = relationship("Book", back_populates="school")


import sqlalchemy as sa
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
    created_at = Column(sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"))
    updated_at = Column(sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
 
    users = relationship("User", back_populates="school")
    books = relationship("Book", back_populates="school")
 
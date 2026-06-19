from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import Base


class ExpenseType(str, enum.Enum):
    OUTSOURCING = "OUTSOURCING"  # 外注費
    LICENSE = "LICENSE"  # ライセンス費
    EQUIPMENT = "EQUIPMENT"  # 機器・備品
    OTHER = "OTHER"  # その他


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    expense_type = Column(Enum(ExpenseType), nullable=False)
    amount = Column(Integer, nullable=False)  # 金額（円）
    description = Column(Text, nullable=True)  # 内容説明
    expense_date = Column(Date, nullable=False)  # 経費発生日
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # relationships
    project = relationship("Project", back_populates="expenses")

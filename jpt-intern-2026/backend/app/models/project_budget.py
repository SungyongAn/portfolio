from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class ProjectBudget(Base):
    __tablename__ = "project_budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, unique=True)
    budget_amount = Column(Integer, nullable=False)  # 予算額（円）
    unit_price = Column(Integer, nullable=True)  # 人月単価（円）
    planned_months = Column(Integer, nullable=True)  # 計画工数（人月）
    actual_amount = Column(Integer, nullable=False, default=0)  # 実績額（円）
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # relationships
    project = relationship("Project", back_populates="budget")

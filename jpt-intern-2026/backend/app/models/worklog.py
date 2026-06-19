from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Numeric,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from decimal import Decimal


class Worklog(Base):
    __tablename__ = "worklogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    work_month = Column(String(7), nullable=False)  # 例: "2026-04"
    actual_months = Column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0.00"),
        comment="実績工数（人月）",
    )  # 実績工数（人月 * 100、小数対応）
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "work_month", name="uq_worklog_project_month"),
    )

    # relationships
    project = relationship("Project", back_populates="worklogs")

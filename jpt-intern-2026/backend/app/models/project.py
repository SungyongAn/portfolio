from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import Base


class ProjectStatus(str, enum.Enum):
    DRAFT = "DRAFT"  # 作成途中の申請書を一時保管用のステータス
    PENDING_DEPT = "PENDING_DEPT"  # 部門管理者承認待ち
    PENDING_HQ = "PENDING_HQ"  # 本部管理者承認待ち

    APPROVED = "APPROVED"  # 承認済み（開始前）
    IN_PROGRESS = "IN_PROGRESS"  # 進行中（着手中）
    COMPLETED = "COMPLETED"  # 完了

    REJECTED = "REJECTED"  # 却下


class DevelopmentMethod(str, enum.Enum):
    WATERFALL = "WATERFALL"  # ウォーターフォール型
    AGILE = "AGILE"  # アジャイル型


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.DRAFT)

    development_method = Column(
        Enum(DevelopmentMethod),
        nullable=True,
        default=None,
    )

    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    budget_amount = Column(Integer, nullable=True)
    planned_months = Column(Integer, nullable=True)

    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    reject_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # relationships
    applicant = relationship("User", back_populates="projects")
    department = relationship("Department", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    budget = relationship("ProjectBudget", back_populates="project", uselist=False)
    worklogs = relationship("Worklog", back_populates="project")
    expenses = relationship("Expense", back_populates="project")
    notifications = relationship("Notification", back_populates="project")

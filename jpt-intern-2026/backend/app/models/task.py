from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import Base


class TaskStatus(str, enum.Enum):
    TODO = "TODO"  # 未着手
    IN_PROGRESS = "IN_PROGRESS"  # 進行中
    IN_REVIEW = "IN_REVIEW"  # レビュー中
    DONE = "DONE"  # 完了


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    name = Column(String(200), nullable=False)
    phase_name = Column(String(100), nullable=True)

    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    progress = Column(Integer, nullable=False, default=0)

    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assignee_id])

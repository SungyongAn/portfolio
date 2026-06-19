from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import Base


class UserRole(str, enum.Enum):
    TASK_MEMBER = "TASK_MEMBER"  # メンバー
    APPLICANT = "APPLICANT"  # 申請者(チームリーダー)
    DEPT_MANAGER = "DEPT_MANAGER"  # 部門管理者
    HQ_MANAGER = "HQ_MANAGER"  # 本部管理者


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # relationships
    department = relationship("Department", back_populates="users")
    projects = relationship("Project", back_populates="applicant")
    notifications = relationship("Notification", back_populates="user")

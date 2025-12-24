from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base
import enum


class RoleEnum(str, enum.Enum):
    """ユーザーロール"""
    student = "student"
    teacher = "teacher"
    admin = "admin"


class User(Base):
    """
    ユーザーテーブル
    生徒、教師、管理者すべてを管理
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False, comment='ログイン用メールアドレス')
    password_hash = Column(String(255), nullable=False, comment='ハッシュ化されたパスワード')
    name = Column(String(100), nullable=False, comment='氏名')
    role = Column(Enum(RoleEnum), nullable=False, comment='ユーザーロール')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーション
    # 生徒としてのクラス割当
    student_class_assignments = relationship(
        "StudentClassAssignment",
        foreign_keys="StudentClassAssignment.student_id",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    
    # 教師としての割当
    teacher_assignments = relationship(
        "TeacherAssignment",
        foreign_keys="TeacherAssignment.teacher_id",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )
    
    # 投稿した連絡帳
    journal_entries = relationship(
        "JournalEntry",
        foreign_keys="JournalEntry.student_id",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    
    # 既読した連絡帳
    read_journals = relationship(
        "JournalEntry",
        foreign_keys="JournalEntry.read_by",
        back_populates="reader"
    )
    
    # 作成した教師メモ
    teacher_notes = relationship(
        "TeacherNote",
        foreign_keys="TeacherNote.teacher_id",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}', role='{self.role}')>"

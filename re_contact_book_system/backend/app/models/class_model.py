from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base
import enum


class Grade(Base):
    """学年テーブル"""
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    grade_number = Column(Integer, nullable=False, comment='学年番号（1,2,3）')
    year = Column(Integer, nullable=False, index=True, comment='年度（2025,2026...）')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    classes = relationship("Class", back_populates="grade", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Grade(id={self.id}, grade={self.grade_number}, year={self.year})>"


class Class(Base):
    """クラステーブル"""
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    grade_id = Column(Integer, ForeignKey("grades.id", ondelete="CASCADE"), nullable=False, index=True, comment='学年ID')
    class_name = Column(String(50), nullable=False, comment='クラス名（A組,B組）')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    grade = relationship("Grade", back_populates="classes")
    student_assignments = relationship("StudentClassAssignment", back_populates="class_obj", cascade="all, delete-orphan")
    teacher_assignments = relationship("TeacherAssignment", back_populates="class_obj", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.class_name}')>"


class StudentClassAssignment(Base):
    """生徒クラス割当テーブル"""
    __tablename__ = "student_class_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment='生徒ID')
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True, comment='クラスID')
    is_current = Column(Boolean, default=True, index=True, comment='現在のクラスか')
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), comment='割当日時')
    
    # リレーション
    student = relationship("User", foreign_keys=[student_id], back_populates="student_class_assignments")
    class_obj = relationship("Class", back_populates="student_assignments")
    
    def __repr__(self):
        return f"<StudentClassAssignment(student_id={self.student_id}, class_id={self.class_id}, is_current={self.is_current})>"


class AssignmentTypeEnum(str, enum.Enum):
    """教師割当種別"""
    homeroom = "homeroom"            # 担任
    subject = "subject"              # 教科担当
    grade_head = "grade_head"        # 学年主任
    administrator = "administrator"  # 管理職


class PermissionLevelEnum(str, enum.Enum):
    """権限レベル"""
    read = "read"    # 閲覧のみ
    write = "write"  # 編集可能
    admin = "admin"  # 管理者権限


class TeacherAssignment(Base):
    """教師割当テーブル"""
    __tablename__ = "teacher_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment='教師ID')
    assignment_type = Column(Enum(AssignmentTypeEnum), nullable=False, index=True, comment='割当種別')
    grade_id = Column(Integer, ForeignKey("grades.id", ondelete="CASCADE"), nullable=True, index=True, comment='学年ID')
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=True, index=True, comment='クラスID')
    subject_name = Column(String(50), nullable=True, comment='教科名')
    is_primary = Column(Boolean, default=False, comment='主担任フラグ')
    permission_level = Column(Enum(PermissionLevelEnum), default=PermissionLevelEnum.read, comment='権限レベル')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="teacher_assignments")
    grade = relationship("Grade")
    class_obj = relationship("Class", back_populates="teacher_assignments")
    
    def __repr__(self):
        return f"<TeacherAssignment(teacher_id={self.teacher_id}, type={self.assignment_type})>"


class TeacherNote(Base):
    """教師メモテーブル（課題2用）"""
    __tablename__ = "teacher_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment='作成教師ID')
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment='対象生徒ID')
    entry_id = Column(Integer, ForeignKey("journal_entries.id", ondelete="SET NULL"), nullable=True, index=True, comment='関連連絡帳ID')
    note_text = Column(Text, nullable=False, comment='メモ内容')
    is_shared = Column(Boolean, default=False, index=True, comment='学年共有フラグ')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーション
    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="teacher_notes")
    student = relationship("User", foreign_keys=[student_id])
    journal_entry = relationship("JournalEntry", back_populates="teacher_notes")
    
    def __repr__(self):
        return f"<TeacherNote(id={self.id}, teacher_id={self.teacher_id}, student_id={self.student_id})>"

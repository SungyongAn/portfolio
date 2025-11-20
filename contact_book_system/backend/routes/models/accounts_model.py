from sqlalchemy import Column, Integer, String, Enum as SQLEnum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from routes.db.base import Base
import enum


# 権限（基本役割）
class RoleEnum(str, enum.Enum):
    admin = "admin"              # 管理者
    teacher = "teacher"          # 教師
    student = "student"          # 生徒
    school_nurse = "school_nurse"  # 養護教諭


# 在籍状況（生徒・職員共通）
class StatusEnum(str, enum.Enum):
    enrolled = "enrolled"          # 在籍中
    graduated = "graduated"        # 卒業・修了
    transferred = "transferred"    # 転入・転出
    on_leave = "on_leave"          # 休学・休職
    other = "other"                # その他


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="アカウントID")
    
    # 基本属性（生徒・教師共通）
    name = Column(String(100), nullable=False, comment="氏名")
    password = Column(String(255), nullable=False, comment="パスワード（ハッシュ化）")
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.student, comment="アカウント種別")
    status = Column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.enrolled, comment="在籍状況")

    # 生徒向けフィールド
    grade = Column(Integer, nullable=False, comment="学年")
    class_name = Column(String(10), nullable=False, comment="クラス")
    enrollment_year = Column(Integer, nullable=False, comment="入学年または採用年")
    graduation_year = Column(Integer, nullable=True, comment="卒業予定年（教師はNULL）")

    # 教師専用フィールド（外部キー）
    teacher_role_id = Column(
        Integer,
        ForeignKey('teacher_roles.id'),
        nullable=True,
        comment="教員区分ID（教師の場合のみ）"
    )
    subject_id = Column(
        Integer,
        ForeignKey('subjects.id'),
        nullable=True,
        comment="担当教科ID（教師の場合のみ）"
    )

    # メタ情報
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時"
    )

    # リレーションシップ（必要に応じて使用）
    teacher_role = relationship("TeacherRole", foreign_keys=[teacher_role_id])
    subject = relationship("Subject", foreign_keys=[subject_id])

    def __repr__(self):
        return (
            f"<Account(id={self.id}, name='{self.name}', role='{self.role.value}', "
            f"grade={self.grade}, class='{self.class_name}')>"
        )


# teacher_roles テーブル
class TeacherRole(Base):
    __tablename__ = "teacher_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, comment="役職コード")
    name = Column(String(50), nullable=False, comment="役職名")
    description = Column(String(255), nullable=True, comment="説明")

    def __repr__(self):
        return f"<TeacherRole(id={self.id}, code='{self.code}', name='{self.name}')>"


# subjects テーブル
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, comment="教科コード")
    name = Column(String(50), nullable=False, comment="教科名")

    def __repr__(self):
        return f"<Subject(id={self.id}, code='{self.code}', name='{self.name}')>"

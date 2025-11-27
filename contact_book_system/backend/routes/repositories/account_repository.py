from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from routes.models.accounts_model import Account, TeacherRole, Subject, RoleEnum, StatusEnum


# アカウント関連のデータアクセスを担当するリポジトリクラス
class AccountRepository:

    # IDでアカウントを検索
    @staticmethod
    def find_by_id(db: Session, account_id: int) -> Optional[Account]:
        return db.query(Account).filter(Account.id == account_id).first()

    # 名前でアカウント検索
    @staticmethod
    def find_by_name(db: Session, name: str) -> Optional[Account]:
        return db.query(Account).filter(Account.name == name).first()

    # 名前・学年・クラスでアカウントを検索（重複チェックに使用）
    @staticmethod
    def find_by_name_grade_class(
        db: Session, 
        name: str, 
        grade: int, 
        class_name: str
    ) -> Optional[Account]:
        
        return db.query(Account).filter(
            Account.name == name,
            Account.grade == grade,
            Account.class_name == class_name
        ).first()

    # 新しいアカウントを作成
    @staticmethod
    def create(db: Session, account: Account) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    # アカウント情報を更新
    @staticmethod
    def update(db: Session, account: Account) -> Account:
        db.commit()
        db.refresh(account)
        return account

    # 複数の条件でアカウントを検索
    @staticmethod
    def search_with_filters(
        db: Session,
        role: Optional[str] = None,
        full_name: Optional[str] = None,
        grade: Optional[int] = None,
        class_name: Optional[str] = None,
        enrollment_year: Optional[int] = None,
        status: Optional[str] = None,
        teacher_role_id: Optional[int] = None,
        subject_id: Optional[int] = None
    ) -> List[Account]:
        
        query = db.query(Account)

        if role:
            try:
                role_enum = RoleEnum(role.lower())
                query = query.filter(Account.role == role_enum)
            except ValueError:
                return []

        if full_name:
            query = query.filter(Account.name == full_name)

        if grade:
            query = query.filter(Account.grade == grade)

        if class_name:
            query = query.filter(Account.class_name == class_name)

        if enrollment_year:
            query = query.filter(Account.enrollment_year == enrollment_year)

        if status:
            try:
                status_enum = StatusEnum(status.lower())
                query = query.filter(Account.status == status_enum)
            except ValueError:
                pass

        if teacher_role_id:
            query = query.filter(Account.teacher_role_id == teacher_role_id)

        if subject_id:
            query = query.filter(Account.subject_id == subject_id)

        return query.all()

    """ 以下未使用 """
    # 指定された学年・クラスの生徒を取得
    @staticmethod
    def find_students_by_grade_class(
        db: Session, 
        grade: int, 
        class_name: str
    ) -> List[Account]:
        
        return db.query(Account).filter(
            Account.grade == grade,
            Account.class_name == class_name,
            Account.role == RoleEnum.student
        ).order_by(Account.name).all()
    """ ここまで未使用 """


# 教員区分関連のデータアクセスを担当するリポジトリクラス
class TeacherRoleRepository:

    # IDで教員区分を検索
    @staticmethod
    def find_by_id(db: Session, teacher_role_id: int) -> Optional[TeacherRole]:
        return db.query(TeacherRole).filter(TeacherRole.id == teacher_role_id).first()

    # コードで教員区分を検索
    @staticmethod
    def find_by_code(db: Session, code: str) -> Optional[TeacherRole]:
        return db.query(TeacherRole).filter(TeacherRole.code == code).first()

    """ 以下未使用 """
    # すべての教員区分を取得
    @staticmethod
    def find_all(db: Session) -> List[TeacherRole]:
        return db.query(TeacherRole).all()
    """ ここまで未使用 """


# 科目関連のデータアクセスを担当するリポジトリクラス
class SubjectRepository:

    # IDで科目を検索
    @staticmethod
    def find_by_id(db: Session, subject_id: int) -> Optional[Subject]:
        return db.query(Subject).filter(Subject.id == subject_id).first()

    # コードで科目を検索
    @staticmethod
    def find_by_code(db: Session, code: str) -> Optional[Subject]:
        return db.query(Subject).filter(Subject.code == code).first()

    """ 以下未使用 """
    # すべての科目を取得
    @staticmethod
    def find_all(db: Session) -> List[Subject]:
        return db.query(Subject).all()
    """ ここまで未使用 """

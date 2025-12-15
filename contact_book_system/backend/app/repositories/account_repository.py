from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from app.models.accounts_model import Account, TeacherRole, Subject, RoleEnum, StatusEnum


# アカウント関連のデータアクセスを担当するリポジトリクラス
class AccountRepository:

    # IDでアカウントを検索
    @staticmethod
    def find_by_id(db: Session, account_id: int) -> Optional[Account]:
        return db.query(Account).filter(Account.id == account_id).first()

    # 姓でアカウント検索
    @staticmethod
    def find_by_last_name(db: Session, last_name: str) -> Optional[Account]:
        return db.query(Account).filter(Account.last_name == last_name).first()

    # 名でアカウント検索
    @staticmethod
    def find_by_first_name(db: Session, first_name: str) -> Optional[Account]:
        return db.query(Account).filter(Account.first_name == first_name).first()

    # 姓名の両方でアカウント検索
    @staticmethod
    def find_by_full_name(db: Session, last_name: str, first_name: str) -> Optional[Account]:
        return db.query(Account).filter(
            Account.last_name == last_name,
            Account.first_name == first_name
        ).first()

    # emailでアカウント検索(重複チェックに使用)
    @staticmethod
    def find_by_email(db: Session, email: str) -> Optional[Account]:
        return db.query(Account).filter(Account.email == email).first()

    # 名前・学年・クラスでアカウントを検索（重複チェックに使用）
    @staticmethod
    def find_by_name_grade_class(
        db: Session,
        email: str,
        last_name: str, 
        first_name: str,
        grade: int, 
        class_name: str
    ) -> Optional[Account]:
        
        return db.query(Account).filter(
            Account.email == email,
            Account.last_name == last_name,
            Account.first_name == first_name,
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
        email: Optional[str] = None,
        role: Optional[str] = None,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        grade: Optional[int] = None,
        class_name: Optional[str] = None,
        enrollment_year: Optional[int] = None,
        status: Optional[str] = None,
        teacher_role_id: Optional[int] = None,
        subject_id: Optional[int] = None
    ) -> List[Account]:
        
        query = db.query(Account)

        if email:
            query = query.filter(Account.email == email)

        if role:
            try:
                role_enum = RoleEnum(role.lower())
                query = query.filter(Account.role == role_enum)
            except ValueError:
                return []

        if last_name:
            query = query.filter(Account.last_name == last_name)
            
        if first_name:
            query = query.filter(Account.first_name == first_name)

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
        ).order_by(Account.last_name, Account.first_name)
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

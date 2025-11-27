from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Optional, List, Tuple
from datetime import date
from routes.models.renrakucho_model import RenrakuchoEntryModel
from routes.models.accounts_model import Account


# 連絡帳関連のデータアクセスを担当するリポジトリクラス
class RenrakuchoRepository:

    # IDで連絡帳を検索
    @staticmethod
    def find_by_id(db: Session, renrakucho_id: int) -> Optional[RenrakuchoEntryModel]:
        
        return db.query(RenrakuchoEntryModel).filter(
            RenrakuchoEntryModel.renrakucho_id == renrakucho_id
        ).first()

    # 生徒IDと対象日で連絡帳を検索（重複チェックに使用）
    @staticmethod
    def find_by_student_and_date(
        db: Session, 
        student_id: int, 
        target_date: date
    ) -> Optional[RenrakuchoEntryModel]:
        
        return db.query(RenrakuchoEntryModel).filter(
            RenrakuchoEntryModel.student_id == student_id,
            RenrakuchoEntryModel.target_date == target_date
        ).first()

    # 新しい連絡帳を作成
    @staticmethod
    def create(db: Session, entry: RenrakuchoEntryModel) -> RenrakuchoEntryModel:

        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    # 担任・副担任）連絡帳の既読処理(複数の同時処理可能)
    @staticmethod
    def mark_as_read(db: Session, renrakucho_ids: List[int]) -> int:
        
        count = db.query(RenrakuchoEntryModel).filter(
            RenrakuchoEntryModel.renrakucho_id.in_(renrakucho_ids)
        ).update(
            {RenrakuchoEntryModel.is_read: True},
            synchronize_session=False
        )
        db.commit()
        return count

    # 生徒の連絡帳閲覧）生徒IDで連絡帳を検索（日付フィルタ対応）
    @staticmethod
    def find_by_student(
        db: Session,
        student_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        weekday: Optional[int] = None
    ) -> List[RenrakuchoEntryModel]:
        
        query = db.query(RenrakuchoEntryModel).filter(
            RenrakuchoEntryModel.student_id == student_id
        )

        if year:
            query = query.filter(func.year(RenrakuchoEntryModel.target_date) == year)
        
        if month:
            query = query.filter(func.month(RenrakuchoEntryModel.target_date) == month)
        
        if day:
            query = query.filter(func.day(RenrakuchoEntryModel.target_date) == day)
        
        if weekday is not None:
            # MySQLのdayofweek: 1=日曜, 2=月曜, ..., 7=土曜
            # Pythonのweekday: 0=月曜, 1=火曜, ..., 6=日曜
            mysql_weekday = ((weekday + 1) % 7) + 1
            query = query.filter(func.dayofweek(RenrakuchoEntryModel.target_date) == mysql_weekday)

        return query.order_by(RenrakuchoEntryModel.target_date.desc()).all()

    # 教師用）担当クラス生徒の過去の連絡帳を検索
    @staticmethod
    def find_by_class_with_student_info(
        db: Session,
        grade: int,
        class_name: str,
        student_name: Optional[str] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        weekday: Optional[int] = None,
        is_read: Optional[bool] = None
    ) -> List[Tuple[RenrakuchoEntryModel, str]]:

        query = db.query(
            RenrakuchoEntryModel, 
            Account.name.label("student_name")
        ).join(
            Account, 
            Account.id == RenrakuchoEntryModel.student_id
        ).filter(
            Account.grade == grade,
            Account.class_name == class_name
        )

        if student_name:
            query = query.filter(Account.name.like(f"%{student_name}%"))

        if year:
            query = query.filter(func.year(RenrakuchoEntryModel.target_date) == year)
        
        if month:
            query = query.filter(func.month(RenrakuchoEntryModel.target_date) == month)
        
        if day:
            query = query.filter(func.day(RenrakuchoEntryModel.target_date) == day)
        
        if weekday is not None:
            mysql_weekday = ((weekday + 1) % 7) + 1
            query = query.filter(func.dayofweek(RenrakuchoEntryModel.target_date) == mysql_weekday)
        
        if is_read is not None:
            query = query.filter(RenrakuchoEntryModel.is_read == is_read)

        return query.order_by(RenrakuchoEntryModel.target_date.desc()).all()

    # 教師用）未読連絡帳の取得
    @staticmethod
    def find_unread_by_class(
        db: Session,
        grade: int,
        class_name: str
    ) -> List[Tuple[RenrakuchoEntryModel, str]]:
        
        return db.query(
            RenrakuchoEntryModel,
            Account.name.label("student_name")
        ).join(
            Account,
            RenrakuchoEntryModel.student_id == Account.id
        ).filter(
            Account.grade == grade,
            Account.class_name == class_name,
            RenrakuchoEntryModel.is_read == False
        ).order_by(
            RenrakuchoEntryModel.submitted_date.asc()
        ).all()

    # 養護教諭用）体調・メンタルが低い（2以下）連絡帳を取得
    @staticmethod
    def find_critical_entries(
        db: Session,
        submitted_date: Optional[date] = None
    ) -> List[Tuple[RenrakuchoEntryModel, Account]]:
        query = db.query(
            RenrakuchoEntryModel,
            Account
        ).join(
            Account,
            RenrakuchoEntryModel.student_id == Account.id
        ).filter(
            or_(
                RenrakuchoEntryModel.physical_condition <= 2,
                RenrakuchoEntryModel.mental_state <= 2
            )
        )
    
        # 日付フィルタ（任意）
        if submitted_date:
            query = query.filter(RenrakuchoEntryModel.submitted_date == submitted_date)
    
        return query.order_by(
            RenrakuchoEntryModel.physical_condition.asc(),
            RenrakuchoEntryModel.mental_state.asc()
        ).all()

    # 担任・副担任）指定日の提出済み生徒情報の取得
    @staticmethod
    def find_submitted_students_by_date(
        db: Session,
        grade: int,
        class_name: str,
        target_date: date
    ) -> List[Account]:
        
        return db.query(Account).join(
            RenrakuchoEntryModel,
            Account.id == RenrakuchoEntryModel.student_id
        ).filter(
            Account.grade == grade,
            Account.class_name == class_name,
            RenrakuchoEntryModel.target_date == target_date
        ).all()

    # 担任・副担任）指定日の未提出の生徒情報の取得
    @staticmethod
    def find_not_submitted_students_by_date(
        db: Session,
        grade: int,
        class_name: str,
        target_date: date
    ) -> List[Account]:
        
        # 提出済みの生徒IDを取得
        submitted_student_ids = db.query(RenrakuchoEntryModel.student_id).join(
            Account,
            RenrakuchoEntryModel.student_id == Account.id
        ).filter(
            Account.grade == grade,
            Account.class_name == class_name,
            RenrakuchoEntryModel.target_date == target_date
        ).subquery()

        # 提出済み以外の生徒を取得
        return db.query(Account).filter(
            Account.grade == grade,
            Account.class_name == class_name,
            Account.role == 'student',
            ~Account.id.in_(submitted_student_ids)
        ).all()

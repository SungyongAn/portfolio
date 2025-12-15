from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.renrakucho_model import RenrakuchoEntryModel
from app.schemas.renrakucho_schema import (
    RenrakuchoEntryRequest,
    PastRenrakuchoRecord,
)
from datetime import date
from app.websocket.notifications import notify_critical_entry_async
from app.repositories.renrakucho_repository import RenrakuchoRepository
from app.repositories.account_repository import AccountRepository
from fastapi import BackgroundTasks
import logging

logger = logging.getLogger(__name__)


class RenrakuchoService:
    # 連絡帳の登録（BackgroundTasks対応版）
    @staticmethod
    def create_entry(db: Session, entry: RenrakuchoEntryRequest, background_tasks: BackgroundTasks = None) -> dict:
        # 既存エントリーチェック（リポジトリを使用）
        existing_entry = RenrakuchoRepository.find_by_student_and_date(
            db,
            entry.student_id,
            entry.target_date
        )

        if existing_entry:
            return {
                "success": False,
                "message": f"{entry.target_date} の連絡帳は既に提出済みです。",
                "data": None,
            }

        # 新規連絡帳の作成
        db_entry = RenrakuchoEntryModel(
            student_id=entry.student_id,
            submitted_date=entry.submitted_date,
            target_date=entry.target_date,
            physical_condition=entry.physical_condition,
            mental_state=entry.mental_state,
            physical_mental_notes=entry.physical_mental_notes,
            daily_reflection=entry.daily_reflection,
        )

        try:
            # リポジトリを使用して作成
            db_entry = RenrakuchoRepository.create(db, db_entry)

            # 体調またはメンタルが2以下の場合はWebSocket通知
            if db_entry.physical_condition <= 2 or db_entry.mental_state <= 2:
                # リポジトリを使用して生徒情報を取得
                student = AccountRepository.find_by_id(db, db_entry.student_id)
                
                if student:
                    entry_dict = {
                        "renrakucho_id": db_entry.renrakucho_id,
                        "student_id": db_entry.student_id,
                        "student_name": student.name,
                        "grade": student.grade,
                        "class_name": student.class_name,
                        "physical_condition": db_entry.physical_condition,
                        "mental_state": db_entry.mental_state,
                        "physical_mental_notes": db_entry.physical_mental_notes,
                        "submitted_date": db_entry.submitted_date.isoformat(),
                        "target_date": db_entry.target_date.isoformat(),
                    }
                    
                    # BackgroundTasksが提供されている場合はそれを使用
                    if background_tasks:
                        background_tasks.add_task(notify_critical_entry_async, entry_dict)
                        logger.info(f"Notification scheduled for student {student.name}")
                    else:
                        logger.warning("BackgroundTasks not provided, notification skipped")
                else:
                    logger.warning(f"Student not found for notification: student_id={db_entry.student_id}")

            return {
                "success": True,
                "message": "連絡帳を提出しました。",
                "data": db_entry,
            }

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error in create_entry: {str(e)}")
            return {
                "success": False,
                "message": f"データベースエラーが発生しました: {str(e)}",
                "data": None,
            }

    # 過去の連絡帳の検索
    @staticmethod
    def get_past_renrakucho(
        db: Session,
        student_id: int | None = None,
        grade: int | None = None,
        class_name: str | None = None,
        student_name: str | None = None,
        teacher_name: str | None = None,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        weekday: int | None = None,
        is_read: int | None = None,
    ):
        # 生徒単位検索
        if student_id is not None:
            # リポジトリを使用
            records = RenrakuchoRepository.find_by_student(
                db,
                student_id=student_id,
                year=year,
                month=month,
                day=day,
                weekday=weekday
            )
            
            result = [
                PastRenrakuchoRecord(
                    record_date=r.target_date,
                    physical_condition=r.physical_condition,
                    mental_state=r.mental_state,
                    physical_mental_notes=r.physical_mental_notes,
                    daily_reflection=r.daily_reflection,
                    teacher_checked=r.is_read,
                    created_at=r.created_at,
                )
                for r in records
            ]
            return result

        # クラス単位検索（教師用）
        elif grade is not None and class_name is not None:
            # リポジトリを使用
            records = RenrakuchoRepository.find_by_class_with_student_info(
                db,
                grade=grade,
                class_name=class_name,
                student_name=student_name,
                year=year,
                month=month,
                day=day,
                weekday=weekday,
                is_read=bool(is_read) if is_read is not None else None
            )
            
            result = [
                PastRenrakuchoRecord(
                    record_date=r.RenrakuchoEntryModel.target_date,
                    physical_condition=r.RenrakuchoEntryModel.physical_condition,
                    mental_state=r.RenrakuchoEntryModel.mental_state,
                    physical_mental_notes=r.RenrakuchoEntryModel.physical_mental_notes,
                    daily_reflection=r.RenrakuchoEntryModel.daily_reflection,
                    teacher_checked=r.RenrakuchoEntryModel.is_read,
                    created_at=r.RenrakuchoEntryModel.created_at,
                    student_id=r.RenrakuchoEntryModel.student_id,
                    student_name=r.student_name,
                )
                for r in records
            ]
            return result
        else:
            return []

    # 教師の担当クラスの未チェックの連絡帳検索
    @staticmethod
    def get_class_not_checked_unviewed(
        db: Session, grade: int, class_name: str
    ) -> list[dict]:
        # リポジトリを使用
        records = RenrakuchoRepository.find_unread_by_class(db, grade, class_name)

        return [
            {
                "renrakucho_id": r.RenrakuchoEntryModel.renrakucho_id,
                "student_id": r.RenrakuchoEntryModel.student_id,
                "student_name": r.student_name,
                "record_date": r.RenrakuchoEntryModel.target_date,
                "physical_condition": r.RenrakuchoEntryModel.physical_condition,
                "mental_state": r.RenrakuchoEntryModel.mental_state,
                "physical_mental_notes": r.RenrakuchoEntryModel.physical_mental_notes,
                "daily_reflection": r.RenrakuchoEntryModel.daily_reflection,
                "teacher_checked": r.RenrakuchoEntryModel.is_read,
                "submitted_date": r.RenrakuchoEntryModel.submitted_date,
                "created_at": r.RenrakuchoEntryModel.created_at,
            }
            for r in records
        ]

    # 連絡帳の既読更新(複数可能)
    @staticmethod
    def mark_as_read(db: Session, renrakucho_ids: list[int]) -> int:
        try:
            # リポジトリを使用
            updated = RenrakuchoRepository.mark_as_read(db, renrakucho_ids)
            return updated

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error in mark_as_read: {str(e)}")
            raise

    # 連絡帳の提出状況の確認
    @staticmethod
    def get_submission_status(
        db: Session,
        grade: int,
        class_name: str,
        target_date: date
    ) -> dict:
        # リポジトリを使用して提出済み・未提出生徒を取得
        submitted_students_accounts = RenrakuchoRepository.find_submitted_students_by_date(
            db, grade, class_name, target_date
        )
        
        not_submitted_students_accounts = RenrakuchoRepository.find_not_submitted_students_by_date(
            db, grade, class_name, target_date
        )
        
        # 提出済み生徒の提出日時を取得するため、連絡帳データも取得
        submitted_entries = RenrakuchoRepository.find_by_class_with_student_info(
            db,
            grade=grade,
            class_name=class_name,
            year=target_date.year,
            month=target_date.month,
            day=target_date.day
        )
        
        # 提出日時のマッピングを作成
        submission_date_map = {
            entry.RenrakuchoEntryModel.student_id: entry.RenrakuchoEntryModel.submitted_date
            for entry in submitted_entries
        }

        submitted_students = [
            {
                "student_id": s.id,
                "student_name": s.name,
                "submitted_at": submission_date_map.get(s.id).isoformat() if submission_date_map.get(s.id) else None
            }
            for s in submitted_students_accounts
        ]

        not_submitted_students = [
            {
                "student_id": s.id,
                "student_name": s.name
            }
            for s in not_submitted_students_accounts
        ]
        
        total_students = len(submitted_students) + len(not_submitted_students)

        return {
            "total_students": total_students,
            "submitted_count": len(submitted_students),
            "not_submitted_count": len(not_submitted_students),
            "submitted_students": submitted_students,
            "not_submitted_students": not_submitted_students
        }

    # 養護教諭用：体調・メンタル低値の連絡帳を取得
    @staticmethod
    def get_critical_entries(db: Session, target_date: date = None) -> list[dict]:
        """
        体調・メンタル低値の連絡帳を取得（養護教諭用）
        
        Args:
            db: データベースセッション
            target_date: 対象日（Noneの場合は当日）
            
        Returns:
            list[dict]: 要注意連絡帳のリスト
        """
        if target_date is None:
            target_date = date.today()
        
        # リポジトリを使用（日付フィルタ付き）
        entries = RenrakuchoRepository.find_critical_entries(db, submitted_date=target_date)
        
        # レスポンス形式に整形
        return [
            {
                "renrakucho_id": entry.renrakucho_id,
                "student_id": entry.student_id,
                "student_name": student.name,
                "grade": student.grade,
                "class_name": student.class_name,
                "physical_condition": entry.physical_condition,
                "mental_state": entry.mental_state,
                "physical_mental_notes": entry.physical_mental_notes,
                "submitted_date": entry.submitted_date.isoformat(),
                "target_date": entry.target_date.isoformat(),
                "created_at": entry.created_at.isoformat() if entry.created_at else None
            }
            for entry, student in entries
        ]

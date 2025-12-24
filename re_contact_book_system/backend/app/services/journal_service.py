from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.journal import JournalEntry
from app.models.user import User
from app.schemas.journal import JournalCreate
from datetime import date, datetime, timedelta
from typing import Optional, List


def calculate_entry_date(target_date: date = None) -> date:
    """
    前登校日を計算（土日をスキップ）
    
    Args:
        target_date: 基準日（省略時は今日）
    
    Returns:
        date: 前登校日
    """
    if target_date is None:
        target_date = date.today()
    
    weekday = target_date.weekday()  # 0=月曜, 6=日曜
    
    if weekday == 0:  # 月曜日
        return target_date - timedelta(days=3)  # 金曜日
    elif weekday == 6:  # 日曜日
        return target_date - timedelta(days=2)  # 金曜日
    else:
        return target_date - timedelta(days=1)  # 前日


def create_journal(db: Session, student_id: int, journal_data: JournalCreate) -> JournalEntry:
    """
    連絡帳を作成
    
    Args:
        db: データベースセッション
        student_id: 生徒ID
        journal_data: 連絡帳データ
    
    Returns:
        JournalEntry: 作成された連絡帳
    """
    entry = JournalEntry(
        student_id=student_id,
        entry_date=journal_data.entry_date,
        submission_date=date.today(),
        physical_condition=journal_data.physical_condition,
        mental_condition=journal_data.mental_condition,
        reflection_text=journal_data.reflection_text
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def mark_as_read(db: Session, journal_id: int, teacher_id: int) -> Optional[JournalEntry]:
    """
    連絡帳を既読にする
    
    Args:
        db: データベースセッション
        journal_id: 連絡帳ID
        teacher_id: 教師ID
    
    Returns:
        JournalEntry: 更新された連絡帳
    """
    entry = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if entry:
        entry.is_read = True
        entry.read_by = teacher_id
        entry.read_at = datetime.utcnow()
        db.commit()
        db.refresh(entry)
    return entry


def get_student_journals(
    db: Session,
    student_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[JournalEntry]:
    """
    生徒の連絡帳一覧を取得
    
    Args:
        db: データベースセッション
        student_id: 生徒ID
        limit: 取得件数
        offset: オフセット
    
    Returns:
        List[JournalEntry]: 連絡帳リスト
    """
    return db.query(JournalEntry).filter(
        JournalEntry.student_id == student_id
    ).order_by(
        JournalEntry.entry_date.desc()
    ).limit(limit).offset(offset).all()


def check_today_submission(db: Session, student_id: int) -> Optional[JournalEntry]:
    """
    今日の連絡帳が提出済みか確認
    
    Args:
        db: データベースセッション
        student_id: 生徒ID
    
    Returns:
        JournalEntry: 今日提出した連絡帳（なければNone）
    """
    today = date.today()
    return db.query(JournalEntry).filter(
        and_(
            JournalEntry.student_id == student_id,
            JournalEntry.submission_date == today
        )
    ).first()


def get_class_submissions(
    db: Session,
    class_id: int,
    submission_date: date = None
) -> List[JournalEntry]:
    """
    クラスの連絡帳提出状況を取得
    
    Args:
        db: データベースセッション
        class_id: クラスID
        submission_date: 提出日（省略時は今日）
    
    Returns:
        List[JournalEntry]: 提出された連絡帳リスト
    """
    if submission_date is None:
        submission_date = date.today()
    
    from app.models.class_model import StudentClassAssignment
    
    # クラスに所属する生徒の連絡帳を取得
    return db.query(JournalEntry).join(
        User, JournalEntry.student_id == User.id
    ).join(
        StudentClassAssignment, User.id == StudentClassAssignment.student_id
    ).filter(
        and_(
            StudentClassAssignment.class_id == class_id,
            StudentClassAssignment.is_current == True,
            JournalEntry.submission_date == submission_date
        )
    ).all()


def get_journal_by_id(db: Session, journal_id: int) -> Optional[JournalEntry]:
    """
    連絡帳をIDで取得
    
    Args:
        db: データベースセッション
        journal_id: 連絡帳ID
    
    Returns:
        JournalEntry: 連絡帳（見つからない場合はNone）
    """
    return db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()

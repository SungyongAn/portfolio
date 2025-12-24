from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.user import User
from app.models.class_model import TeacherAssignment, AssignmentTypeEnum, StudentClassAssignment
from app.models.journal import JournalEntry
from typing import List, Optional
from datetime import date


def get_teacher_classes(db: Session, teacher_id: int) -> List[int]:
    """
    教師が担当するクラスIDのリストを取得
    
    Args:
        db: データベースセッション
        teacher_id: 教師ID
    
    Returns:
        List[int]: クラスIDのリスト
    """
    assignments = db.query(TeacherAssignment).filter(
        TeacherAssignment.teacher_id == teacher_id,
        TeacherAssignment.class_id.isnot(None)
    ).all()
    
    return [assignment.class_id for assignment in assignments]


def get_teacher_grades(db: Session, teacher_id: int) -> List[int]:
    """
    教師が担当する学年IDのリストを取得
    
    Args:
        db: データベースセッション
        teacher_id: 教師ID
    
    Returns:
        List[int]: 学年IDのリスト
    """
    assignments = db.query(TeacherAssignment).filter(
        TeacherAssignment.teacher_id == teacher_id,
        TeacherAssignment.grade_id.isnot(None)
    ).all()
    
    return [assignment.grade_id for assignment in assignments]


def can_view_journal(db: Session, teacher_id: int, journal_id: int) -> bool:
    """
    教師が連絡帳を閲覧できるか確認
    
    Args:
        db: データベースセッション
        teacher_id: 教師ID
        journal_id: 連絡帳ID
    
    Returns:
        bool: 閲覧可能ならTrue
    """
    journal = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if not journal:
        return False
    
    # 生徒のクラス情報を取得
    student_class = db.query(StudentClassAssignment).filter(
        and_(
            StudentClassAssignment.student_id == journal.student_id,
            StudentClassAssignment.is_current == True
        )
    ).first()
    
    if not student_class:
        return False
    
    # 教師の割当を確認
    teacher_assignment = db.query(TeacherAssignment).filter(
        TeacherAssignment.teacher_id == teacher_id,
        or_(
            # 担任としてクラスを担当
            TeacherAssignment.class_id == student_class.class_id,
            # 学年主任として学年を担当
            and_(
                TeacherAssignment.assignment_type == AssignmentTypeEnum.grade_head,
                TeacherAssignment.grade_id == student_class.class_obj.grade_id
            ),
            # 管理者
            TeacherAssignment.assignment_type == AssignmentTypeEnum.administrator
        )
    ).first()
    
    return teacher_assignment is not None


def get_submission_status(
    db: Session,
    class_id: int,
    target_date: date = None
) -> List[dict]:
    """
    クラスの提出状況を取得
    
    Args:
        db: データベースセッション
        class_id: クラスID
        target_date: 対象日（省略時は今日）
    
    Returns:
        List[dict]: 提出状況リスト
    """
    if target_date is None:
        target_date = date.today()
    
    # クラスの生徒一覧を取得
    students = db.query(User).join(
        StudentClassAssignment, User.id == StudentClassAssignment.student_id
    ).filter(
        StudentClassAssignment.class_id == class_id,
        StudentClassAssignment.is_current == True
    ).all()
    
    status_list = []
    for student in students:
        # その日の提出を確認
        journal = db.query(JournalEntry).filter(
            and_(
                JournalEntry.student_id == student.id,
                JournalEntry.submission_date == target_date
            )
        ).first()
        
        status_list.append({
            "student_id": student.id,
            "student_name": student.name,
            "has_submitted": journal is not None,
            "is_read": journal.is_read if journal else False,
            "journal_id": journal.id if journal else None,
            "submission_date": journal.submission_date if journal else None
        })
    
    return status_list


def is_teacher_of_class(db: Session, teacher_id: int, class_id: int) -> bool:
    """
    教師が指定クラスの担当か確認
    
    Args:
        db: データベースセッション
        teacher_id: 教師ID
        class_id: クラスID
    
    Returns:
        bool: 担当ならTrue
    """
    assignment = db.query(TeacherAssignment).filter(
        TeacherAssignment.teacher_id == teacher_id,
        TeacherAssignment.class_id == class_id
    ).first()
    
    return assignment is not None


def is_grade_head(db: Session, teacher_id: int, grade_id: int) -> bool:
    """
    教師が学年主任か確認
    
    Args:
        db: データベースセッション
        teacher_id: 教師ID
        grade_id: 学年ID
    
    Returns:
        bool: 学年主任ならTrue
    """
    assignment = db.query(TeacherAssignment).filter(
        TeacherAssignment.teacher_id == teacher_id,
        TeacherAssignment.assignment_type == AssignmentTypeEnum.grade_head,
        TeacherAssignment.grade_id == grade_id
    ).first()
    
    return assignment is not None

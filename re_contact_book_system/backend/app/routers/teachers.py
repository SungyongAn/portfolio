from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.journal import SubmissionStatusResponse, JournalResponse
from app.services.teacher_service import (
    get_teacher_classes,
    get_submission_status,
    is_teacher_of_class
)
from app.services.journal_service import get_class_submissions
from app.dependencies import get_current_teacher, get_current_teacher_or_admin
from app.models.user import User
from typing import List
from datetime import date

router = APIRouter(prefix="/api/teachers", tags=["教師機能"])


# 担当クラス一覧を取得
@router.get("/my-classes")
def get_my_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):

    class_ids = get_teacher_classes(db, current_user.id)
    
    if not class_ids:
        return {
            "message": "担当クラスがありません",
            "class_ids": []
        }
    
    # クラス詳細情報を取得
    from app.models.class_model import Class
    classes = db.query(Class).filter(Class.id.in_(class_ids)).all()
    
    result = []
    for cls in classes:
        result.append({
            "class_id": cls.id,
            "class_name": cls.class_name,
            "grade_number": cls.grade.grade_number,
            "grade_id": cls.grade_id
        })
    
    return {
        "classes": result,
        "total": len(result)
    }


@router.get("/classes/{class_id}/submissions", response_model=List[SubmissionStatusResponse])
def get_class_submission_status(
    class_id: int,
    submission_date: date = Query(default=None, description="提出日（省略時は今日）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    """
    クラスの提出状況を取得
    
    指定クラスの連絡帳提出状況を一覧で取得する。
    教師は担当クラスのみ、管理者は全クラスを閲覧可能。
    """
    # 教師の場合、担当クラスか確認
    from app.models.user import RoleEnum
    if current_user.role == RoleEnum.teacher:
        if not is_teacher_of_class(db, current_user.id, class_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="このクラスの提出状況を閲覧する権限がありません"
            )
    
    # 提出状況を取得
    status_list = get_submission_status(db, class_id, submission_date)
    
    return [SubmissionStatusResponse(**item) for item in status_list]


@router.get("/classes/{class_id}/journals", response_model=List[JournalResponse])
def get_class_journals(
    class_id: int,
    submission_date: date = Query(default=None, description="提出日（省略時は今日）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    """
    クラスの連絡帳一覧を取得
    
    指定クラス・指定日の連絡帳を全て取得する。
    """
    # 教師の場合、担当クラスか確認
    from app.models.user import RoleEnum
    if current_user.role == RoleEnum.teacher:
        if not is_teacher_of_class(db, current_user.id, class_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="このクラスの連絡帳を閲覧する権限がありません"
            )
    
    # 連絡帳を取得
    journals = get_class_submissions(db, class_id, submission_date)
    
    # レスポンス用に生徒名を追加
    result = []
    for journal in journals:
        response = JournalResponse.from_orm(journal)
        if journal.student:
            response.student_name = journal.student.name
        result.append(response)
    
    return result


@router.get("/dashboard")
def get_teacher_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """
    教師ダッシュボード情報を取得
    
    担当クラスの提出状況サマリーを返す。
    """
    class_ids = get_teacher_classes(db, current_user.id)
    
    if not class_ids:
        return {
            "message": "担当クラスがありません",
            "summary": []
        }
    
    # 各クラスの提出状況を集計
    summary = []
    for class_id in class_ids:
        status_list = get_submission_status(db, class_id)
        
        total_students = len(status_list)
        submitted_count = sum(1 for s in status_list if s["has_submitted"])
        read_count = sum(1 for s in status_list if s["is_read"])
        
        # クラス情報を取得
        from app.models.class_model import Class
        cls = db.query(Class).filter(Class.id == class_id).first()
        
        summary.append({
            "class_id": class_id,
            "class_name": cls.class_name if cls else "不明",
            "grade_number": cls.grade.grade_number if cls else None,
            "total_students": total_students,
            "submitted_count": submitted_count,
            "unsubmitted_count": total_students - submitted_count,
            "read_count": read_count,
            "unread_count": submitted_count - read_count,
            "submission_rate": round(submitted_count / total_students * 100, 1) if total_students > 0 else 0
        })
    
    return {
        "date": date.today().isoformat(),
        "summary": summary,
        "total_classes": len(summary)
    }


@router.get("/unread-journals", response_model=List[JournalResponse])
def get_unread_journals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """
    未読の連絡帳一覧を取得
    
    担当クラスの未読連絡帳を全て取得する。
    """
    class_ids = get_teacher_classes(db, current_user.id)
    
    if not class_ids:
        return []
    
    # 各クラスの未読連絡帳を取得
    from app.models.journal import JournalEntry
    from app.models.class_model import StudentClassAssignment
    from app.models.user import User as UserModel
    
    unread_journals = db.query(JournalEntry).join(
        UserModel, JournalEntry.student_id == UserModel.id
    ).join(
        StudentClassAssignment, UserModel.id == StudentClassAssignment.student_id
    ).filter(
        StudentClassAssignment.class_id.in_(class_ids),
        StudentClassAssignment.is_current == True,
        JournalEntry.is_read == False
    ).order_by(JournalEntry.submission_date.desc()).all()
    
    # レスポンス用に生徒名を追加
    result = []
    for journal in unread_journals:
        response = JournalResponse.from_orm(journal)
        if journal.student:
            response.student_name = journal.student.name
        result.append(response)
    
    return result

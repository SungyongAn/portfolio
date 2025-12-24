from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.journal import JournalCreate, JournalResponse, JournalListResponse
from app.services.journal_service import (
    create_journal,
    get_student_journals,
    check_today_submission,
    calculate_entry_date,
    mark_as_read,
    get_journal_by_id
)
from app.services.teacher_service import can_view_journal
from app.dependencies import get_current_user, get_current_student, get_current_teacher
from app.models.user import User, RoleEnum
from typing import List

router = APIRouter(prefix="/api/journals", tags=["連絡帳"])


# 生徒手帳の提出処理（1日1回のみ提出可）
@router.post("/", response_model=JournalResponse, status_code=status.HTTP_201_CREATED)
def submit_journal(
    journal_data: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):

    # 今日すでに提出済みか確認
    existing = check_today_submission(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="本日の連絡帳は既に提出済みです"
        )
    
    # 連絡帳を作成
    entry = create_journal(db, current_user.id, journal_data)
    
    # レスポンス用に生徒名を追加
    response = JournalResponse.from_orm(entry)
    response.student_name = current_user.name
    
    return response


# 過去の連絡帳を取得
@router.get("/history", response_model=List[JournalResponse])
def get_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):

    journals = get_student_journals(db, current_user.id, limit, offset)
    
    # レスポンス用に生徒名を追加
    result = []
    for journal in journals:
        response = JournalResponse.from_orm(journal)
        response.student_name = current_user.name
        result.append(response)
    
    return result


# 今日の連絡帳を取得
@router.get("/today", response_model=JournalResponse)
def get_today_journal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):

    journal = check_today_submission(db, current_user.id)
    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="本日の連絡帳はまだ提出されていません"
        )
    
    response = JournalResponse.from_orm(journal)
    response.student_name = current_user.name
    
    return response


# 推奨される記入対象日を取得(土日はスキップ)
@router.get("/suggested-date")
def get_suggested_date(current_user: User = Depends(get_current_student)):
    entry_date = calculate_entry_date()
    return {
        "entry_date": entry_date.isoformat(),
        "message": f"記入対象日: {entry_date.strftime('%Y年%m月%d日')}"
    }


# 連絡帳の詳細を取得 生徒は自分の連絡帳のみ、教師は担当クラスの連絡帳を閲覧可
@router.get("/{journal_id}", response_model=JournalResponse)
def get_journal_detail(
    journal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    journal = get_journal_by_id(db, journal_id)
    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="連絡帳が見つかりません"
        )
    
    # 権限チェック
    if current_user.role == RoleEnum.student:
        # 生徒は自分の連絡帳のみ閲覧可能
        if journal.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="他の生徒の連絡帳は閲覧できません"
            )
    elif current_user.role == RoleEnum.teacher:
        # 教師は担当クラスの連絡帳のみ閲覧可能
        if not can_view_journal(db, current_user.id, journal_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この連絡帳を閲覧する権限がありません"
            )
    # 管理者は全て閲覧可能
    
    response = JournalResponse.from_orm(journal)
    if journal.student:
        response.student_name = journal.student.name
    
    return response


# 連絡帳を既読にする
@router.put("/{journal_id}/read", response_model=JournalResponse)
def mark_journal_as_read(
    journal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    
    # 連絡帳を取得
    journal = get_journal_by_id(db, journal_id)
    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="連絡帳が見つかりません"
        )
    
    # 権限チェック
    if not can_view_journal(db, current_user.id, journal_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この連絡帳を既読にする権限がありません"
        )
    
    # 既読処理
    updated_journal = mark_as_read(db, journal_id, current_user.id)
    
    response = JournalResponse.from_orm(updated_journal)
    if updated_journal.student:
        response.student_name = updated_journal.student.name
    
    return response

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date
import logging
from routes.db.db import get_db
from routes.services.renrakucho_service import RenrakuchoService
from routes.models.renrakucho_model import RenrakuchoEntryModel
from routes.models.accounts_model import Account
from routes.schemas.renrakucho_schema import (
    RenrakuchoEntryRequest,
    RenrakuchoEntryResponse,
    PastRenrakuchoSearchRequest,
    PastRenrakuchoSearchResponse,
    ClassNotCheckedRenrakuchoRequest,
    MarkAsReadRequest,
    MarkAsReadResponse,
    SubmissionStatusRequest,
    SubmissionStatusResponse
)

router = APIRouter()

logger = logging.getLogger(__name__)


# 生徒用）連絡帳の登録
@router.post("/entry-renrakucho", response_model=RenrakuchoEntryResponse)
def entry_renrakucho(entry_data: RenrakuchoEntryRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    result = RenrakuchoService.create_entry(db, entry_data, background_tasks=background_tasks)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    db_entry = result["data"]

    response_data = {
        "id": db_entry.renrakucho_id,
        "student_id": db_entry.student_id,
        "submitted_date": (
            db_entry.submitted_date.isoformat() if db_entry.submitted_date else None
        ),
        "target_date": (
            db_entry.target_date.isoformat() if db_entry.target_date else None
        ),
        "physical_condition": db_entry.physical_condition,
        "mental_state": db_entry.mental_state,
        "daily_reflection": db_entry.daily_reflection,
    }

    return RenrakuchoEntryResponse(
        success=True,
        message=result["message"],
        data=response_data,
    )


# 生徒、教師共有）過去の履歴帳検索
@router.post("/past-renrakucho-search", response_model=PastRenrakuchoSearchResponse)
def search_past_renrakucho(payload: PastRenrakuchoSearchRequest, db: Session = Depends(get_db)):
    try:
        if payload.flag:  # クラス単位検索(教師用)
            records = RenrakuchoService.get_past_renrakucho(
                db=db,
                grade=payload.grade,
                class_name=payload.class_name,
                teacher_name=payload.teacher_name,
                student_name=payload.student_name,
                year=payload.year,
                month=payload.month,
                day=payload.day,
                weekday=payload.weekday,
                is_read=payload.is_read
                )
            
        else:  # 生徒単位検索
            records = RenrakuchoService.get_past_renrakucho(
                db=db,
                student_id=payload.student_id,
                year=payload.year,
                month=payload.month,
                day=payload.day,
                weekday=payload.weekday,
                is_read=payload.is_read
                )
            
        if not records:
            return PastRenrakuchoSearchResponse(success=True, message="該当する連絡帳はありません", data=[])

        return PastRenrakuchoSearchResponse(success=True, message="取得成功", data=records)

    except Exception:
        return PastRenrakuchoSearchResponse(
            success=False,
            message="取得中にエラーが発生しました",
            data=None
        )


# 教師の担当クラスの未確認連絡帳の検索
@router.post("/class-not-checked-renrakucho")
def get_class_today_renrakucho(
    payload: ClassNotCheckedRenrakuchoRequest,
    db: Session = Depends(get_db)
):
    data = RenrakuchoService.get_class_not_checked_unviewed(db, payload.grade, payload.class_name)
    if not data:
        raise HTTPException(status_code=404, detail="未確認の連絡帳はありません。")
    return {"success": True, "data": data}


# 連絡帳を既読にする
@router.post("/mark-as-read")
def mark_as_read(
    payload: MarkAsReadRequest,
    db: Session = Depends(get_db)
):
    try:
        updated_count = RenrakuchoService.mark_as_read(db, payload.renrakucho_ids)
        
        return MarkAsReadResponse(
            success=True,
            message=f"{updated_count}件の連絡帳を既読にしました",
            data={"updated_count": updated_count}
        )
    
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="既読更新に失敗しました"
        )


# 連絡帳提出状況の確認
@router.post("/submission-status", response_model=SubmissionStatusResponse)
def get_submission_status(
    payload: SubmissionStatusRequest,
    db: Session = Depends(get_db)
):
    try:
        data = RenrakuchoService.get_submission_status(
            db, 
            payload.grade, 
            payload.class_name, 
            payload.target_date
        )
        
        return SubmissionStatusResponse(
            success=True,
            message="提出状況を取得しました",
            data=data
        )
    
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="提出状況の取得に失敗しました"
        )


# 養護教諭用: 要注意連絡帳の取得（体調またはメンタルが2以下）
@router.get("/critical-entries")
def get_critical_entries(
    date_filter: date = Query(default=None, description="対象日付"),
    db: Session = Depends(get_db)
):

    try:
        # Service層を使用
        result = RenrakuchoService.get_critical_entries(db, date_filter)
        
        return {
            "success": True,
            "message": f"{len(result)}件の要注意連絡帳が見つかりました",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error in get_critical_entries: {str(e)}")
        return {
            "success": False,
            "message": "エラーが発生しました",
            "data": []
        }


# 連絡帳の詳細取得
@router.get("/entry/{renrakucho_id}")
def get_entry_detail(
    renrakucho_id: int,
    db: Session = Depends(get_db)
):

    try:
        # 連絡帳と生徒情報を取得
        entry_data = db.query(
            RenrakuchoEntryModel,
            Account.name.label('student_name'),
            Account.grade,
            Account.class_name
        ).join(
            Account, RenrakuchoEntryModel.student_id == Account.id
        ).filter(
            RenrakuchoEntryModel.renrakucho_id == renrakucho_id
        ).first()
        
        if not entry_data:
            return {
                "success": False,
                "message": "連絡帳が見つかりませんでした",
                "data": None
            }

        entry = entry_data[0]
        student_name = entry_data[1]
        grade = entry_data[2]
        class_name = entry_data[3]
        
        result = {
            "renrakucho_id": entry.renrakucho_id,
            "student_id": entry.student_id,
            "student_name": student_name,
            "grade": grade,
            "class_name": class_name,
            "submitted_date": entry.submitted_date.isoformat(),
            "target_date": entry.target_date.isoformat(),
            "physical_condition": entry.physical_condition,
            "mental_state": entry.mental_state,
            "physical_mental_notes": entry.physical_mental_notes,
            "daily_reflection": entry.daily_reflection,
            "is_read": entry.is_read,
            "created_at": entry.created_at.isoformat() if entry.created_at else None
        }
        
        return {
            "success": True,
            "message": "連絡帳の詳細を取得しました",
            "data": result
        }
        
    except Exception:
        return {
            "success": False,
            "message": "詳細取得エラー",
            "data": None
        }

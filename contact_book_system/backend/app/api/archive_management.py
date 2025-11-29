from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.services.archive_service import ArchiveService
from app.schemas.archive_schema import (
    ArchiveExecutionRequest,
    DeleteExecutionRequest
)
from app.services.auth import get_current_user
from app.models.accounts_model import Account, RoleEnum


router = APIRouter(prefix="/archive-management", tags=["Archive Management"])


def require_admin(current_user: Account = Depends(get_current_user)):
    """管理者権限チェック"""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/statistics")
async def get_archive_statistics(
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin)
):
    """
    アーカイブ統計を取得
    
    管理者のみアクセス可能
    """
    result = ArchiveService.get_statistics(db)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@router.post("/execute-archive")
async def execute_archive(
    request: ArchiveExecutionRequest,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin)
):
    """
    アーカイブを手動実行
    
    管理者のみアクセス可能
    """
    result = ArchiveService.execute_archive(
        db, 
        archive_years=request.archive_years
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@router.post("/execute-deletion")
async def execute_deletion(
    request: DeleteExecutionRequest,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin)
):
    """
    期限切れデータを削除
    
    管理者のみアクセス可能
    
    ⚠️ 警告: この操作は元に戻せません
    """
    result = ArchiveService.execute_deletion(
        db,
        retention_years=request.retention_years
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@router.get("/deletion-logs")
async def get_deletion_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin)
):
    """
    削除ログを取得
    
    管理者のみアクセス可能
    """
    result = ArchiveService.get_deletion_logs(db, limit=limit)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@router.get("/search-archive")
async def search_archive(
    student_name: str = None,
    year: int = None,
    month: int = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin)
):
    """
    アーカイブデータを検索
    
    管理者のみアクセス可能
    """
    result = ArchiveService.search_archive(
        db,
        student_name=student_name,
        year=year,
        month=month,
        limit=limit
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result

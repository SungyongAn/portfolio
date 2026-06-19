from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.schemas.task import TaskResponse
from app.services import task_service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["管理タスク"])


@router.get("/all", response_model=list[TaskResponse], operation_id="get_all_tasks")
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """本部管理者用 全案件タスク取得"""
    return task_service.get_all_tasks(db, current_user)

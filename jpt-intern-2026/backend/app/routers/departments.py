from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.department import Department
from app.dependencies.auth import get_current_user
from app.models.user import User
from pydantic import BaseModel
from app.schemas.task import TaskResponse
from app.services import task_service


class DepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


router = APIRouter(prefix="/api/departments", tags=["部門"])


@router.get("", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """部門一覧取得（全ロール対応）"""
    return db.query(Department).all()


@router.get(
    "/{department_id}/tasks",
    response_model=list[TaskResponse],
    operation_id="get_department_tasks",
)
def get_department_tasks(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """部門内の全タスク一覧取得"""
    return task_service.get_department_tasks(db, department_id, current_user)

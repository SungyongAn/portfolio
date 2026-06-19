from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/api/projects/{project_id}/tasks", tags=["タスク"])


@router.post("", response_model=TaskResponse, operation_id="create_task")
def create_task(
    project_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """タスク作成"""
    return task_service.create_task(db, project_id, task_data, current_user)


@router.get("", response_model=list[TaskResponse], operation_id="list_tasks")
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """タスク一覧取得"""
    return task_service.get_tasks(db, project_id, current_user)


@router.put("/{task_id}", response_model=TaskResponse, operation_id="update_task")
def update_task(
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.APPLICANT, UserRole.TASK_MEMBER])),
):
    """タスク更新"""
    return task_service.update_task(db, project_id, task_id, task_data, current_user)


@router.delete("/{task_id}", status_code=204, operation_id="delete_task")
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """タスク削除"""
    task_service.delete_task(db, project_id, task_id, current_user)
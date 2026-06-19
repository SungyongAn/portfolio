from datetime import timezone, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.task import Task, TaskStatus
from app.models.project import Project, ProjectStatus
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.project.permission_service import check_project_access


def _check_project_exists(project: Project | None) -> Project:
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="案件が見つかりません",
        )
    return project


def _check_project_approved(project: Project) -> None:
    if project.status not in [
        ProjectStatus.APPROVED,
        ProjectStatus.IN_PROGRESS,
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="承認済みまたは進行中の案件のみタスクを管理できます",
        )


def _to_response(task: Task, db: Session) -> TaskResponse:
    """TaskモデルをTaskResponseに変換する（assignee_name付き）"""
    assignee_name: Optional[str] = None

    if task.assignee_id is not None:
        user = db.query(User).filter(User.id == task.assignee_id).first()
        if user:
            assignee_name = user.name

    return TaskResponse(
        id=task.id,
        project_id=task.project_id,
        name=task.name,
        phase_name=task.phase_name,
        description=task.description,
        assignee_id=task.assignee_id,
        assignee_name=assignee_name,
        status=task.status,
        progress=task.progress,
        start_date=task.start_date,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def create_task(
    db: Session,
    project_id: int,
    task_data: TaskCreate,
    current_user: User,
) -> TaskResponse:
    """タスクを作成する"""
    project = _check_project_exists(
        db.query(Project).filter(Project.id == project_id).first()
    )
    _check_project_approved(project)
    check_project_access(project, current_user)

    if current_user.role == UserRole.TASK_MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="担当者はタスクを登録できません",
        )

    task = Task(
        project_id=project_id,
        name=task_data.name,
        phase_name=task_data.phase_name,
        description=task_data.description,
        assignee_id=task_data.assignee_id,
        status=task_data.status,
        progress=task_data.progress,
        start_date=task_data.start_date,
        due_date=task_data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return _to_response(task, db)


def get_tasks(
    db: Session,
    project_id: int,
    current_user: User,
) -> List[TaskResponse]:
    """案件に紐づくタスク一覧を取得する"""
    project = _check_project_exists(
        db.query(Project).filter(Project.id == project_id).first()
    )
    check_project_access(project, current_user)

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    return [_to_response(t, db) for t in tasks]


def update_task(
    db: Session,
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User,
) -> TaskResponse:
    """タスクを更新する"""
    project = _check_project_exists(
        db.query(Project).filter(Project.id == project_id).first()
    )
    _check_project_approved(project)
    check_project_access(project, current_user)

    task = (
        db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="タスクが見つかりません",
        )

    # DEPT_MANAGER / HQ_MANAGER はタスク更新不可（閲覧のみ）
    if current_user.role in [UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を行う権限がありません",
        )

    # TASK_MEMBERは、休暇・代理対応を考慮し、同一部門内のタスク更新を許可する。
    # ただし、他部門案件のタスク更新は不可。
    if current_user.role == UserRole.TASK_MEMBER:
        # 他部門は不可
        if project.department_id != current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この操作を行う権限がありません",
            )

        # 担当者はレビュー中・完了に変更不可（現在値から変更しようとした場合のみ制限）
        next_status = task_data.status
        if (
            next_status is not None
            and next_status != task.status
            and next_status in [
                TaskStatus.IN_REVIEW,
                TaskStatus.DONE,
            ]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="担当者は進行中まで変更可能です",
            )

        # 担当者は100%不可（現在値から変更しようとした場合のみ制限）
        next_progress = task_data.progress
        if (
            next_progress is not None
            and next_progress != task.progress
            and next_progress >= 100
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="担当者は進捗率100%に変更できません",
            )

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)

    return _to_response(task, db)


def delete_task(
    db: Session,
    project_id: int,
    task_id: int,
    current_user: User,
) -> None:
    """タスクを削除する"""
    project = _check_project_exists(
        db.query(Project).filter(Project.id == project_id).first()
    )
    _check_project_approved(project)
    check_project_access(project, current_user)

    if current_user.role == UserRole.TASK_MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="担当者はタスクを削除できません",
        )

    task = (
        db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="タスクが見つかりません",
        )

    db.delete(task)
    db.commit()


def get_department_tasks(
    db: Session,
    department_id: int,
    current_user: User,
) -> list[TaskResponse]:
    """部門内の全案件のタスクを取得する"""
    from app.services.project.permission_service import check_dept_access

    check_dept_access(department_id, current_user)

    tasks = (
        db.query(Task)
        .join(Project, Task.project_id == Project.id)
        .filter(Project.department_id == department_id)
        .filter(
            Project.status.in_(
                [
                    ProjectStatus.APPROVED,
                    ProjectStatus.IN_PROGRESS,
                    ProjectStatus.COMPLETED,
                ]
            )
        )
        .order_by(Task.due_date.asc())
        .all()
    )

    return [_to_response(t, db) for t in tasks]


def get_all_tasks(
    db: Session,
    current_user: User,
) -> list[TaskResponse]:
    """全案件のタスクを取得する（本部管理者専用）"""

    if current_user.role != UserRole.HQ_MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を行う権限がありません",
        )

    tasks = (
        db.query(Task)
        .join(Project, Task.project_id == Project.id)
        .filter(
            Project.status.in_(
                [
                    ProjectStatus.APPROVED,
                    ProjectStatus.IN_PROGRESS,
                    ProjectStatus.COMPLETED,
                ]
            )
        )
        .order_by(Task.due_date.asc())
        .all()
    )

    return [_to_response(t, db) for t in tasks]
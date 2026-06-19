from datetime import timezone, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.worklog import Worklog
from app.models.user import User

from app.schemas.budget import (
    WorklogCreate,
    WorklogUpdate,
    WorklogResponse,
)

from app.services.project.permission_service import (
    check_budget_permission,
    check_project_access,
)
from app.services.project.query_service import check_project_approved
from app.services.budget.budget_calc_service import update_actual_amount


def create_worklog(
    db: Session,
    project_id: int,
    worklog_data: WorklogCreate,
    current_user: User,
) -> WorklogResponse:
    """工数実績を登録する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    existing = (
        db.query(Worklog)
        .filter(
            Worklog.project_id == project_id,
            Worklog.work_month == worklog_data.work_month,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この月の工数実績は既に登録されています",
        )

    worklog = Worklog(
        project_id=project_id,
        work_month=worklog_data.work_month,
        actual_months=worklog_data.actual_months,
    )

    db.add(worklog)
    db.flush()

    update_actual_amount(db, project_id)

    db.commit()
    db.refresh(worklog)

    return WorklogResponse.model_validate(worklog)


def get_worklogs(db, project_id, current_user):
    project = check_project_approved(db, project_id)
    check_project_access(project, current_user)
    worklogs = (
        db.query(Worklog)
        .filter(Worklog.project_id == project_id)
        .order_by(Worklog.work_month)
        .all()
    )
    return [WorklogResponse.model_validate(w) for w in worklogs]


def update_worklog(
    db: Session,
    project_id: int,
    worklog_id: int,
    worklog_data: WorklogUpdate,
    current_user: User,
) -> WorklogResponse:
    """工数実績を更新する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    worklog = (
        db.query(Worklog)
        .filter(
            Worklog.id == worklog_id,
            Worklog.project_id == project_id,
        )
        .first()
    )

    if worklog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工数実績が見つかりません",
        )

    worklog.actual_months = worklog_data.actual_months
    worklog.updated_at = datetime.now(timezone.utc)

    db.flush()
    update_actual_amount(db, project_id)

    db.commit()
    db.refresh(worklog)

    return WorklogResponse.model_validate(worklog)


def delete_worklog(
    db: Session,
    project_id: int,
    worklog_id: int,
    current_user: User,
) -> None:
    """工数実績を削除する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    worklog = (
        db.query(Worklog)
        .filter(
            Worklog.id == worklog_id,
            Worklog.project_id == project_id,
        )
        .first()
    )

    if worklog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工数実績が見つかりません",
        )

    db.delete(worklog)
    db.flush()

    update_actual_amount(db, project_id)

    db.commit()

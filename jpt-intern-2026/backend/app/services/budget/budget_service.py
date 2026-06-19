from datetime import timezone, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project_budget import ProjectBudget
from app.models.user import User

from app.schemas.budget import (
    ProjectBudgetCreate,
    ProjectBudgetUpdate,
    ProjectBudgetResponse,
)

from app.services.project.permission_service import check_budget_permission
from app.services.project.query_service import check_project_approved
from app.services.project.permission_service import check_project_access


def create_budget(
    db: Session,
    project_id: int,
    budget_data: ProjectBudgetCreate,
    current_user: User,
) -> ProjectBudgetResponse:
    """予算を登録する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    existing = (
        db.query(ProjectBudget).filter(ProjectBudget.project_id == project_id).first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この案件の予算は既に登録されています",
        )

    budget = ProjectBudget(
        project_id=project_id,
        budget_amount=budget_data.budget_amount,
        unit_price=budget_data.unit_price,
        planned_months=budget_data.planned_months,
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return _to_budget_response(budget)


def get_budget(db, project_id, current_user):
    project = check_project_approved(db, project_id)

    check_project_access(project, current_user)

    budget = (
        db.query(ProjectBudget).filter(ProjectBudget.project_id == project_id).first()
    )

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="予算情報が見つかりません",
        )

    return _to_budget_response(budget)


def update_budget(
    db: Session,
    project_id: int,
    budget_data: ProjectBudgetUpdate,
    current_user: User,
) -> ProjectBudgetResponse:
    """予算情報を更新する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    budget = (
        db.query(ProjectBudget).filter(ProjectBudget.project_id == project_id).first()
    )

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="予算情報が見つかりません",
        )

    for key, value in budget_data.model_dump(exclude_unset=True).items():
        setattr(budget, key, value)

    budget.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(budget)

    return _to_budget_response(budget)


def _to_budget_response(budget: ProjectBudget) -> ProjectBudgetResponse:
    """ProjectBudgetをProjectBudgetResponseに変換する（consumption_rate付き）"""
    data = ProjectBudgetResponse.model_validate(budget)
    if budget.budget_amount > 0:
        data.consumption_rate = int(budget.actual_amount / budget.budget_amount * 100)
    return data

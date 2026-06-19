from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User

from app.schemas.budget import (
    ProjectBudgetCreate,
    ProjectBudgetUpdate,
    ProjectBudgetResponse,
    WorklogCreate,
    WorklogUpdate,
    WorklogResponse,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

import app.services.budget.budget_service as budget_service
import app.services.budget.worklog_service as worklog_service
import app.services.budget.expense_service as expense_service

from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/projects/{project_id}", tags=["予算管理"])


# ── ProjectBudget ────────────────────────────────────────


@router.post(
    "/budget",
    response_model=ProjectBudgetResponse,
    operation_id="create_budget",
)
def create_budget(
    project_id: int,
    budget_data: ProjectBudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """予算登録"""
    return budget_service.create_budget(
        db,
        project_id,
        budget_data,
        current_user,
    )


@router.get(
    "/budget",
    response_model=ProjectBudgetResponse,
    operation_id="get_budget",
)
def get_budget(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """予算取得"""
    return budget_service.get_budget(
        db,
        project_id,
        current_user,
    )


@router.put(
    "/budget",
    response_model=ProjectBudgetResponse,
    operation_id="update_budget",
)
def update_budget(
    project_id: int,
    budget_data: ProjectBudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """予算更新"""
    return budget_service.update_budget(
        db,
        project_id,
        budget_data,
        current_user,
    )


# ── Worklog ──────────────────────────────────────────────


@router.post(
    "/worklogs",
    response_model=WorklogResponse,
    operation_id="create_worklog",
)
def create_worklog(
    project_id: int,
    worklog_data: WorklogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """工数実績登録"""
    return worklog_service.create_worklog(
        db,
        project_id,
        worklog_data,
        current_user,
    )


@router.get(
    "/worklogs",
    response_model=list[WorklogResponse],
    operation_id="get_worklogs",
)
def get_worklogs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """工数実績一覧取得"""
    return worklog_service.get_worklogs(
        db,
        project_id,
        current_user,
    )


@router.put(
    "/worklogs/{worklog_id}",
    response_model=WorklogResponse,
    operation_id="update_worklog",
)
def update_worklog(
    project_id: int,
    worklog_id: int,
    worklog_data: WorklogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """工数実績更新"""
    return worklog_service.update_worklog(
        db,
        project_id,
        worklog_id,
        worklog_data,
        current_user,
    )


@router.delete(
    "/worklogs/{worklog_id}",
    status_code=204,
    operation_id="delete_worklog",
)
def delete_worklog(
    project_id: int,
    worklog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """工数実績削除"""
    worklog_service.delete_worklog(
        db,
        project_id,
        worklog_id,
        current_user,
    )


# ── Expense ──────────────────────────────────────────────


@router.post(
    "/expenses",
    response_model=ExpenseResponse,
    operation_id="create_expense",
)
def create_expense(
    project_id: int,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """直接経費登録"""
    return expense_service.create_expense(
        db,
        project_id,
        expense_data,
        current_user,
    )


@router.get(
    "/expenses",
    response_model=list[ExpenseResponse],
    operation_id="get_expenses",
)
def get_expenses(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """直接経費一覧取得"""
    return expense_service.get_expenses(
        db,
        project_id,
        current_user,
    )


@router.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse,
    operation_id="update_expense",
)
def update_expense(
    project_id: int,
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """直接経費更新"""
    return expense_service.update_expense(
        db,
        project_id,
        expense_id,
        expense_data,
        current_user,
    )


@router.delete(
    "/expenses/{expense_id}",
    status_code=204,
    operation_id="delete_expense",
)
def delete_expense(
    project_id: int,
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """直接経費削除"""
    expense_service.delete_expense(
        db,
        project_id,
        expense_id,
        current_user,
    )

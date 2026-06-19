from datetime import timezone, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.expense import Expense
from app.models.user import User

from app.schemas.budget import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

from app.services.project.permission_service import (
    check_budget_permission,
    check_project_access,
)
from app.services.project.query_service import check_project_approved
from app.services.budget.budget_calc_service import update_actual_amount


def create_expense(
    db: Session,
    project_id: int,
    expense_data: ExpenseCreate,
    current_user: User,
) -> ExpenseResponse:
    """直接経費を登録する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    expense = Expense(
        project_id=project_id,
        expense_type=expense_data.expense_type,
        amount=expense_data.amount,
        description=expense_data.description,
        expense_date=expense_data.expense_date,
    )

    db.add(expense)
    db.flush()

    update_actual_amount(db, project_id)

    db.commit()
    db.refresh(expense)

    return ExpenseResponse.model_validate(expense)


def get_expenses(db, project_id, current_user):
    project = check_project_approved(db, project_id)
    check_project_access(project, current_user)
    expenses = (
        db.query(Expense)
        .filter(Expense.project_id == project_id)
        .order_by(Expense.expense_date)
        .all()
    )
    return [ExpenseResponse.model_validate(e) for e in expenses]


def update_expense(
    db: Session,
    project_id: int,
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: User,
) -> ExpenseResponse:
    """直接経費を更新する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.project_id == project_id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="経費が見つかりません",
        )

    for key, value in expense_data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)

    expense.updated_at = datetime.now(timezone.utc)

    db.flush()
    update_actual_amount(db, project_id)

    db.commit()
    db.refresh(expense)

    return ExpenseResponse.model_validate(expense)


def delete_expense(
    db: Session,
    project_id: int,
    expense_id: int,
    current_user: User,
) -> None:
    """直接経費を削除する"""
    project = check_project_approved(db, project_id)
    check_budget_permission(project, current_user)

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.project_id == project_id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="経費が見つかりません",
        )

    db.delete(expense)
    db.flush()

    update_actual_amount(db, project_id)

    db.commit()

from datetime import timezone, datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project_budget import ProjectBudget
from app.models.worklog import Worklog
from app.models.expense import Expense


def update_actual_amount(db: Session, project_id: int) -> None:
    """工数実績と直接経費から実績額をSQLで再計算してproject_budgetsを更新する"""
    budget = (
        db.query(ProjectBudget).filter(ProjectBudget.project_id == project_id).first()
    )

    if budget is None:
        return

    # 工数実績の合計をSQLで計算
    total_months = (
        db.query(func.coalesce(func.sum(Worklog.actual_months), 0))
        .filter(Worklog.project_id == project_id)
        .scalar()
    )

    worklog_amount = int(total_months * budget.unit_price) if budget.unit_price else 0

    # 直接経費の合計をSQLで計算
    expense_amount = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.project_id == project_id)
        .scalar()
    )

    budget.actual_amount = worklog_amount + int(expense_amount)
    budget.updated_at = datetime.now(timezone.utc)

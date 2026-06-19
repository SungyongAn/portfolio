from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.project import Project
from app.models.project_budget import ProjectBudget
from app.models.user import User
from app.schemas.project import BudgetSummaryResponse
from app.services.project.query_service import apply_project_filters


def get_budget_summary(
    db: Session,
    current_user: User,
    status: list[str] | None = None,
    department_id=None,
    budget_min=None,
    budget_max=None,
    keyword: str | None = None,
) -> BudgetSummaryResponse:

    query = apply_project_filters(
        db.query(Project),
        current_user,
        status,
        department_id,
        budget_min,
        budget_max,
        keyword,
    )

    # サブクエリ化してProjectBudgetとJOIN
    subquery = query.subquery()

    result = (
        db.query(
            func.count(subquery.c.id).label("total_projects"),
            func.coalesce(func.sum(subquery.c.budget_amount), 0).label("total_budget"),
            func.coalesce(func.sum(ProjectBudget.actual_amount), 0).label(
                "total_actual"
            ),
            # 加重平均：SUM(actual) / SUM(budget) * 100（ゼロ除算対策）
            func.coalesce(
                case(
                    (
                        func.sum(subquery.c.budget_amount) > 0,
                        func.sum(ProjectBudget.actual_amount)
                        * 100
                        / func.sum(subquery.c.budget_amount),
                    ),
                    else_=0,
                ),
                0,
            ).label("avg_consumption_rate"),
        )
        .outerjoin(ProjectBudget, ProjectBudget.project_id == subquery.c.id)
        .one()
    )

    return BudgetSummaryResponse(
        total_projects=result.total_projects or 0,
        total_budget=int(result.total_budget or 0),
        total_actual=int(result.total_actual or 0),
        avg_consumption_rate=int(result.avg_consumption_rate or 0),
    )

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User, UserRole

from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ApprovalRequest,
    ProjectResponse,
    ProjectListResponse,
    BudgetSummaryResponse,
)

from app.services.project import project_service
import app.services.budget.budget_summary_service as budget_summary_service
import app.services.project.approval_service as approval_service

from app.dependencies.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/projects", tags=["案件"])


@router.post("", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.APPLICANT])),
):
    """案件申請（申請者のみ）"""
    return project_service.create_project(
        db,
        project_data,
        current_user,
    )


@router.get("", response_model=ProjectListResponse)
def get_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: list[str] | None = Query(None),
    keyword: str | None = Query(None),
    department_id: int | None = None,
    budget_min: int | None = None,
    budget_max: int | None = None,
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    alert_level: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """案件一覧取得（ロール別）"""
    return project_service.get_projects(
        db=db,
        current_user=current_user,
        page=page,
        limit=limit,
        status=status,
        keyword=keyword,
        department_id=department_id,
        budget_min=budget_min,
        budget_max=budget_max,
        sort_by=sort_by,
        sort_order=sort_order,
        alert_level=alert_level,
    )


@router.get("/budget-summary", response_model=BudgetSummaryResponse)
def get_budget_summary(
    status: list[str] | None = Query(None),
    keyword: str | None = Query(None),
    department_id: int | None = None,
    budget_min: int | None = None,
    budget_max: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER])
    ),
):
    """予算サマリー取得（部門管理者・本部管理者のみ）"""
    return budget_summary_service.get_budget_summary(
        db=db,
        current_user=current_user,
        status=status,
        keyword=keyword,
        department_id=department_id,
        budget_min=budget_min,
        budget_max=budget_max,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """案件詳細取得"""
    return project_service.get_project_by_id(
        db,
        project_id,
        current_user,
    )


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.APPLICANT])),
):
    """案件更新（申請者のみ・承認待ち状態のみ）"""
    return project_service.update_project(
        db,
        project_id,
        project_data,
        current_user,
    )


@router.post("/{project_id}/approve", response_model=ProjectResponse)
def approve_project(
    project_id: int,
    approval: ApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER])
    ),
):
    """案件承認・却下（部門管理者・本部管理者のみ）"""
    return approval_service.approve_project(
        db,
        project_id,
        approval,
        current_user,
    )


@router.patch("/{project_id}/start", response_model=ProjectResponse)
def start_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                UserRole.APPLICANT,
                UserRole.DEPT_MANAGER,
                UserRole.HQ_MANAGER,
            ]
        )
    ),
):
    """案件着手"""
    return project_service.start_project(
        db,
        project_id,
        current_user,
    )


@router.patch("/{project_id}/complete", response_model=ProjectResponse)
def complete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER])
    ),
):
    """案件完了"""
    return project_service.complete_project(
        db,
        project_id,
        current_user,
    )

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project, ProjectStatus
from app.models.user import UserRole


# 共通取得関数
def get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "案件が見つかりません")
    return project


def apply_project_filters(
    query,
    current_user,
    status=None,
    department_id=None,
    budget_min=None,
    budget_max=None,
    keyword=None,
):
    if current_user.role == UserRole.HQ_MANAGER:
        pass
    elif current_user.role in [UserRole.DEPT_MANAGER, UserRole.TASK_MEMBER]:
        query = query.filter(Project.department_id == current_user.department_id)
    else:
        query = query.filter(Project.applicant_id == current_user.id)

    if status:
        query = query.filter(Project.status.in_(status))

    if keyword:
        query = query.filter(Project.name.contains(keyword))

    if department_id:
        query = query.filter(Project.department_id == department_id)

    if budget_min is not None:
        query = query.filter(Project.budget_amount >= budget_min)

    if budget_max is not None:
        query = query.filter(Project.budget_amount <= budget_max)

    return query


def check_project_approved(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="案件が見つかりません",
        )

    if project.status not in [
        ProjectStatus.APPROVED,
        ProjectStatus.IN_PROGRESS,
        ProjectStatus.COMPLETED,
    ]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="予算情報が見つかりません",
        )

    return project

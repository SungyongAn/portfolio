from datetime import timezone, datetime
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectStatus
from app.models.user import User, UserRole
from app.models.notification import Notification
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)
from app.services.notification_service import notify_applicant, push_notification
from app.services.project.query_service import (
    get_project_or_404,
    apply_project_filters,
)
from app.services.response_service import to_response
from app.services.project.permission_service import (
    check_project_access,
    check_project_editable,
    check_start_permission,
    check_complete_permission,
)


def create_project(
    db: Session, project_data: ProjectCreate, current_user: User
) -> ProjectResponse:
    """案件を申請する"""
    project = Project(
        name=project_data.name,
        description=project_data.description,
        status=ProjectStatus.PENDING_DEPT,
        applicant_id=current_user.id,
        department_id=current_user.department_id,
        budget_amount=project_data.budget_amount,
        planned_months=project_data.planned_months,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        development_method=project_data.development_method,
    )
    db.add(project)
    db.flush()

    dept_managers = (
        db.query(User)
        .filter(
            User.role == UserRole.DEPT_MANAGER,
            User.department_id == current_user.department_id,
        )
        .all()
    )

    for manager in dept_managers:
        notification = Notification(
            user_id=manager.id,
            project_id=project.id,
            title="新規案件申請",
            message=f"「{project.name}」の承認依頼が届いています",
        )
        db.add(notification)
        push_notification(
            manager.id,
            "新規案件申請",
            f"「{project.name}」の承認依頼が届いています",
            project.id,
        )

    db.commit()
    db.refresh(project)
    return to_response(db, project)


def start_project(db: Session, project_id: int, current_user: User):
    project = get_project_or_404(db, project_id)

    check_start_permission(project, current_user)

    project.status = ProjectStatus.IN_PROGRESS
    project.updated_at = datetime.now(timezone.utc)

    notify_applicant(
        db, project, "案件が開始されました", f"「{project.name}」が着手されました"
    )

    db.commit()
    db.refresh(project)

    return to_response(db, project)


def complete_project(db: Session, project_id: int, current_user: User):
    project = get_project_or_404(db, project_id)

    check_complete_permission(project, current_user)

    project.status = ProjectStatus.COMPLETED
    project.updated_at = datetime.now(timezone.utc)

    notify_applicant(
        db, project, "案件が完了しました", f"「{project.name}」が完了しました"
    )

    db.commit()
    db.refresh(project)

    return to_response(db, project)


def _apply_project_sort(query, sort_by: str | None, sort_order: str):
    """案件一覧のSQLソートを適用する"""

    if sort_by == "budget_amount":
        if sort_order == "asc":
            return query.order_by(Project.budget_amount.asc())

        return query.order_by(Project.budget_amount.desc())

    # デフォルトは従来どおり新しい案件順
    return query.order_by(Project.created_at.desc())


def get_projects(
    db: Session,
    current_user: User,
    page: int = 1,
    limit: int = 10,
    status: list[str] | None = None,
    keyword: str | None = None,
    department_id: int | None = None,
    budget_min: int | None = None,
    budget_max: int | None = None,
    sort_by: str | None = None,
    sort_order: str = "desc",
    alert_level: str | None = None,
) -> ProjectListResponse:

    page = max(page, 1)
    limit = max(min(limit, 100), 10)

    query = apply_project_filters(
        db.query(Project),
        current_user,
        status,
        department_id,
        budget_min,
        budget_max,
        keyword,
    )

    query = _apply_project_sort(query, sort_by, sort_order)

    project_responses = [to_response(db, p) for p in query.all()]

    if alert_level:
        project_responses = [
            project
            for project in project_responses
            if project.alert_level == alert_level
        ]

    total = len(project_responses)

    paged_projects = project_responses[(page - 1) * limit : page * limit]

    return ProjectListResponse(
        total=total,
        page=page,
        limit=limit,
        items=paged_projects,
    )


def get_project_by_id(
    db: Session, project_id: int, current_user: User
) -> ProjectResponse:
    """案件詳細を取得する"""
    project = get_project_or_404(db, project_id)

    check_project_access(project, current_user)
    return to_response(db, project)


def update_project(
    db: Session, project_id: int, project_data: ProjectUpdate, current_user: User
) -> ProjectResponse:
    """案件情報を更新する（申請者のみ・PENDING_DEPT状態のみ）"""
    project = get_project_or_404(db, project_id)

    check_project_editable(project, current_user)

    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    project.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(project)
    return to_response(db, project)

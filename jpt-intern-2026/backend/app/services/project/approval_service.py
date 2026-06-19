from datetime import timezone, datetime
from sqlalchemy.orm import Session

from app.models.project import ProjectStatus
from app.models.user import User, UserRole
from app.models.notification import Notification

from app.services.response_service import to_response
from app.services.project.query_service import get_project_or_404
from app.services.notification_service import notify_applicant, push_notification
from app.services.project.permission_service import check_approval_permission

from app.schemas.project import (
    ApprovalRequest,
    ProjectResponse,
)


def approve_project(
    db: Session, project_id: int, approval: ApprovalRequest, current_user: User
) -> ProjectResponse:
    """案件を承認・却下する"""
    project = get_project_or_404(db, project_id)

    check_approval_permission(project, current_user)

    if current_user.role == UserRole.DEPT_MANAGER:
        if approval.reject_reason:
            project.status = ProjectStatus.REJECTED
            project.reject_reason = approval.reject_reason

            notify_applicant(
                db,
                project,
                "案件が却下されました",
                f"「{project.name}」が却下されました。理由：{approval.reject_reason}",
            )
        else:
            project.status = ProjectStatus.PENDING_HQ

            # 本部管理者への通知
            hq_managers = db.query(User).filter(User.role == UserRole.HQ_MANAGER).all()

            for manager in hq_managers:
                db.add(
                    Notification(
                        user_id=manager.id,
                        project_id=project.id,
                        title="案件承認依頼",
                        message=f"「{project.name}」の最終承認依頼が届いています",
                    )
                )

                push_notification(
                    manager.id,
                    "案件承認依頼",
                    f"「{project.name}」の最終承認依頼が届いています",
                    project.id,
                )

    elif current_user.role == UserRole.HQ_MANAGER:
        if approval.reject_reason:
            project.status = ProjectStatus.REJECTED
            project.reject_reason = approval.reject_reason

            notify_applicant(
                db,
                project,
                "案件が却下されました",
                f"「{project.name}」が却下されました。理由：{approval.reject_reason}",
            )
        else:
            project.status = ProjectStatus.APPROVED

            notify_applicant(
                db,
                project,
                "案件が承認されました",
                f"「{project.name}」が承認されました",
            )

    project.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(project)

    return to_response(db, project)

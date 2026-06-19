from sqlalchemy.orm import Session, joinedload

from app.models.notification import Notification
from app.models.project import Project
from app.models.task import Task
from app.models.user import User, UserRole
from app.services.project.permission_service import check_dept_access


def get_target_projects(db: Session, current_user: User) -> list[Project]:
    """ユーザー権限に応じてダッシュボード対象案件を取得"""

    query = db.query(Project).options(
        joinedload(Project.department),
        joinedload(Project.applicant),
        joinedload(Project.budget),
        joinedload(Project.tasks).joinedload(Task.assignee),
    )

    if current_user.role == UserRole.HQ_MANAGER:
        return query.all()

    if current_user.role in {UserRole.DEPT_MANAGER, UserRole.TASK_MEMBER}:
        check_dept_access(current_user.department_id, current_user)
        return query.filter(Project.department_id == current_user.department_id).all()

    # APPLICANT：自身が申請した案件のみ
    return query.filter(Project.applicant_id == current_user.id).all()


def get_target_tasks(db: Session, current_user: User) -> list[Task]:
    """ユーザー権限に応じてダッシュボード対象タスクを取得"""

    query = db.query(Task).options(
        joinedload(Task.project).joinedload(Project.department),
        joinedload(Task.assignee),
    )

    if current_user.role == UserRole.HQ_MANAGER:
        return query.all()

    if current_user.role == UserRole.DEPT_MANAGER:
        return (
            query.join(Project)
            .filter(Project.department_id == current_user.department_id)
            .all()
        )

    if current_user.role == UserRole.TASK_MEMBER:
        return query.filter(Task.assignee_id == current_user.id).all()

    # APPLICANT：自身の案件に紐づくタスクのみ
    return query.join(Project).filter(Project.applicant_id == current_user.id).all()


def get_unread_notification_count(db: Session, current_user: User) -> int:
    """ログインユーザーの未読通知数を取得"""

    return (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False),
        )
        .count()
    )

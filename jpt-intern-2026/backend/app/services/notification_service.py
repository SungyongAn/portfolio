from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationListResponse
from app.websocket_manager import manager as ws_manager
import asyncio
from app.models.project import Project


def get_notifications(
    db: Session,
    current_user: User,
    page: int = 1,
    limit: int = 10,
) -> NotificationListResponse:
    page = max(page, 1)
    limit = max(min(limit, 100), 10)

    query = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    )

    total = query.count()
    notifications = query.offset((page - 1) * limit).limit(limit).all()

    return NotificationListResponse(
        total=total,
        page=page,
        limit=limit,
        items=[NotificationResponse.model_validate(n) for n in notifications],
    )


def mark_as_read(
    db: Session, notification_id: int, current_user: User
) -> NotificationResponse:
    """通知を既読にする"""
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="通知が見つかりません"
        )

    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return NotificationResponse.model_validate(notification)


def mark_all_as_read(db: Session, current_user: User) -> None:
    """全通知を既読にする"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read.is_(False),
    ).update({"is_read": True})
    db.commit()


def notify_applicant(db: Session, project: Project, title: str, message: str) -> None:
    """申請者への通知を作成する"""
    db.add(
        Notification(
            user_id=project.applicant_id,
            project_id=project.id,
            title=title,
            message=message,
        )
    )
    push_notification(project.applicant_id, title, message, project.id)


def push_notification(user_id: int, title: str, message: str, project_id: int) -> None:
    """WebSocket経由でリアルタイム通知をプッシュする"""
    payload = {
        "type": "notification",
        "title": title,
        "message": message,
        "project_id": project_id,
    }
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(ws_manager.send_to_user(user_id, payload))
        else:
            loop.run_until_complete(ws_manager.send_to_user(user_id, payload))
    except Exception:
        pass

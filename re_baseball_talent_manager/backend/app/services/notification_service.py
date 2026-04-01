from sqlalchemy.orm import Session

from app.routers.notifications import manager


async def notify_user(user_id: int, message: dict):
    await manager.send_to_user(user_id, message)


async def notify_role(role: str, message: dict, db: Session):
    await manager.send_to_role(role, message, db)
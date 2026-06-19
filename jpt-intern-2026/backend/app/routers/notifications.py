from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from app.db import get_db, SessionLocal
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationListResponse
import app.services.notification_service as notification_service
from app.dependencies.auth import get_current_user
from app.utils.security import decode_token
from app.websocket_manager import manager

router = APIRouter(prefix="/api/notifications", tags=["通知"])


@router.websocket("/ws")
async def websocket_notifications(
    websocket: WebSocket,
    token: str = Query(...),
):
    """
    WebSocket通知エンドポイント。
    接続時にクエリパラメータ token でJWTを検証する。
    例: ws://host/api/notifications/ws?token=<access_token>
    """
    # トークン検証
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        await websocket.close(code=4001)
        return

    user_id = payload.get("sub")
    if user_id is None:
        await websocket.close(code=4001)
        return

    user_id = int(user_id)

    # DB上にユーザーが存在するか確認
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            await websocket.close(code=4001)
            return
    finally:
        db.close()

    await manager.connect(user_id, websocket)
    try:
        while True:
            # クライアントからのメッセージは受け取るだけ（ping/pong用途）
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)


@router.get("", response_model=NotificationListResponse)
def get_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """通知一覧取得"""
    return notification_service.get_notifications(db, current_user, page, limit)


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """通知を既読にする"""
    return notification_service.mark_as_read(db, notification_id, current_user)


@router.put("/read-all", status_code=204)
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """全通知を既読にする"""
    notification_service.mark_all_as_read(db, current_user)

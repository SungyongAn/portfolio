from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.utils.security import decode_token

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, message: dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

    async def send_to_role(self, role: str, message: dict, db: Session):
        users = db.query(User).filter(User.role == role).all()

        for user in users:
            websocket = self.active_connections.get(user.id)
            if websocket:
                await websocket.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    # ① クエリパラメータから token 取得
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    # ② トークン検証
    try:
        payload = decode_token(token)
    except Exception:
        await websocket.close(code=1008)
        return

    # ③ user_id取得
    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=1008)
        return

    # 型変換（念のため）
    user_id = int(user_id)

    # ④ DBセッション取得（Depends使えないため手動）
    db: Session = next(get_db())

    try:
        # ⑤ ユーザー存在チェック
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            await websocket.close(code=1008)
            return

        # ⑥ 接続
        await manager.connect(user_id, websocket)

        while True:
            # 接続維持（受信は特に使わない）
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(user_id)

    finally:
        db.close()

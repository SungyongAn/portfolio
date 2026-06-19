from fastapi import WebSocket
from typing import Dict, List
import json


class ConnectionManager:
    """WebSocket接続を管理するクラス。ユーザーIDごとに複数接続を保持する。"""

    def __init__(self):
        # user_id -> list of WebSocket
        self._connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        if user_id not in self._connections:
            self._connections[user_id] = []
        self._connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        if user_id in self._connections:
            self._connections[user_id] = [
                ws for ws in self._connections[user_id] if ws is not websocket
            ]
            if not self._connections[user_id]:
                del self._connections[user_id]

    async def send_to_user(self, user_id: int, payload: dict) -> None:
        """指定ユーザーの全接続にJSONを送信する。切断済みの接続は自動除去する。"""
        if user_id not in self._connections:
            return

        message = json.dumps(payload, ensure_ascii=False, default=str)
        dead: List[WebSocket] = []

        for ws in self._connections[user_id]:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)

        for ws in dead:
            self.disconnect(user_id, ws)


# アプリ全体で共有するシングルトンインスタンス
manager = ConnectionManager()

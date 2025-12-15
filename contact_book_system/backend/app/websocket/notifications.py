from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.db.db import SessionLocal
from sqlalchemy.orm import Session
from app.models.accounts_model import Account
from app.models.chat_model import ChatRoom, ChatParticipant, ChatMessage
from datetime import datetime
import json
import asyncio
import logging
from threading import Thread


router = APIRouter()
logger = logging.getLogger(__name__)


# 接続管理
class ConnectionManager:
    def __init__(self):
        # room_id -> {user_id: websocket}
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, room_id: int, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket
        logger.info(f"User {user_id} connected to room {room_id} ({len(self.active_connections[room_id])} users)")

    def disconnect(self, room_id: int, user_id: int):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            logger.info(f"User {user_id} disconnected from room {room_id} ({len(self.active_connections[room_id])} users)")
            if len(self.active_connections[room_id]) == 0:
                del self.active_connections[room_id]
                logger.info(f"Removed empty room {room_id}")

    async def broadcast_to_room(self, room_id: int, message: dict, exclude_user_id: int = None):
        if room_id not in self.active_connections:
            logger.warning(f"No active connections in room {room_id}")
            return
        disconnected = []
        for user_id, ws in self.active_connections[room_id].items():
            if exclude_user_id and user_id == exclude_user_id:
                continue
            try:
                await ws.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Failed to send to user {user_id}: {e}")
                disconnected.append(user_id)
        for user_id in disconnected:
            self.disconnect(room_id, user_id)

    async def send_to_user(self, room_id: int, user_id: int, message: dict):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            ws = self.active_connections[room_id][user_id]
            try:
                await ws.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Failed to send to user {user_id}: {e}")
                self.disconnect(room_id, user_id)

    def get_online_users(self, room_id: int) -> list:
        if room_id in self.active_connections:
            return list(self.active_connections[room_id].keys())
        return []


manager = ConnectionManager()
active_nurses: dict[str, WebSocket] = {}


# Chat WebSocket
@router.websocket("/ws/chat/{room_id}/{user_id}")
async def chat_websocket(websocket: WebSocket, room_id: int, user_id: int):
    db = SessionLocal()
    try:
        # --- 認証・参加権限チェック ---
        user = db.query(Account).filter(Account.id == user_id).first()
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        participant = db.query(ChatParticipant).filter(
            ChatParticipant.room_id == room_id,
            ChatParticipant.user_id == user_id
        ).first()
        if not user or not room or not participant:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            logger.warning(f"Rejected WS connection: user {user_id}, room {room_id}")
            return

        # WebSocket接続確立
        await manager.connect(room_id, user_id, websocket)

        # 接続中のユーザー一覧を送信（自分用）
        online_user_ids = manager.get_online_users(room_id)
        await manager.send_to_user(room_id, user_id, {
            "type": "online_users",
            "user_ids": online_user_ids
        })

        # 他の参加者に参加通知を送信
        await manager.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "user_name": user.name,
            "timestamp": datetime.now().isoformat()
        }, exclude_user_id=user_id)

        # --- メッセージ受信ループ ---
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            msg_type = msg.get("type", "message")

            if msg_type == "message":
                content = msg.get("content", "").strip()
                if not content:
                    continue
                chat_msg = ChatMessage(
                    room_id=room_id,
                    sender_id=user_id,
                    message=content,
                    sent_at=datetime.now()
                )
                db.add(chat_msg)
                db.commit()
                db.refresh(chat_msg)

                await manager.broadcast_to_room(
                    room_id,
                    {
                        "type": "message",
                        "message_id": chat_msg.id,
                        "sender_id": user_id,
                        "sender_name": user.name,
                        "message": content,
                        "sent_at": chat_msg.sent_at.isoformat()
                    }
                )
                logger.info(f"Message {chat_msg.id} in room {room_id} by user {user_id}")

            elif msg_type == "typing":
                await manager.broadcast_to_room(
                    room_id,
                    {
                        "type": "typing",
                        "user_id": user_id,
                        "user_name": user.name,
                        "is_typing": msg.get("is_typing", False)
                    },
                    exclude_user_id=user_id
                )

            elif msg_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

            # ✅ ユーザー退出通知の処理を追加
            elif msg_type == "user_leaving":
                logger.info(f"User {user_id} is leaving room {room_id}")
                # ループを抜けて正常終了処理へ
                break

    except WebSocketDisconnect:
        logger.info(f"User {user_id} disconnected from room {room_id}")
    except Exception as e:
        logger.error(f"WebSocket error room {room_id}, user {user_id}: {e}")
    finally:
        # クリーンアップ
        manager.disconnect(room_id, user_id)
        await manager.broadcast_to_room(
            room_id,
            {
                "type": "user_left",
                "user_id": user_id,
                "user_name": user.name,
                "timestamp": datetime.now().isoformat()
            }
        )
        db.close()


# 養護教諭 WebSocket
@router.websocket("/ws/nurse/{nurse_id}")
async def nurse_ws(websocket: WebSocket, nurse_id: str):
    await websocket.accept()
    active_nurses[nurse_id] = websocket
    logger.info(f"✅ Nurse {nurse_id} connected")
    
    db = SessionLocal()
    try:
        while True:
            try:
                # メッセージ受信（タイムアウト付き）
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60)
                msg = json.loads(data)
                msg_type = msg.get("type")
                
                # ✅ 看護師の切断通知を処理
                if msg_type == "nurse_disconnect":
                    logger.info(f"Nurse {nurse_id} requested disconnect")
                    break
                    
            except asyncio.TimeoutError:
                # 1分ごとにpingで接続確認
                try:
                    await websocket.send_text(json.dumps({"type": "ping"}))
                except Exception:
                    logger.warning(f"Ping failed for nurse {nurse_id}")
                    break

    except WebSocketDisconnect:
        logger.info(f"Nurse {nurse_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for nurse {nurse_id}: {e}")
    finally:
        active_nurses.pop(nurse_id, None)
        logger.info(f"🔌 Nurse {nurse_id} removed from active connections")
        db.close()


# 体調不良通知（養護教諭向け）
async def notify_critical_entry_async(entry: dict):
    """体調不良の生徒情報を養護教諭に通知"""
    # 体調もメンタルも3以上（問題なし）の場合は通知しない
    if entry.get("physical_condition", 3) > 2 and entry.get("mental_state", 3) > 2:
        logger.debug("Entry does not meet critical criteria, skipping notification")
        return
    
    if not entry or not entry.get("student_name"):
        logger.warning("空または不正なエントリのため通知スキップ")
        return  
    
    # 接続中の養護教諭のリスト化
    disconnected_nurses = []
    for nurse_id, ws in list(active_nurses.items()):
        try:
            await ws.send_text(json.dumps(entry, ensure_ascii=False))
            logger.info(f"📨 Notification sent to nurse {nurse_id} for student {entry.get('student_name')}")
        except Exception as e:
            logger.error(f"Failed to send notification to nurse {nurse_id}: {e}")
            disconnected_nurses.append(nurse_id)
    
    # 切断されたWebSocketを削除
    for nurse_id in disconnected_nurses:
        active_nurses.pop(nurse_id, None)
        logger.info(f"Removed disconnected nurse: {nurse_id}")


def notify_critical_entry(entry: dict, db: Session):
    """同期関数から非同期通知を呼び出す（dbは互換性のため残す）"""
    # WebSocketが接続されていない場合はスキップ
    if not active_nurses:
        logger.debug("No active nurses connected, skipping notification")
        return
    
    try:
        # 新しいスレッドでイベントループを作成して実行
        def run_in_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(notify_critical_entry_async(entry))
                finally:
                    loop.close()
            except Exception as e:
                logger.error(f"Error in notification thread: {e}")
        
        thread = Thread(target=run_in_thread, daemon=True)
        thread.start()
        logger.debug(f"Notification thread started for entry: {entry.get('renrakucho_id')}")
        
    except Exception as e:
        logger.error(f"Failed to create notification thread: {e}")

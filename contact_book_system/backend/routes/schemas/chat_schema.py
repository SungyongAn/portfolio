from pydantic import BaseModel, Field
from datetime import datetime


# ============================================
# チャットルーム関連
# ============================================

class ChatRoomCreate(BaseModel):
    """ルーム作成リクエスト"""
    name: str
    description: str | None = None
    participant_ids: list[int]


class ChatRoomUpdate(BaseModel):
    """ルーム更新リクエスト"""
    name: str | None = None
    description: str | None = None


class ParticipantInfo(BaseModel):
    """参加者情報"""
    user_id: int
    name: str
    role: str
    joined_at: datetime


class ChatRoomResponse(BaseModel):
    """ルーム情報レスポンス"""
    id: int
    name: str
    description: str | None = None
    creator_id: int
    creator_name: str
    participant_count: int
    last_message: str | None = None
    last_message_at: datetime | None = None
    unread_count: int
    created_at: datetime


class ChatRoomDetail(BaseModel):
    """ルーム詳細レスポンス"""
    id: int
    name: str
    description: str | None = None
    creator_id: int
    creator_name: str
    participants: list[ParticipantInfo]
    created_at: datetime


# ============================================
# メッセージ関連
# ============================================

class MessageCreate(BaseModel):
    """メッセージ送信リクエスト"""
    message: str


class MessageResponse(BaseModel):
    """メッセージレスポンス"""
    id: int
    room_id: int
    sender_id: int
    sender_name: str
    sender_role: str
    message: str
    sent_at: datetime
    is_read: bool = False
    read_by: list[str] = []


# 参加者管理
class AddParticipantsRequest(BaseModel):
    """参加者追加リクエスト"""
    user_ids: list[int]


class RemoveParticipantRequest(BaseModel):
    """参加者削除リクエスト"""
    user_id: int

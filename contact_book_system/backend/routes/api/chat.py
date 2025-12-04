from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from routes.db.db import get_db
from routes.models.accounts_model import Account, RoleEnum
from routes.services.auth import get_current_user
from routes.services.chat_service import ChatService
from routes.schemas.chat_schema import (
    ChatRoomCreate,
    ChatRoomUpdate,
    ChatRoomResponse,
    ChatRoomDetail,
    MessageCreate,
    MessageResponse,
    AddParticipantsRequest,
    RemoveParticipantRequest
)

router = APIRouter()


# 報連相部屋入室時に教師権限の確認
def require_teacher(current_user: Account = Depends(get_current_user)):
    if current_user.role not in [RoleEnum.teacher, RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can perform this action"
        )
    return current_user


# チャットルームの作成
@router.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(
    room_data: ChatRoomCreate,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_teacher)
):
    try:
        room = ChatService.create_room(db, room_data, current_user.id)
        
        return {
            "success": True,
            "message": "Chat room created successfully",
            "room_id": room.id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 参加しているチャットルーム情報の取得
@router.get("/rooms", response_model=list[ChatRoomResponse])
def get_rooms(
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    try:
        rooms = ChatService.get_user_rooms(db, current_user.id)
        return rooms
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ルーム一覧の取得に失敗しました"
        )


# 参加しているチャットルームの詳細取得
@router.get("/rooms/{room_id}", response_model=ChatRoomDetail)
def get_room_detail(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    try:
        room = ChatService.get_room_detail(db, room_id, current_user.id)
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found or you are not a participant"
            )
        
        return room
        
    except HTTPException as he:
        print(f"HTTPException caught: {he.status_code} - {he.detail}")
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.put("/rooms/{room_id}")
def update_room(
    room_id: int,
    room_data: ChatRoomUpdate,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_teacher)
):
    """ルーム情報を更新（作成者のみ）"""
    
    try:
        success = ChatService.update_room(db, room_id, current_user.id, room_data)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the creator can update the room"
            )
        
        return {
            "success": True,
            "message": "Room updated successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# チャットルームの削除(作成者のみの機能)
@router.delete("/rooms/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_teacher)
):
    success = ChatService.delete_room(db, room_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator can delete the room"
        )
    
    return {
        "success": True,
        "message": "Room deleted successfully"
    }


# 参加者の追加
@router.post("/rooms/{room_id}/participants")
def add_participants(
    room_id: int,
    request: AddParticipantsRequest,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_teacher)
):
    print("yes")
    try:
        success = ChatService.add_participants(
            db, room_id, current_user.id, request.user_ids
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the creator can add participants"
            )
        
        return {
            "success": True,
            "message": f"{len(request.user_ids)}人の参加者を追加しました"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/rooms/{room_id}/participants")
def remove_participant(
    room_id: int,
    request: RemoveParticipantRequest,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_teacher)
):
    """参加者を削除（作成者のみ）"""
    try:
        success = ChatService.remove_participant(
            db, room_id, current_user.id, request.user_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot remove participant"
            )
        
        return {
            "success": True,
            "message": "参加者を削除しました"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# メッセージ
@router.post("/rooms/{room_id}/messages")
def send_message(
    room_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    """メッセージを送信（参加者のみ）"""
    try:
        message = ChatService.send_message(
            db, room_id, current_user.id, message_data.message
        )
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a participant of this room"
            )
        
        return {
            "success": True,
            "message_id": message.id,
            "sent_at": message.sent_at
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="メッセージの送信に失敗しました"
        )


@router.get("/rooms/{room_id}/messages", response_model=list[MessageResponse])
def get_messages(
    room_id: int,
    limit: int = 50,
    before: int | None = None,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    """メッセージ一覧を取得（参加者のみ）"""
    try:
        messages = ChatService.get_messages(
            db, room_id, current_user.id, limit, before
        )
        return messages
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="メッセージの取得に失敗しました"
        )


@router.post("/rooms/{room_id}/read")
def mark_as_read(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user)
):
    """未読メッセージを既読にする"""
    try:
        print("届いてるよ")
        count = ChatService.mark_as_read(db, room_id, current_user.id)
        
        return {
            "success": True,
            "marked_count": count
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="既読処理に失敗しました"
        )


# アカウント検索（参加者追加用）
@router.get("/accounts/search")
def search_accounts(
    query: str = "",
    role: str | None = None,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_teacher)
):
    """アカウントを検索（参加者追加用、教師のみ）"""
    try:
        accounts_query = db.query(Account).filter(
            Account.id != current_user.id  # 自分自身を除外
        )
        
        # 名前で検索
        if query:
            accounts_query = accounts_query.filter(
                Account.name.like(f"%{query}%")
            )
        
        # 役割でフィルタ
        if role:
            accounts_query = accounts_query.filter(Account.role == role)
        
        accounts = accounts_query.limit(20).all()
        
        return [
            {
                "id": account.id,
                "name": account.name,
                "role": account.role.value,
                "grade": account.grade,
                "class_name": account.class_name
            }
            for account in accounts
        ]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="アカウント検索に失敗しました"
        )

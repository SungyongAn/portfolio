from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Any, Optional
from datetime import datetime

from app.models.chat_model import ChatRoom, ChatParticipant, ChatMessage, ChatReadStatus
from app.models.accounts_model import Account, RoleEnum
from app.schemas.chat_schema import ChatRoomCreate


class ChatService:
    """チャットサービス"""
    
    @staticmethod
    def create_room(
        db: Session,
        room_data: ChatRoomCreate,
        creator_id: int
    ) -> ChatRoom:
        """
        チャットルームを作成（教師のみ）
        """
        # 作成者が教師または管理者か確認
        creator = db.query(Account).filter(Account.id == creator_id).first()
        if not creator or creator.role not in [RoleEnum.teacher, RoleEnum.admin]:
            raise ValueError("Only teachers can create chat rooms")
        
        # ルーム作成
        room = ChatRoom(
            name=room_data.name,
            description=room_data.description,
            creator_id=creator_id
        )
        db.add(room)
        db.flush()  # IDを取得するためflush
        
        # 作成者を参加者に追加
        creator_participant = ChatParticipant(
            room_id=room.id,
            user_id=creator_id
        )
        db.add(creator_participant)
        
        # 指定された参加者を追加
        for user_id in room_data.participant_ids:
            if user_id != creator_id:  # 作成者は既に追加済み
                participant = ChatParticipant(
                    room_id=room.id,
                    user_id=user_id
                )
                db.add(participant)
        
        db.commit()
        db.refresh(room)
        
        return room
    
    @staticmethod
    def get_user_rooms(
        db: Session,
        user_id: int
    ) -> list[dict[str, Any]]:
        """
        ユーザーが参加しているルーム一覧を取得
        """
        # 参加しているルームを取得
        rooms = db.query(ChatRoom).join(
            ChatParticipant,
            ChatRoom.id == ChatParticipant.room_id
        ).filter(
            ChatParticipant.user_id == user_id
        ).order_by(
            ChatRoom.updated_at.desc()
        ).all()
        
        result = []
        for room in rooms:
            # 参加者数
            participant_count = db.query(ChatParticipant).filter(
                ChatParticipant.room_id == room.id
            ).count()
            
            # 最新メッセージ
            last_message = db.query(ChatMessage).filter(
                ChatMessage.room_id == room.id
            ).order_by(
                ChatMessage.sent_at.desc()
            ).first()
            
            # 未読数
            unread_count = db.query(ChatMessage).filter(
                and_(
                    ChatMessage.room_id == room.id,
                    ChatMessage.sender_id != user_id,
                    ~ChatMessage.id.in_(
                        db.query(ChatReadStatus.message_id).filter(
                            ChatReadStatus.user_id == user_id
                        )
                    )
                )
            ).count()
            
            result.append({
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "creator_id": room.creator_id,
                "creator_name": room.creator.name,
                "participant_count": participant_count,
                "last_message": last_message.message if last_message else None,
                "last_message_at": last_message.sent_at if last_message else None,
                "unread_count": unread_count,
                "created_at": room.created_at
            })
        
        return result
    
    @staticmethod
    def get_room_detail(
        db: Session,
        room_id: int,
        user_id: int
    ) -> Optional[dict[str, Any]]:
        """
        ルーム詳細を取得（参加者のみ）
        """
        # 参加権限確認
        if not ChatService.is_participant(db, room_id, user_id):
            return None

        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            return None

        # 参加者情報
        participants = db.query(
            ChatParticipant, Account
        ).join(
            Account, ChatParticipant.user_id == Account.id
        ).filter(
            ChatParticipant.room_id == room_id
        ).all()
        
        participant_list = [
            {
                "user_id": p.ChatParticipant.user_id,
                "name": p.Account.name,
                "role": p.Account.role.value,
                "joined_at": p.ChatParticipant.joined_at
            }
            for p in participants
        ]
        
        return {
            "id": room.id,
            "name": room.name,
            "description": room.description,
            "creator_id": room.creator_id,
            "creator_name": room.creator.name,
            "participants": participant_list,
            "created_at": room.created_at
        }
    
    @staticmethod
    def delete_room(
        db: Session,
        room_id: int,
        user_id: int
    ) -> bool:
        """
        ルームを削除（作成者のみ）
        """
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        
        if not room:
            return False
        
        # 作成者でない場合は削除不可
        if room.creator_id != user_id:
            return False
        
        # カスケード削除で関連データも削除される
        db.delete(room)
        db.commit()
        
        return True
    
    @staticmethod
    def add_participants(
        db: Session,
        room_id: int,
        user_id: int,
        participant_ids: list[int]
    ) -> bool:
        """
        参加者を追加（作成者のみ）
        """
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()

        if not room or room.creator_id != user_id:
            return False

        for participant_id in participant_ids:
            # 既に参加している場合はスキップ
            existing = db.query(ChatParticipant).filter(
                and_(
                    ChatParticipant.room_id == room_id,
                    ChatParticipant.user_id == participant_id
                )
            ).first()
            
            if not existing:
                participant = ChatParticipant(
                    room_id=room_id,
                    user_id=participant_id
                )
                db.add(participant)
        
        db.commit()
        return True
    
    @staticmethod
    def remove_participant(
        db: Session,
        room_id: int,
        user_id: int,
        target_user_id: int
    ) -> bool:
        """
        参加者を削除（作成者のみ、作成者自身は削除不可）
        """
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        
        if not room or room.creator_id != user_id:
            return False
        
        # 作成者自身は削除不可
        if target_user_id == user_id:
            return False
        
        participant = db.query(ChatParticipant).filter(
            and_(
                ChatParticipant.room_id == room_id,
                ChatParticipant.user_id == target_user_id
            )
        ).first()
        
        if participant:
            db.delete(participant)
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def send_message(
        db: Session,
        room_id: int,
        sender_id: int,
        message_text: str
    ) -> Optional[ChatMessage]:
        """
        メッセージを送信（参加者のみ）
        """
        # 参加権限確認
        if not ChatService.is_participant(db, room_id, sender_id):
            return None
        
        message = ChatMessage(
            room_id=room_id,
            sender_id=sender_id,
            message=message_text
        )
        db.add(message)
        
        # ルームの更新日時を更新
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if room:
            room.updated_at = datetime.now()
        
        db.commit()
        db.refresh(message)
        
        return message
    
    @staticmethod
    def get_messages(
        db: Session,
        room_id: int,
        user_id: int,
        limit: int = 50,
        before_message_id: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """
        メッセージ一覧を取得（参加者のみ）
        """
        # 参加権限確認
        if not ChatService.is_participant(db, room_id, user_id):
            return []
        
        query = db.query(ChatMessage).filter(
            ChatMessage.room_id == room_id
        )
        
        # ページネーション（指定されたメッセージより前）
        if before_message_id:
            query = query.filter(ChatMessage.id < before_message_id)
        
        messages = query.order_by(
            ChatMessage.sent_at.desc()
        ).limit(limit).all()
        
        result = []
        for message in reversed(messages):  # 古い順に並べ替え
            # 既読情報
            read_by = db.query(Account.name).join(
                ChatReadStatus,
                Account.id == ChatReadStatus.user_id
            ).filter(
                ChatReadStatus.message_id == message.id
            ).all()
            
            read_by_names = [name[0] for name in read_by]
            
            result.append({
                "id": message.id,
                "room_id": message.room_id,
                "sender_id": message.sender_id,
                "sender_name": message.sender.name,
                "sender_role": message.sender.role.value,
                "message": message.message,
                "sent_at": message.sent_at,
                "is_read": user_id in [rs.user_id for rs in message.read_status],
                "read_by": read_by_names
            })
        
        return result
    
    @staticmethod
    def mark_as_read(
        db: Session,
        room_id: int,
        user_id: int
    ) -> int:
        """
        未読メッセージを既読にする
        """
        # 参加権限確認
        if not ChatService.is_participant(db, room_id, user_id):
            return 0
        
        # 未読メッセージを取得
        unread_messages = db.query(ChatMessage).filter(
            and_(
                ChatMessage.room_id == room_id,
                ChatMessage.sender_id != user_id,  # 自分のメッセージは除外
                ~ChatMessage.id.in_(
                    db.query(ChatReadStatus.message_id).filter(
                        ChatReadStatus.user_id == user_id
                    )
                )
            )
        ).all()
        
        count = 0
        for message in unread_messages:
            read_status = ChatReadStatus(
                message_id=message.id,
                user_id=user_id
            )
            db.add(read_status)
            count += 1
        
        db.commit()
        return count
    
    @staticmethod
    def is_participant(
        db: Session,
        room_id: int,
        user_id: int
    ) -> bool:
        """
        ユーザーがルームの参加者かチェック
        """
        participant = db.query(ChatParticipant).filter(
            and_(
                ChatParticipant.room_id == room_id,
                ChatParticipant.user_id == user_id
            )
        ).first()
        
        return participant is not None
    
    @staticmethod
    def is_creator(
        db: Session,
        room_id: int,
        user_id: int
    ) -> bool:
        """
        ユーザーがルームの作成者かチェック
        """
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        return room and room.creator_id == user_id

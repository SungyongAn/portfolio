from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class ChatRoom(Base):
    """チャットルーム"""
    __tablename__ = "chat_rooms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # リレーション
    creator = relationship("Account", foreign_keys=[creator_id])
    participants = relationship("ChatParticipant", back_populates="room", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="room", cascade="all, delete-orphan")


class ChatParticipant(Base):
    """チャットルーム参加者"""
    __tablename__ = "chat_participants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('chat_rooms.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    joined_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # リレーション
    room = relationship("ChatRoom", back_populates="participants")
    user = relationship("Account")


class ChatMessage(Base):
    """チャットメッセージ"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('chat_rooms.id', ondelete='CASCADE'), nullable=False)
    sender_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # リレーション
    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("Account")
    read_status = relationship("ChatReadStatus", back_populates="message", cascade="all, delete-orphan")


class ChatReadStatus(Base):
    """メッセージ既読状態"""
    __tablename__ = "chat_read_status"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('chat_messages.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    read_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # リレーション
    message = relationship("ChatMessage", back_populates="read_status")
    user = relationship("Account")

from sqlalchemy import Column, String, Enum, TIMESTAMP
from routes.db import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    admission_year = Column(String(4), nullable=False)
    graduation_year = Column(String(4), nullable=False)
    password = Column(String(255), nullable=False)  # ハッシュ化済み
    affiliation = Column(String(255), nullable=False)
    role = Column(Enum('ユーザー', '図書委員', '司書', '管理者'), nullable=False, default='ユーザー')
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

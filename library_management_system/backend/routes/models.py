from sqlalchemy import Column, String, Integer, Enum, DateTime, text
from sqlalchemy.sql import func
from routes.db import Base


class Account(Base):
    __tablename__ = "accounts"
    
    # 必須フィールド（NOT NULL）
    user_id = Column(String(50), primary_key=True, comment='利用者ID')
    username = Column(String(100), nullable=False, comment='ユーザー名')
    email = Column(String(255), unique=True, nullable=False, comment='メールアドレス')
    admission_year = Column(Integer, nullable=False, comment='入学年(西暦)')
    graduation_year = Column(Integer, nullable=False, comment='卒業予定年(西暦)')
    password = Column(String(255), nullable=False, comment='パスワード(ハッシュ化推奨)')
    affiliation = Column(String(255), nullable=False, comment='所属(学校名)')
    
    # ENUM型（デフォルト値あり）
    role = Column(
        Enum('ユーザー', '図書委員', '司書', '管理者', name='role_enum'), 
        nullable=False, 
        default='ユーザー',
        comment='権限'
    )
    
    # タイムスタンプ
    created_at = Column(
        DateTime, 
        nullable=False,
        server_default=func.current_timestamp(),
        comment='作成日時'
    )
    updated_at = Column(
        DateTime, 
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新日時'
    )

    def __repr__(self):
        return f"<Account(user_id='{self.user_id}', username='{self.username}', role='{self.role}')>"
    
    # パスワードが設定されているかチェック
    def has_password(self):
        return bool(self.password and self.password.strip())
    
    # ユーザー情報の辞書形式での取得
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'admission_year': self.admission_year,
            'graduation_year': self.graduation_year,
            'affiliation': self.affiliation,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

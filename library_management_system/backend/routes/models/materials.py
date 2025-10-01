from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from routes.db import Base
from datetime import date


# NDCテーブル（分類マスタ）
class NDC(Base):
    __tablename__ = "NDC"

    ndc_code = Column(String(10), primary_key=True, comment='NDCコード')
    ndc_name = Column(String(100), nullable=False, comment='分類名')
    
    # リレーション
    materials = relationship("Material", back_populates="ndc")


# 資料種別マスタ
class MaterialType(Base):
    __tablename__ = "MaterialType"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), nullable=False, unique=True, comment='種別名')
    
    # リレーション
    materials = relationship("Material", back_populates="material_type")


# 貸出状況マスタ
class LoanStatus(Base):
    __tablename__ = "LoanStatus"

    status_code = Column(String(20), primary_key=True, comment='状態コード')
    status_name = Column(String(50), nullable=False, comment='状態名')
    
    # リレーション
    materials = relationship("Material", back_populates="loan_status_info")


# 資料テーブル
class Material(Base):
    __tablename__ = "Materials"

    material_id = Column(Integer, primary_key=True, autoincrement=True)
    barcode = Column(String(50), nullable=False, unique=True, comment='一元バーコード番号')
    title = Column(String(255), nullable=False, comment='書籍タイトル')
    author = Column(String(100), comment='著者名')
    publisher = Column(String(100), comment='出版社')
    ndc_code = Column(String(10), ForeignKey('NDC.ndc_code'), nullable=False, comment='分類(NDC)')
    type_id = Column(Integer, ForeignKey('MaterialType.type_id'), nullable=False, comment='種別')
    affiliation = Column(String(255), nullable=False, comment='学校名')
    shelf = Column(String(50), comment='棚版')
    loan_status = Column(String(20), ForeignKey('LoanStatus.status_code'), nullable=False, comment='貸出状況')
    registration_date = Column(Date, nullable=False, default=date.today, comment='登録日')
    
    # リレーション
    ndc = relationship("NDC", back_populates="materials")
    material_type = relationship("MaterialType", back_populates="materials")
    loan_status_info = relationship("LoanStatus", back_populates="materials")

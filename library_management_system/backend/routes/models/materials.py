from sqlalchemy import Column, String, Integer
from routes.db import Base


class Material(Base):
    __tablename__ = "Materials"

    material_id = Column(Integer, primary_key=True, autoincrement=True)
    barcode = Column(String(50), nullable=False, unique=True, comment='一元バーコード番号')

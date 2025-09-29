from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from routes.db import Base


class MaterialType(Base):
    __tablename__ = "materialtype"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), nullable=False, unique=True)

    # Materialとのリレーションシップ
    materials = relationship("Material", back_populates="material_type")


# from sqlalchemy import Column, String
# from sqlalchemy.orm import relationship
# from routes.db import Base


# class NDC(Base):
#     __tablename__ = "ndc"

#     ndc_code = Column(String(10), primary_key=True, comment='分類コード(NDC)')
#     ndc_name = Column(String(100), nullable=False, comment='分類名')

#     # Materialとのリレーションシップ
#     materials = relationship("Material", back_populates="ndc")


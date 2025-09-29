# from sqlalchemy import Column, String
# from sqlalchemy.orm import relationship
# from routes.db import Base


# class LoanStatus(Base):
#     __tablename__ = "loanstatus"

#     status_code = Column(String(20), primary_key=True)
#     status_name = Column(String(50), nullable=False)

#     # Materialとのリレーションシップ
#     materials = relationship("Material", back_populates="loan_status_ref")

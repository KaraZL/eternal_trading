from sqlalchemy.orm import Column, String
from app.db.base import Base

class Collateral(Base):
    __tablename__ = "collaterals"

    id = Column(String, primary_key=True, index=True)
    loan_id = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    market_value = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    haircut = Column(String, nullable=False)
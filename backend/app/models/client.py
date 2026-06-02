from sqlalchemy.orm import Column, String
from app.db.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    risk_rating = Column(String, nullable=False)
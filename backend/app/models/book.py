from sqlalchemy.orm import Column, String
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)
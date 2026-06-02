from sqlalchemy.orm import Column, String
from app.db.base import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True, index=True)
    client_id = Column(String, nullable=False)
    book_id = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    currency = Column(String, nullable=False)
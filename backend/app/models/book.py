from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.loan import Loan

class Book(Base):
    """Represents a book in the system, with a relationship to the Loan model."""
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)

    loan: Mapped[list["Loan"]] = relationship("Loan", back_populates="book")
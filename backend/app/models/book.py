from uuid import uuid4
from sqlalchemy import String, UUID, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.loan import Loan

class Book(Base):
    """Represents a book in the system, with a relationship to the Loan model."""
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)

    loan: Mapped[list["Loan"]] = relationship("Loan", back_populates="book")
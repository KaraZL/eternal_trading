from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.loan import Loan

class Client(Base):
    """Represents a client in the system, with a relationship to the Loan model."""
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    risk_rating: Mapped[str] = mapped_column(String, nullable=False)

    loan: Mapped["Loan"] = relationship("Loan", back_populates="client")
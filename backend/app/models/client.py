from uuid import uuid4
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.loan import Loan

class Client(Base):
    """Represents a client in the system, with a relationship to the Loan model."""
    __tablename__ = "clients"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid4)
    '''UUID is a universally unique identifier, which is a 128-bit number used to uniquely identify information in computer systems.
    The default=uuid4 argument tells SQLAlchemy to automatically generate a new UUID using the uuid4() function from the uuid module whenever a new Client instance is created without an explicit ID.'''

    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    risk_rating: Mapped[str] = mapped_column(String, nullable=False)

    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="client")
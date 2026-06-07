from decimal import Decimal
from uuid import uuid4
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Numeric, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.loan import Loan

class Collateral(Base):
    """Represents a collateral item in the system, with a relationship to the Loan model."""
    __tablename__ = "collaterals"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid4)
    loan_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("loans.id"), nullable=False)
    asset_type: Mapped[str] = mapped_column(String, nullable=False)
    asset_name: Mapped[str] = mapped_column(String, nullable=False)
    market_value: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    haircut: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    loans: Mapped["Loan"] = relationship("Loan", back_populates="collateral_items")

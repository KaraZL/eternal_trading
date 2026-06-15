from decimal import Decimal
from datetime import datetime
from uuid import uuid4, UUID
"""uuid4 is a function() which create a value"""
from sqlalchemy import Uuid, ForeignKey, String, JSON, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.book import Book

from app.db.base import Base

class ScenarioRun(Base):
    __tablename__ = "scenario_runs"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    book_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("books.id"), nullable=False)

    scenario_name: Mapped[str] = mapped_column(String, nullable=False)
    asset_type_shocks: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    base_total_loan_exposure: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    base_total_collateral_market_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    base_total_eligible_collateral_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    base_weighted_ltv: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    base_risk_status: Mapped[str] = mapped_column(String, nullable=False)

    stressed_total_collateral_market_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    stressed_total_eligible_collateral_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    stressed_weighted_ltv: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    stressed_risk_status: Mapped[str] = mapped_column(String, nullable=False)

    base_total_position_market_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    stressed_total_position_market_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="scenario_runs")
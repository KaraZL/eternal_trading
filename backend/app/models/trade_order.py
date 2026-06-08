from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import UUID, ForeignKey, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.book import Book

class TradeOrder(Base):
    __tablename__ = "trade_orders"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid4)
    book_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("books.id"), nullable=False)
    side: Mapped[str] = mapped_column(String, nullable=False)
    asset_type: Mapped[str] = mapped_column(String, nullable=False)
    asset_name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=4), nullable=False)
    limit_price: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=4), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    execution_price: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    book: Mapped["Book"] = relationship("Book", back_populates="trade_orders")
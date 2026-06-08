from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class TradeOrderRequest(BaseModel):
    book_id: UUID
    side: str
    asset_type: str
    asset_name: str
    quantity: Decimal
    limit_price: Decimal
    currency: str

class TradeOrderExecutionRequest(BaseModel):
    execution_price: Decimal

class TradeOrderResponse(BaseModel):
    id: UUID
    book_id: UUID
    side: str
    asset_type: str
    asset_name: str
    quantity: Decimal
    limit_price: Decimal
    currency: str
    status: str
    execution_price: Decimal | None = None
    executed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


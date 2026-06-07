from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

class TradeOrderRequest(BaseModel):
    book_id: UUID = Field(...)
    side: str = Field(...)
    asset_type: str = Field(...)
    asset_name: str = Field(...)
    quantity: Decimal = Field(...)
    limit_price: Decimal = Field(...)
    currency: str = Field(...)

class TradeOrderResponse(BaseModel):
    id: Optional[UUID] = Field()
    book_id: UUID = Field(...)
    side: str = Field(...)
    asset_type: str = Field(...)
    asset_name: str = Field(...)
    quantity: Decimal = Field(...)
    limit_price: Decimal = Field(...)
    currency: str = Field(...)
    status: str = Field(...)

    class Config:
        from_attributes = True


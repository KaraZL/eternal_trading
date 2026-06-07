from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class PositionRequest(BaseModel):
    book_id: UUID = Field(...)
    asset_type: str = Field(...)
    asset_name: str = Field(...)
    quantity: Decimal = Field(..., gt=0)
    market_price: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)

class PositionResponse(BaseModel):
    id: Optional[UUID] = Field()
    book_id: Optional[UUID] = Field(...)
    asset_type: str = Field(...)
    asset_name: str = Field(...)
    quantity: Decimal = Field(..., gt=0)
    market_price: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    market_value: Optional[Decimal]

    model_config = ConfigDict(from_attributes=True)
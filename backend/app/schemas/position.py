from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class PositionRequest(BaseModel):
    book_id: UUID
    asset_type: str
    asset_name: str
    quantity: Decimal = Field(..., gt=0)
    market_price: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)

class PositionResponse(BaseModel):
    id: UUID
    book_id: UUID
    asset_type: str
    asset_name: str
    quantity: Decimal
    market_price: Decimal
    currency: str
    market_value: Decimal

    model_config = ConfigDict(from_attributes=True)
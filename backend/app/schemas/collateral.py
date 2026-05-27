"""Pydantic schemas for Collateral API."""

from decimal import Decimal
from pydantic import BaseModel, Field


class CollateralBase(BaseModel):
    """Base collateral schema."""

    loan_id: str = Field(..., min_length=1)
    asset_type: str = Field(..., min_length=1, max_length=100)
    asset_name: str = Field(..., min_length=1, max_length=255)
    market_value: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(..., min_length=3, max_length=3)
    haircut_percentage: Decimal = Field(..., ge=0, le=1, decimal_places=4)


class CollateralCreate(CollateralBase):
    """Schema for creating collateral."""

    pass


class CollateralResponse(CollateralBase):
    """Schema for collateral response."""

    id: str

    class Config:
        from_attributes = True

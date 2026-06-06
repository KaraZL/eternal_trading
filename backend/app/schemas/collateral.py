"""Pydantic schemas for Collateral API."""

from decimal import Decimal
from pydantic import BaseModel, Field


class CollateralRequest(BaseModel):
    """Schema for creating collateral.
    
    The haircut_percentage is applied to market_value to calculate eligible collateral value.
    For example, 0.10 means 10% haircut, so eligible value = market_value * (1 - 0.10).
    """

    loan_id: str = Field(..., min_length=1, description="ID of the associated loan")
    asset_type: str = Field(..., min_length=1, max_length=100, description="Type of asset (e.g., Stock, Bond)")
    asset_name: str = Field(..., min_length=1, max_length=255, description="Name or description of the asset")
    market_value: Decimal = Field(..., gt=0, decimal_places=2, description="Current market value of the asset")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., USD)")
    haircut_percentage: Decimal = Field(..., ge=0, le=1, decimal_places=4, description="Haircut percentage (0.0 to 1.0)")


class CollateralResponse(BaseModel):
    """Schema for reading collateral data."""

    id: str = Field(..., description="Unique collateral ID")
    loan_id: str = Field(..., description="ID of the associated loan")
    asset_type: str = Field(..., description="Type of asset")
    asset_name: str = Field(..., description="Name or description of the asset")
    market_value: Decimal = Field(..., description="Current market value of the asset")
    currency: str = Field(..., description="Currency code")
    haircut_percentage: Decimal = Field(..., description="Haircut percentage (0.0 to 1.0)")

    class Config:
        from_attributes = True

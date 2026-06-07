"""Pydantic schemas for Collateral API."""

from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CollateralRequest(BaseModel):
    """Schema for creating collateral.
    
    The haircut_percentage is applied to market_value to calculate eligible collateral value.
    For example, 0.10 means 10% haircut, so eligible value = market_value * (1 - 0.10).
    """

    loan_id: UUID = Field(..., description="ID of the associated loan")
    asset_type: str = Field(..., min_length=1, max_length=100, description="Type of asset (e.g., Stock, Bond)")
    asset_name: str = Field(..., min_length=1, max_length=255, description="Name or description of the asset")
    market_value: Decimal = Field(..., gt=0, decimal_places=2, description="Current market value of the asset")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., USD)")
    haircut_percentage: Decimal = Field(..., ge=0, le=1, decimal_places=4, description="Haircut percentage (0.0 to 1.0)")


class CollateralResponse(BaseModel):
    """Schema for reading collateral data."""

    id: UUID = Field(..., description="Unique collateral ID")
    loan_id: UUID = Field(..., description="ID of the associated loan")
    asset_type: str = Field(..., description="Type of asset")
    asset_name: str = Field(..., description="Name or description of the asset")
    market_value: Decimal = Field(..., description="Current market value of the asset")
    currency: str = Field(..., description="Currency code")
    haircut_percentage: Decimal = Field(..., description="Haircut percentage (0.0 to 1.0)", validation_alias="haircut")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "loan_id": "9c93a975-c60f-47ab-9a85-105eef76dc86",
                "asset_type": "equity",
                "asset_name": "Nestle shares",
                "market_value": "2000000.00",
                "currency": "CHF",
                "haircut_percentage": "0.20",
            }
        },
    )

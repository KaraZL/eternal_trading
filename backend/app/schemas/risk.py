"""Pydantic schemas for risk assessment API."""

from decimal import Decimal
from pydantic import BaseModel, Field


class RiskAssessmentRequest(BaseModel):
    """Request model for loan risk assessment."""

    loan_amount: Decimal = Field(..., gt=0, decimal_places=2)
    collateral_market_value: Decimal = Field(..., gt=0, decimal_places=2)
    haircut_percentage: Decimal = Field(
        ..., ge=0, le=1, decimal_places=2, description="Haircut as decimal (0.0 to 1.0)"
    )
    warning_ltv_threshold: Decimal = Field(
        default=Decimal("0.60"), ge=0, le=1, decimal_places=2
    )
    breach_ltv_threshold: Decimal = Field(
        default=Decimal("0.70"), ge=0, le=1, decimal_places=2
    )


class RiskAssessmentResponse(BaseModel):
    """Response model for loan risk assessment."""

    eligible_collateral_value: Decimal = Field(..., decimal_places=2)
    ltv: Decimal = Field(..., decimal_places=4)
    status: str = Field(..., description="Status: 'healthy', 'warning', or 'breach'")

"""Pydantic schemas for Loan API."""

from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class LoanRequest(BaseModel):
    """Schema for creating a loan."""

    client_id: UUID = Field(..., description="ID of the borrower client")
    book_id: UUID = Field(..., description="ID of the portfolio book")
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="Loan amount")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., USD)")


class LoanResponse(BaseModel):
    """Schema for reading loan data."""

    id: UUID = Field(..., description="Unique loan ID")
    client_id: UUID = Field(..., description="ID of the borrower client")
    book_id: UUID = Field(..., description="ID of the portfolio book")
    amount: Decimal = Field(..., description="Loan amount")
    currency: str = Field(..., description="Currency code (e.g., USD)")

    model_config = ConfigDict(from_attributes=True)

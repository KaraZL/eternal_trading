"""Pydantic schemas for Loan API."""

from decimal import Decimal
from pydantic import BaseModel, Field


class LoanBase(BaseModel):
    """Base loan schema."""

    client_id: str = Field(..., min_length=1)
    book_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(..., min_length=3, max_length=3)


class LoanCreate(LoanBase):
    """Schema for creating a loan."""

    pass


class LoanResponse(LoanBase):
    """Schema for loan response."""

    id: str

    class Config:
        from_attributes = True

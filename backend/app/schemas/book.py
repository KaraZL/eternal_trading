"""Pydantic schemas for Book API."""

from uuid import UUID
from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    """Schema for creating a book (lending or trading portfolio)."""

    name: str = Field(..., min_length=1, max_length=255, description="Book name")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., USD)")


class BookResponse(BaseModel):
    """Schema for reading book data."""

    id: UUID = Field(..., description="Unique book ID")
    name: str = Field(..., description="Book name")
    currency: str = Field(..., description="Currency code (e.g., USD)")

    class Config:
        from_attributes = True

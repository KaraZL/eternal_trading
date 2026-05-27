"""Pydantic schemas for Book API."""

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Base book schema."""

    name: str = Field(..., min_length=1, max_length=255)
    currency: str = Field(..., min_length=3, max_length=3)


class BookCreate(BookBase):
    """Schema for creating a book."""

    pass


class BookResponse(BookBase):
    """Schema for book response."""

    id: str

    class Config:
        from_attributes = True

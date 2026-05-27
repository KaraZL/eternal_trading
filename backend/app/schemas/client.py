"""Pydantic schemas for Client API."""

from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    """Base client schema."""

    name: str = Field(..., min_length=1, max_length=255)
    country: str = Field(..., min_length=1, max_length=100)
    risk_rating: str = Field(..., min_length=1, max_length=50)


class ClientCreate(ClientBase):
    """Schema for creating a client."""

    pass


class ClientResponse(ClientBase):
    """Schema for client response."""

    id: str

    class Config:
        from_attributes = True

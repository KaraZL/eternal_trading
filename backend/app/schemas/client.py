"""Pydantic schemas for Client API."""

from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ClientRequest(BaseModel):
    """Schema for creating a client."""

    name: str = Field(..., min_length=1, max_length=255, description="Client name")
    country: str = Field(..., min_length=1, max_length=100, description="Country code or name")
    risk_rating: str = Field(..., min_length=1, max_length=50, description="Risk rating")


class ClientResponse(BaseModel):
    """Schema for reading client data."""

    id: UUID = Field(..., description="Unique client ID")
    name: str = Field(..., description="Client name")
    country: str = Field(..., description="Country code or name")
    risk_rating: str = Field(..., description="Risk rating")

    model_config = ConfigDict(from_attributes=True)

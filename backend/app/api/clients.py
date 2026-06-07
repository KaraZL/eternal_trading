"""Client API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.client import ClientRequest, ClientResponse
from ..services.client_service import create_client, get_client, list_clients

router = APIRouter()


@router.post("", response_model=ClientResponse)
async def create_client_route(request: ClientRequest, db: Session = Depends(get_db)) -> ClientResponse:
    """Create a new client."""
    return create_client(db, request)


@router.get("", response_model=list[ClientResponse])
async def list_clients_route(db: Session = Depends(get_db)) -> list[ClientResponse]:
    """List all clients."""
    return list_clients(db)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_route(client_id: str, db: Session = Depends(get_db)) -> ClientResponse:
    """Get a client by ID."""
    client = get_client(db, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

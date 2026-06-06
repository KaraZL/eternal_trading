"""Client API routes."""

from fastapi import APIRouter, HTTPException

from ..db.store import clients, generate_id
from ..schemas.client import ClientRequest, ClientResponse

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("", response_model=ClientResponse)
async def create_client(request: ClientRequest) -> ClientResponse:
    """Create a new client."""
    client_id = generate_id("client", clients)
    client = {
        "id": client_id,
        "name": request.name,
        "country": request.country,
        "risk_rating": request.risk_rating,
    }
    clients[client_id] = client
    return ClientResponse(**client)


@router.get("", response_model=list[ClientResponse])
async def list_clients() -> list[ClientResponse]:
    """List all clients."""
    return [ClientResponse(**client) for client in clients.values()]

"""Collateral API routes."""

from fastapi import APIRouter

from ..db.store import collateral_list, generate_id
from ..schemas.collateral import CollateralRequest, CollateralResponse

router = APIRouter(prefix="/api/collateral", tags=["collateral"])


@router.post("", response_model=CollateralResponse)
async def add_collateral(request: CollateralRequest) -> CollateralResponse:
    """Add collateral to a loan."""
    collateral_id = generate_id("collateral", collateral_list)
    collateral = {
        "id": collateral_id,
        "loan_id": request.loan_id,
        "asset_type": request.asset_type,
        "asset_name": request.asset_name,
        "market_value": request.market_value,
        "currency": request.currency,
        "haircut_percentage": request.haircut_percentage,
    }
    collateral_list.append(collateral)
    return CollateralResponse(**collateral)


@router.get("", response_model=list[CollateralResponse])
async def list_collateral() -> list[CollateralResponse]:
    """List all collateral."""
    return [CollateralResponse(**c) for c in collateral_list]

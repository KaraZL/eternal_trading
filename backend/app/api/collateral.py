"""Collateral API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.collateral import CollateralRequest, CollateralResponse
from ..services.collateral_service import (
    create_collateral,
    get_collateral,
    list_collateral,
    list_collateral_by_loan,
)

router = APIRouter()


@router.post("", response_model=CollateralResponse)
async def create_collateral_route(
    request: CollateralRequest, db: Session = Depends(get_db)
) -> CollateralResponse:
    """Add collateral to a loan."""
    return create_collateral(db, request)


@router.get("", response_model=list[CollateralResponse])
async def list_collateral_route(db: Session = Depends(get_db)) -> list[CollateralResponse]:
    """List all collateral."""
    return list_collateral(db)


@router.get("/loan/{loan_id}", response_model=list[CollateralResponse])
async def list_collateral_by_loan_route(
    loan_id: str, db: Session = Depends(get_db)
) -> list[CollateralResponse]:
    """List all collateral for a specific loan."""
    return list_collateral_by_loan(db, loan_id)


@router.get("/{collateral_id}", response_model=CollateralResponse)
async def get_collateral_route(
    collateral_id: str, db: Session = Depends(get_db)
) -> CollateralResponse:
    """Get collateral by ID."""
    collateral = get_collateral(db, collateral_id)
    if collateral is None:
        raise HTTPException(status_code=404, detail="Collateral not found")
    return collateral

"""Loan API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.loan import LoanRequest, LoanResponse
from ..services.loan_service import create_loan, get_loan, list_loans
from ..services.risk_service import assess_loan_risk_with_collateral

router = APIRouter(prefix="/api/loans", tags=["loans"])


@router.post("", response_model=LoanResponse)
async def create_loan_route(request: LoanRequest, db: Session = Depends(get_db)) -> LoanResponse:
    """Create a new loan."""
    return create_loan(db, request)


@router.get("", response_model=list[LoanResponse])
async def list_loans_route(db: Session = Depends(get_db)) -> list[LoanResponse]:
    """List all loans."""
    return list_loans(db)


@router.get("/{loan_id}/risk")
async def get_loan_risk(loan_id: str, db: Session = Depends(get_db)) -> dict:
    """
    Calculate risk metrics for a loan.

    Returns:
        Dictionary with loan_id, loan_amount, total_market_value,
        total_eligible_collateral_value, ltv, status, and collateral_count.

    Raises:
        HTTPException 404: If loan not found
        HTTPException 400: If loan has no collateral
    """
    from ..services.collateral_service import list_collateral_by_loan

    loan = get_loan(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan_collateral = list_collateral_by_loan(db, loan_id)
    if not loan_collateral:
        raise HTTPException(status_code=400, detail="Loan has no collateral")

    result = assess_loan_risk_with_collateral(loan, loan_collateral)
    return result


@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan_route(loan_id: str, db: Session = Depends(get_db)) -> LoanResponse:
    """Get a loan by ID."""
    loan = get_loan(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

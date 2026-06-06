"""Loan API routes."""

from fastapi import APIRouter, HTTPException

from ..db.store import loans, generate_id, collateral_list
from ..schemas.loan import LoanRequest, LoanResponse
from ..services.risk_service import assess_loan_risk_with_collateral

router = APIRouter(prefix="/api/loans", tags=["loans"])


@router.post("", response_model=LoanResponse)
async def create_loan(request: LoanRequest) -> LoanResponse:
    """Create a new loan."""
    loan_id = generate_id("loan", loans)
    loan = {
        "id": loan_id,
        "client_id": request.client_id,
        "book_id": request.book_id,
        "amount": request.amount,
        "currency": request.currency,
    }
    loans[loan_id] = loan
    return LoanResponse(**loan)


@router.get("", response_model=list[LoanResponse])
async def list_loans() -> list[LoanResponse]:
    """List all loans."""
    return [LoanResponse(**loan) for loan in loans.values()]


@router.get("/{loan_id}/risk")
async def get_loan_risk(loan_id: str) -> dict:
    """
    Calculate risk metrics for a loan.

    Returns:
        Dictionary with loan_id, loan_amount, total_market_value,
        total_eligible_collateral_value, ltv, status, and collateral_count.

    Raises:
        HTTPException 404: If loan not found
        HTTPException 400: If loan has no collateral
    """
    if loan_id not in loans:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan = loans[loan_id]

    # Find collateral for this loan
    loan_collateral = [c for c in collateral_list if c["loan_id"] == loan_id]

    if not loan_collateral:
        raise HTTPException(status_code=400, detail="Loan has no collateral")

    result = assess_loan_risk_with_collateral(loan, loan_collateral)
    return result

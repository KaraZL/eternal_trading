"""FastAPI application for AI-assisted lending platform."""

from decimal import Decimal
from fastapi import FastAPI

from .schemas.risk import LTVCalculationRequest, LTVCalculationResponse, RiskAssessmentRequest, RiskAssessmentResponse
from .services.risk_service import assess_loan_risk

app = FastAPI(title="Eternal Lending Platform", version="0.1.0")


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/risk/assess", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest) -> RiskAssessmentResponse:
    """
    Assess loan risk based on LTV calculation.

    Args:
        request: Risk assessment request with loan details

    Returns:
        Risk assessment response with LTV and status
    """
    result = assess_loan_risk(
        loan_amount=request.loan_amount,
        collateral_market_value=request.collateral_market_value,
        haircut_percentage=request.haircut_percentage,
        warning_ltv_threshold=request.warning_ltv_threshold,
        breach_ltv_threshold=request.breach_ltv_threshold,
    )

    return RiskAssessmentResponse(
        eligible_collateral_value=result["eligible_collateral_value"],
        ltv=result["ltv"],
        status=result["status"],
    )

@app.post("/api/risk/ltv", response_model=LTVCalculationResponse)
async def calculate_ltv_endpoint(request: LTVCalculationRequest) -> LTVCalculationResponse:
    """
    Calculate LTV based on loan amount and collateral.

    Args:
        request: LTV calculation request with loan details
    Returns:
        LTV calculation response with eligible collateral and LTV
    """
    eligible_collateral_value = assess_loan_risk(
        loan_amount=request.loan_amount,
        collateral_market_value=request.collateral_market_value,
        haircut_percentage=request.haircut_percentage,
        warning_ltv_threshold=request.warning_ltv_threshold,
        breach_ltv_threshold=request.breach_ltv_threshold,
    )["eligible_collateral_value"]

    ltv = assess_loan_risk(
        loan_amount=request.loan_amount,
        collateral_market_value=request.collateral_market_value,
        haircut_percentage=request.haircut_percentage,
        warning_ltv_threshold=request.warning_ltv_threshold,
        breach_ltv_threshold=request.breach_ltv_threshold,
    )["ltv"]

    return LTVCalculationResponse(
        eligible_collateral_value=eligible_collateral_value,
        ltv=ltv,
        loan_amount=request.loan_amount,
        collateral_market_value=request.collateral_market_value,
        haircut_percentage=request.haircut_percentage,
        status=assess_loan_risk(
            loan_amount=request.loan_amount,
            collateral_market_value=request.collateral_market_value,
            haircut_percentage=request.haircut_percentage,
            warning_ltv_threshold=request.warning_ltv_threshold,
            breach_ltv_threshold=request.breach_ltv_threshold,
        )["status"]
    )


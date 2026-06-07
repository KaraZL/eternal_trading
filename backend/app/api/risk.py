
from fastapi import APIRouter

from ..schemas.risk import LTVCalculationRequest, LTVCalculationResponse, RiskAssessmentRequest, RiskAssessmentResponse
from ..services.risk_service import assess_loan_risk
from ..db.store import risk_assessments

router = APIRouter(prefix="/api/risk", tags=["risk"])

@router.post("/assess", response_model=RiskAssessmentResponse)
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

    risk_assessments.append(result)

    return RiskAssessmentResponse(
        eligible_collateral_value=result["eligible_collateral_value"],
        ltv=result["ltv"],
        status=result["status"],
    )

@router.post("/ltv", response_model=LTVCalculationResponse)
async def calculate_ltv_endpoint(request: LTVCalculationRequest) -> LTVCalculationResponse:
    """
    Calculate LTV based on loan amount and collateral.

    Args:
        request: LTV calculation request with loan details
    Returns:
        LTV calculation response with eligible collateral and LTV
    """
    result = assess_loan_risk(
        loan_amount=request.loan_amount,
        collateral_market_value=request.collateral_market_value,
        haircut_percentage=request.haircut_percentage,
        warning_ltv_threshold=request.warning_ltv_threshold,
        breach_ltv_threshold=request.breach_ltv_threshold,
    )

    risk_assessments.append(result)

    return LTVCalculationResponse(
        eligible_collateral_value=result["eligible_collateral_value"],
        ltv=result["ltv"],
        loan_amount=request.loan_amount,
        collateral_market_value=request.collateral_market_value,
        haircut_percentage=request.haircut_percentage,
        status=result["status"]
    )


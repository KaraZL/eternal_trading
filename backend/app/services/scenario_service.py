from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.collateral import Collateral
from app.models.loan import Loan
from app.models.position import Position
from app.schemas.scenario import StressScenarioRequest, StressScenarioResponse


MONEY_QUANTIZER = Decimal("0.01")
RATIO_QUANTIZER = Decimal("0.0001")

WARNING_LTV_THRESHOLD = Decimal("0.60")
BREACH_LTV_THRESHOLD = Decimal("0.70")


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANTIZER)


def _ratio(value: Decimal) -> Decimal:
    return value.quantize(RATIO_QUANTIZER)


def _risk_status(weighted_ltv: Decimal | None) -> str:
    if weighted_ltv is None:
        return "not_applicable"

    if weighted_ltv >= BREACH_LTV_THRESHOLD:
        return "breach"

    if weighted_ltv >= WARNING_LTV_THRESHOLD:
        return "warning"

    return "healthy"


def _apply_shock(value: Decimal, shock: Decimal) -> Decimal:
    """
    Example:
    value = 100
    shock = -0.20
    result = 80
    """
    return value * (Decimal("1") + shock)


def _get_shock_for_asset_type(
    asset_type_shocks: dict[str, Decimal],
    asset_type: str,
) -> Decimal:
    return asset_type_shocks.get(asset_type.lower(), Decimal("0"))


def run_stress_scenario(
    db: Session,
    book_id: UUID,
    request: StressScenarioRequest,
) -> StressScenarioResponse:
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    loans = db.query(Loan).filter(Loan.book_id == book_id).all()
    positions = db.query(Position).filter(Position.book_id == book_id).all()

    loan_ids = [loan.id for loan in loans]

    if loan_ids:
        collateral_items = (
            db.query(Collateral)
            .filter(Collateral.loan_id.in_(loan_ids))
            .all()
        )
    else:
        collateral_items = []

    normalized_shocks = {
        asset_type.lower(): shock
        for asset_type, shock in request.asset_type_shocks.items()
    }

    total_loan_exposure = sum(
        (loan.amount for loan in loans),
        Decimal("0"),
    )

    base_total_collateral_market_value = sum(
        (collateral.market_value for collateral in collateral_items),
        Decimal("0"),
    )

    base_total_eligible_collateral_value = sum(
        (
            collateral.market_value * (Decimal("1") - collateral.haircut_percentage)
            for collateral in collateral_items
        ),
        Decimal("0"),
    )

    stressed_total_collateral_market_value = sum(
        (
            _apply_shock(
                collateral.market_value,
                _get_shock_for_asset_type(normalized_shocks, collateral.asset_type),
            )
            for collateral in collateral_items
        ),
        Decimal("0"),
    )

    stressed_total_eligible_collateral_value = sum(
        (
            _apply_shock(
                collateral.market_value,
                _get_shock_for_asset_type(normalized_shocks, collateral.asset_type),
            )
            * (Decimal("1") - collateral.haircut_percentage)
            for collateral in collateral_items
        ),
        Decimal("0"),
    )

    base_total_position_market_value = sum(
        (
            position.quantity * position.market_price
            for position in positions
        ),
        Decimal("0"),
    )

    stressed_total_position_market_value = sum(
        (
            position.quantity
            * _apply_shock(
                position.market_price,
                _get_shock_for_asset_type(normalized_shocks, position.asset_type),
            )
            for position in positions
        ),
        Decimal("0"),
    )

    if total_loan_exposure == 0 or base_total_eligible_collateral_value == 0:
        base_weighted_ltv = None
    else:
        base_weighted_ltv = _ratio(
            total_loan_exposure / base_total_eligible_collateral_value
        )

    if total_loan_exposure == 0 or stressed_total_eligible_collateral_value == 0:
        stressed_weighted_ltv = None
    else:
        stressed_weighted_ltv = _ratio(
            total_loan_exposure / stressed_total_eligible_collateral_value
        )

    return StressScenarioResponse(
        book_id=book.id,
        scenario_name=request.scenario_name,
        base_total_loan_exposure=_money(total_loan_exposure),
        base_total_collateral_market_value=_money(base_total_collateral_market_value),
        base_total_eligible_collateral_value=_money(base_total_eligible_collateral_value),
        base_weighted_ltv=base_weighted_ltv,
        base_risk_status=_risk_status(base_weighted_ltv),
        stressed_total_collateral_market_value=_money(
            stressed_total_collateral_market_value
        ),
        stressed_total_eligible_collateral_value=_money(
            stressed_total_eligible_collateral_value
        ),
        stressed_weighted_ltv=stressed_weighted_ltv,
        stressed_risk_status=_risk_status(stressed_weighted_ltv),
        base_total_position_market_value=_money(base_total_position_market_value),
        stressed_total_position_market_value=_money(
            stressed_total_position_market_value
        ),
    )
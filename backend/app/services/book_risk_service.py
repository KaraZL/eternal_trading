from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.collateral import Collateral
from app.models.loan import Loan
from app.models.position import Position
from app.models.trade_order import TradeOrder
from app.schemas.book_risk import BookRiskResponse


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


def get_book_risk_summary(
    db: Session,
    book_id: UUID,
) -> BookRiskResponse:
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

    pending_trade_order_count = (
        db.query(TradeOrder)
        .filter(
            TradeOrder.book_id == book_id,
            TradeOrder.status == "pending",
        )
        .count()
    )

    executed_trade_order_count = (
        db.query(TradeOrder)
        .filter(
            TradeOrder.book_id == book_id,
            TradeOrder.status == "executed",
        )
        .count()
    )

    total_loan_exposure = sum(
        (loan.amount for loan in loans),
        Decimal("0"),
    )

    total_collateral_market_value = sum(
        (collateral.market_value for collateral in collateral_items),
        Decimal("0"),
    )

    total_eligible_collateral_value = sum(
        (
            collateral.market_value * (Decimal("1") - collateral.haircut)
            for collateral in collateral_items
        ),
        Decimal("0"),
    )

    total_position_market_value = sum(
        (
            position.quantity * position.market_price
            for position in positions
        ),
        Decimal("0"),
    )

    if total_loan_exposure == 0 or total_eligible_collateral_value == 0:
        weighted_ltv = None
    else:
        weighted_ltv = _ratio(total_loan_exposure / total_eligible_collateral_value)

    return BookRiskResponse(
        book_id=book.id,
        book_name=book.name,
        currency=book.currency,
        loan_count=len(loans),
        position_count=len(positions),
        pending_trade_order_count=pending_trade_order_count,
        executed_trade_order_count=executed_trade_order_count,
        total_loan_exposure=_money(total_loan_exposure),
        total_collateral_market_value=_money(total_collateral_market_value),
        total_eligible_collateral_value=_money(total_eligible_collateral_value),
        weighted_ltv=weighted_ltv,
        total_position_market_value=_money(total_position_market_value),
        risk_status=_risk_status(weighted_ltv),
    )
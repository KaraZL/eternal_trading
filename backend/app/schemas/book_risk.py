from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BookRiskResponse(BaseModel):
    book_id: UUID
    currency: str
    loan_count: int
    position_count: int
    pending_trade_order_count: int
    executed_trade_order_count: int
    total_loan_exposure: str
    total_collateral_market_value: Decimal
    total_eligible_collateral_value: Decimal
    weighted_ltv: Decimal | None
    '''
    Because a book may have no collateral or no loans. In that case, there is no meaningful LTV.
    '''
    total_position_market_value: Decimal
    risk_status: str

    model_config = ConfigDict(from_attributes=True)
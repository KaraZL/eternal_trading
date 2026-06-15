from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class ScenarioRunResponse(BaseModel):
    id: UUID
    book_id: UUID
    scenario_name: str
    asset_type_shocks: dict[str, Decimal]
    created_at: datetime

    base_total_loan_exposure: Decimal
    base_total_collateral_market_value: Decimal
    base_total_eligible_collateral_value: Decimal
    base_weighted_ltv: Decimal | None
    base_risk_status: str

    stressed_total_collateral_market_value: Decimal
    stressed_total_eligible_collateral_value: Decimal
    stressed_weighted_ltv: Decimal | None
    stressed_risk_status: str

    base_total_position_market_value: Decimal
    stressed_total_position_market_value: Decimal

    model_config = ConfigDict(from_attributes=True)
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StressScenarioRequest(BaseModel):
    scenario_name: str = Field(..., min_length=1)
    asset_type_shocks: dict[str, Decimal] = Field(
        ...,
        description="Mapping of asset_type to shock percentage. Example: equity=-0.20",
    )


class StressScenarioResponse(BaseModel):
    book_id: UUID
    scenario_name: str

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
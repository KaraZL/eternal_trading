from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.scenario_run import ScenarioRun
from app.schemas.scenario import StressScenarioRequest
from app.schemas.scenario_run import ScenarioRunResponse
from app.services.scenario_service import run_stress_scenario

def _json_safe_shocks(asset_type_shocks: dict[str, Decimal]) -> dict[str, str]:
    return {
        asset_type: str(shock)
        for asset_type, shock in asset_type_shocks.items()
    }

def run_and_persist_stress_scenario(
    db: Session,
    book_id: UUID,
    request: StressScenarioRequest,
) -> ScenarioRunResponse:
    result = run_stress_scenario(db, book_id, request)

    scenario_run = ScenarioRun(
        book_id=result.book_id,
        scenario_name=result.scenario_name,
        asset_type_shocks=_json_safe_shocks(request.asset_type_shocks),
        created_at=datetime.now(timezone.utc),

        base_total_loan_exposure=result.base_total_loan_exposure,
        base_total_collateral_market_value=result.base_total_collateral_market_value,
        base_total_eligible_collateral_value=result.base_total_eligible_collateral_value,
        base_weighted_ltv=result.base_weighted_ltv,
        base_risk_status=result.base_risk_status,

        stressed_total_collateral_market_value=result.stressed_total_collateral_market_value,
        stressed_total_eligible_collateral_value=result.stressed_total_eligible_collateral_value,
        stressed_weighted_ltv=result.stressed_weighted_ltv,
        stressed_risk_status=result.stressed_risk_status,

        base_total_position_market_value=result.base_total_position_market_value,
        stressed_total_position_market_value=result.stressed_total_position_market_value,
    )

    db.add(scenario_run)
    db.commit()
    db.refresh(scenario_run)

    return ScenarioRunResponse.model_validate(scenario_run)


def list_scenario_runs_by_book(book_id: UUID, db: Session) -> ScenarioRunResponse | None:
    scenario_runs = db.query(ScenarioRun).filter(ScenarioRun.book_id == book_id).all()
    return [
        ScenarioRunResponse.model_validate(scenario_run)
        for scenario_run in scenario_runs
    ]

def get_scenario_run(
    db: Session,
    scenario_run_id: UUID,
) -> ScenarioRunResponse | None:
    scenario_run = (
        db.query(ScenarioRun)
        .filter(ScenarioRun.id == scenario_run_id)
        .first()
    )

    if scenario_run is None:
        return None

    return ScenarioRunResponse.model_validate(scenario_run)
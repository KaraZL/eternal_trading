from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.scenario import StressScenarioRequest, StressScenarioResponse
from app.schemas.scenario_run import ScenarioRunResponse
from app.services.scenario_service import run_stress_scenario
from app.services.scenario_run_service import (
    run_and_persist_stress_scenario, 
    list_scenario_runs_by_book, 
    get_scenario_run
)


router = APIRouter()


@router.post(
    "/books/{book_id}/stress",
    response_model=StressScenarioResponse,
)
async def run_book_stress_scenario_route(
    book_id: UUID,
    request: StressScenarioRequest,
    db: Session = Depends(get_db),
) -> StressScenarioResponse:
    return run_stress_scenario(db, book_id, request)

@router.post(
    "/books/{book_id}/stress-runs",
    response_model=ScenarioRunResponse
)
async def run_and_persist_book_stress_scenario_route(
    book_id: UUID,
    request: StressScenarioRequest,
    db: Session = Depends(get_db)
) -> ScenarioRunResponse:
    return run_and_persist_stress_scenario(db, book_id, request)

@router.get(
    "/books/{book_id}/runs",
    response_model=list[ScenarioRunResponse],
)
async def list_book_scenario_runs_route(
    book_id: UUID,
    db: Session = Depends(get_db),
) -> list[ScenarioRunResponse]:
    return list_scenario_runs_by_book(db=db, book_id=book_id)


@router.get(
    "/runs/{scenario_run_id}",
    response_model=ScenarioRunResponse,
)
async def get_scenario_run_route(
    scenario_run_id: UUID,
    db: Session = Depends(get_db),
) -> ScenarioRunResponse:
    scenario_run = get_scenario_run(db, scenario_run_id)

    if scenario_run is None:
        raise HTTPException(status_code=404, detail="Scenario run not found.")

    return scenario_run
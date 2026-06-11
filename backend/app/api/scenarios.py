from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.scenario import StressScenarioRequest, StressScenarioResponse
from app.services.scenario_service import run_stress_scenario


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
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.schemas.position import PositionRequest, PositionResponse
from app.services.position_service import create_position, list_positions, list_positions_by_book
from app.services.book_service import get_book

router = APIRouter()

@router.post("", response_model=PositionResponse)
async def create_position_route(request: PositionRequest, db: Session = Depends(get_db)) -> PositionResponse:
    return create_position(db, request)

@router.get("", response_model=list[PositionResponse])
async def list_positions_router(db: Session = Depends(get_db)) -> list[PositionResponse]:
    return list_positions(db)

@router.get("/{book_id}/positions", response_model=PositionResponse)
async def list_positions_by_book_router(book_id: UUID, db: Session = Depends(get_db)) -> dict:
    db_book = get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    db_positions = list_positions_by_book(db, book_id)
    if not db_positions:
        raise HTTPException(status_code=404, detail="No positions for this book.")
    
    return db_positions
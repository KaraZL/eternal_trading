from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.services.trade_order_service import create_trade_order, list_all_trade_order, list_all_trade_order_by_book, execute_trade_order
from app.schemas.trade_order import TradeOrderRequest, TradeOrderResponse, TradeOrderExecutionRequest
from app.db.database import get_db

from sqlalchemy.orm import Session

from app.services.book_service import get_book


router = APIRouter()

@router.post("", response_model=TradeOrderResponse)
async def create_trade_order_route(trade_order: TradeOrderRequest, db: Session = Depends(get_db)):
    return create_trade_order(db, trade_order)

@router.get("", response_model=list[TradeOrderResponse])
async def list_all_trade_order_route(db: Session = Depends(get_db)):
    return list_all_trade_order(db)

@router.post("/{order_id}/execute", response_model=TradeOrderResponse)
async def create_trade_order_execution_route(order_id: UUID, trade_order_exec: TradeOrderExecutionRequest, db: Session = Depends(get_db)):
    return execute_trade_order(order_id, trade_order_exec, db)

@router.get("/book/{book_id}", response_model=list[TradeOrderResponse])
async def list_trade_orders_by_book_route(
    book_id: UUID,
    db: Session = Depends(get_db),
) -> list[TradeOrderResponse]:
    db_book = get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    return list_all_trade_order_by_book(db, book_id)
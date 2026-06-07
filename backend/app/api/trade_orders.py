from fastapi import APIRouter, Depends

from app.services.trade_order_service import create_trade_order, list_all_trade_order
from app.schemas.trade_order import TradeOrderRequest, TradeOrderResponse
from app.db.database import get_db

from sqlalchemy.orm import Session


router = APIRouter()

@router.post("", response_model=TradeOrderResponse)
async def create_trade_order_route(trade_order: TradeOrderRequest, db: Session = Depends(get_db)):
    return create_trade_order(db, trade_order)

@router.get("", response_model=list[TradeOrderResponse])
async def list_all_trade_order_route(db: Session = Depends(get_db)):
    return list_all_trade_order(db)
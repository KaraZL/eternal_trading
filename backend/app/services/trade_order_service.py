from app.schemas.trade_order import TradeOrderRequest, TradeOrderResponse, TradeOrderExecutionRequest
from app.models.trade_order import TradeOrder
from app.models.position import Position
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from uuid import UUID

def create_trade_order(db: Session, trade_order: TradeOrderRequest) -> TradeOrderResponse:
    db_trade_order = TradeOrder(
        book_id=trade_order.book_id,
        side=trade_order.side,
        asset_type=trade_order.asset_type,
        asset_name=trade_order.asset_name,
        quantity=trade_order.quantity,
        limit_price=trade_order.limit_price,
        currency=trade_order.currency,
        status="pending"
    )
    db.add(db_trade_order)
    db.commit()
    db.refresh(db_trade_order)
    return TradeOrderResponse.model_validate(db_trade_order)

def list_all_trade_order(db: Session) -> list[TradeOrderResponse]:
    db_trade = db.query(TradeOrder).all()
    return [TradeOrderResponse.model_validate(trade) for trade in db_trade]

def list_all_trade_order_by_book(db: Session, book_id: str) -> list[TradeOrderResponse]:
    db_trade = db.query(TradeOrder).filter(TradeOrder.book_id == book_id).all()
    return [TradeOrderResponse.model_validate(trade) for trade in db_trade]

def execute_trade_order(order_id: UUID, trade_order_execution: TradeOrderExecutionRequest, db: Session) -> TradeOrderResponse:
    db_order = db.query(TradeOrder).filter(TradeOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Trade order not found.")
    
    if db_order.status != "pending":
        raise HTTPException(status_code=400, detail=f"The trade order couldn't be executed because the status is : {db_order.status}")
    
    db_position = db.query(Position).filter(Position.book_id == db_order.book_id,
                                            Position.asset_name == db_order.asset_name,
                                            Position.asset_type == db_order.asset_type,
                                            Position.currency == db_order.currency).first()
    
    side = db_order.side.lower()
    
    if side == "buy":
        if db_position is None:
            db_position = Position(
                book_id = db_order.book_id,
                asset_type = db_order.asset_type,
                asset_name = db_order.asset_name,
                quantity = db_order.quantity,
                market_price = trade_order_execution.execution_price,
                currency = db_order.currency
            )
            db.add(db_position)
        else:
            db_position.quantity += db_order.quantity
            db_position.market_price = trade_order_execution.execution_price
    
    elif side == "sell":
        if db_position is None:
            raise HTTPException(status_code=400, detail="Cannot sell because no matching positions exists.")
        
        if db_position.quantity < db_order.quantity:
            raise HTTPException(status_code=400, detail="Cannot sell more than the current position quantity.")
        
        db_position.quantity -= db_order.quantity
        db_position.market_price = trade_order_execution.execution_price

    else:
        raise HTTPException(
            status_code=400,
            detail="Trade order side must be 'buy' or 'sell'."
        )

    db_order.status = "executed"
    db_order.execution_price = trade_order_execution.execution_price
    db_order.executed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_order)

    return TradeOrderResponse.model_validate(db_order)


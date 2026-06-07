from app.schemas.trade_order import TradeOrderRequest, TradeOrderResponse
from app.models.trade_order import TradeOrder
from sqlalchemy.orm import Session

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
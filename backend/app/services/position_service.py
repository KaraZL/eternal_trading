from decimal import Decimal
from app.schemas.position import PositionRequest, PositionResponse
from app.models.position import Position
from sqlalchemy.orm import Session

def create_position(db: Session, position: PositionRequest) -> PositionResponse:
    
    db_position = Position(
        id=None,
        book_id=position.book_id,
        asset_type=position.asset_type,
        asset_name=position.asset_name,
        quantity=position.quantity,
        market_price=position.market_price,
        currency=position.currency
    )

    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return _to_position_response(db_position)

def list_positions(db: Session) -> list[PositionResponse]:

    db_positions = db.query(Position).all()
    return [_to_position_response(pos) for pos in db_positions]

def list_positions_by_book(db: Session, book_id: str) -> list[PositionResponse]:

    db_positions = db.query(Position).filter(Position.book_id == book_id).all()
    return [_to_position_response(pos) for pos in db_positions]

def _to_position_response(position: Position) -> PositionResponse:
    return PositionResponse(
        id=position.id,
        book_id=position.book_id,
        asset_type=position.asset_type,
        asset_name=position.asset_name,
        quantity=position.quantity,
        market_price=position.market_price,
        currency=position.currency,
        market_value=(position.quantity * position.market_price).quantize(Decimal("0.01"))
    )
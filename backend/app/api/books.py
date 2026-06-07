"""Book API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.book import BookRequest, BookResponse
from ..schemas.trade_order import TradeOrderResponse
from ..services.book_service import create_book, get_book, list_books
from ..services.trade_order_service import list_all_trade_order_by_book

router = APIRouter()


@router.post("", response_model=BookResponse)
async def create_book_route(request: BookRequest, db: Session = Depends(get_db)) -> BookResponse:
    """Create a new book."""
    return create_book(db, request)


@router.get("", response_model=list[BookResponse])
async def list_books_route(db: Session = Depends(get_db)) -> list[BookResponse]:
    """List all books."""
    return list_books(db)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book_route(book_id: str, db: Session = Depends(get_db)) -> BookResponse:
    """Get a book by ID."""
    book = get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_id}/trade-orders", response_class=list[TradeOrderResponse])
async def list_trade_orders_by_book_route(book_id: str, db: Session = Depends(get_db)):
    db_trades = list_all_trade_order_by_book(db, book_id)
    if not db_trades:
        raise HTTPException(status_code=404, detail="Traders not found for the given book")
    
    return db_trades

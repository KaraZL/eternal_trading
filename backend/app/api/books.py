"""Book API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.book import BookRequest, BookResponse
from ..services.book_service import create_book, get_book, list_books

router = APIRouter(prefix="/api/books", tags=["books"])


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

"""Book API routes."""

from fastapi import APIRouter

from ..db.store import books, generate_id
from ..schemas.book import BookRequest, BookResponse

router = APIRouter(prefix="/api/books", tags=["books"])


@router.post("", response_model=BookResponse)
async def create_book(request: BookRequest) -> BookResponse:
    """Create a new book."""
    book_id = generate_id("book", books)
    book = {
        "id": book_id,
        "name": request.name,
        "currency": request.currency,
    }
    books[book_id] = book
    return BookResponse(**book)


@router.get("", response_model=list[BookResponse])
async def list_books() -> list[BookResponse]:
    """List all books."""
    return [BookResponse(**book) for book in books.values()]

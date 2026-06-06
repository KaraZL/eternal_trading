from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.db.base import Base

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Provide a database session.
    Generator[YieldType, SendType, ReturnType]

    This function returns a generator that yields Session objects, does not accept values sent into it, and does not return a final value.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
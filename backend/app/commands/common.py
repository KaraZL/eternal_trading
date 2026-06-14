"""
This code creates a safe helper to open and close a SQLAlchemy database session.
It is especially useful for your CLI commands, because FastAPI usually handles DB sessions with Depends(...), but CLI commands need another clean way.
"""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.container import container

@contextmanager
def db_session() -> Iterator[Session]:
    session_factory = container.db_session_factory()
    '''
    This asks the container for the SQLAlchemy session factory.
    does not give you a DB session directly.
    '''

    db = session_factory()
    '''
    session_factory is something that can create sessions.
    This creates the actual SQLAlchemy session.
    This is the object you use to query, insert, update, delete, commit, rollback, etc.
    '''

    try:
        yield db
    finally:
        db.close()
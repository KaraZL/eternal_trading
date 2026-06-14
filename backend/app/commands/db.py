import click
from sqlalchemy import text
"""
text() lets you write raw SQL safely as a SQLAlchemy SQL expression.
"""

from app.commands.common import db_session

@click.group()
def db() -> None:
    """Database utilities"""

@db.command("check")
def check_db() -> None:
    """Check database connectivity."""
    with db_session() as session:
        result = session.execute(text("select 1")).scalar_one()
        """
        Instead of passing a plain string directly to SQLAlchemy.
        In SQLAlchemy 2.x, this is the recommended way when executing raw SQL.
        """

    click.echo(f"Database connection OK: {result}")
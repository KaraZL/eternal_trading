from decimal import Decimal

import click

from app.commands.common import db_session
from app.models.book import Book
from app.models.client import Client
from app.models.collateral import Collateral
from app.models.loan import Loan
from app.models.position import Position
from app.models.trade_order import TradeOrder

@click.group()
def seed() -> None:
    """Seed demo data"""

@seed.command("demo")
def seed_demo() -> None:
    """Create a demi client, book, loan, collateral, position and trade order"""

    with db_session() as db:
        client = Client(
            name="Acme Holding AG",
            country="CH",
            risk_rating="medium",
        )

        book = Book(
            name="Swiss Lombard Lending Book",
            currency="CHF",
        )

        db.add(client)
        db.add(book)
        db.flush()
        """
        Send the pending changes from the SQLAlchemy Session to the database, but do not commit the transaction yet.
        The main reason to use flush() is to get generated values, especially IDs.
        """

        loan = Loan(
            client_id=client.id,
            book_id=book.id,
            amount=Decimal("1000000.00"),
            currency="CHF",
        )

        db.add(loan)
        db.flush()

        collateral = Collateral(
            loan_id=loan.id,
            asset_type="equity",
            asset_name="Nestle shares",
            market_value=Decimal("2000000.00"),
            currency="CHF",
            haircut=Decimal("0.20"),
        )

        position = Position(
            book_id=book.id,
            asset_type="equity",
            asset_name="Nestle shares",
            quantity=Decimal("100"),
            market_price=Decimal("99.50"),
            currency="CHF",
        )

        trade_order = TradeOrder(
            book_id=book.id,
            side="buy",
            asset_type="equity",
            asset_name="Nestle shares",
            quantity=Decimal("100"),
            limit_price=Decimal("98.50"),
            currency="CHF",
            status="pending",
        )

        db.add_all([collateral, position, trade_order])
        db.commit()

        click.echo("Demo data created.")
        click.echo(f"Client ID: {client.id}")
        click.echo(f"Book ID:   {book.id}")
        click.echo(f"Loan ID:   {loan.id}")
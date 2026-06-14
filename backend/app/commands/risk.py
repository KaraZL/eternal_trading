from uuid import UUID

import click

from app.commands.common import db_session
from app.services.book_risk_service import get_book_risk_summary

@click.group()
def risk() -> None:
    """Risk calculation commands"""

@risk.command("book")
@click.argument("book_id")
def risk_book(book_id: str) -> None:
    """Calculate risk summary for a book"""
    with db_session() as db:
        result = get_book_risk_summary(db, UUID(book_id))

        click.echo(f"Book: {result.book_name}")
        click.echo(f"Currency: {result.currency}")
        click.echo(f"Loans: {result.loan_count}")
        click.echo(f"Positions: {result.position_count}")
        click.echo(f"Total loan exposure: {result.total_loan_exposure}")
        click.echo(f"Total eligible collateral: {result.total_eligible_collateral_value}")
        click.echo(f"Weighted LTV: {result.weighted_ltv}")
        click.echo(f"Risk status: {result.risk_status}")
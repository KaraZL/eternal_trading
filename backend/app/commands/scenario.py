from decimal import Decimal
from uuid import UUID

import click

from app.commands.common import db_session
from app.schemas.scenario import StressScenarioRequest
from app.services.scenario_service import run_stress_scenario
from app.services.scenario_run_service import run_and_persist_stress_scenario


@click.group()
def scenario() -> None:
    """Scenario analysis commands."""


@scenario.command("stress")
@click.argument("book_id")
@click.option(
    "--equity-shock",
    default="-0.20",
    show_default=True,
    help="Shock to apply to equity assets. Example: -0.20 means -20%.",
)
@click.option(
    "--bond-shock",
    default="-0.05",
    show_default=True,
    help="Shock to apply to bond assets. Example: -0.05 means -5%.",
)
def stress_book(
    book_id: str,
    equity_shock: str,
    bond_shock: str,
) -> None:
    """Run a simple stress scenario for a book."""
    request = StressScenarioRequest(
        scenario_name="CLI stress scenario",
        asset_type_shocks={
            "equity": Decimal(equity_shock),
            "bond": Decimal(bond_shock),
        },
    )

    with db_session() as db:
        result = run_stress_scenario(db, UUID(book_id), request)

    click.echo(f"Scenario: {result.scenario_name}")
    click.echo(f"Base LTV: {result.base_weighted_ltv}")
    click.echo(f"Base status: {result.base_risk_status}")
    click.echo(f"Stressed LTV: {result.stressed_weighted_ltv}")
    click.echo(f"Stressed status: {result.stressed_risk_status}")
    click.echo(
        f"Stressed eligible collateral: "
        f"{result.stressed_total_eligible_collateral_value}"
    )


@scenario.command("stress-save")
@click.argument("book_id")
@click.option(
    "--equity-shock",
    default="-0.20",
    show_default=True,
    help="Shock to apply to equity assets. Example: -0.20 means -20%.",
)
@click.option(
    "--bond-shock",
    default="-0.05",
    show_default=True,
    help="Shock to apply to bond assets. Example: -0.05 means -5%.",
)
def stress_save_book(
    book_id: str,
    equity_shock: str,
    bond_shock: str,
) -> None:
    request = StressScenarioRequest(
        scenario_name="CLI stress save scenario",
        asset_type_shocks={
            "equity": Decimal(equity_shock),
            "bond": Decimal(bond_shock),
        }
    )

    with db_session() as db:
        result = run_and_persist_stress_scenario(db, UUID(book_id), request)
    
    click.echo(f"Scenario run saved: {result.id}")
    click.echo(f"Book ID: {result.book_id}")
    click.echo(f"Base status: {result.base_risk_status}")
    click.echo(f"Stressed status: {result.stressed_risk_status}")
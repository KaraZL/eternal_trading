import click
"""
click is a Python library for building command-line interfaces.
It lets you create commands such as: python -m app.commands seed
or, if configured through Poetry: poetry run eternal seed
"""

from app.commands.db import db
from app.commands.seed import seed
from app.commands.risk import risk
from app.commands.scenario import scenario

@click.group()
def cli() -> None:
    """AI Lending Platform command line tools"""

cli.add_command(db)
cli.add_command(seed)
cli.add_command(risk)
cli.add_command(scenario)

if __name__ == "__main__":
    cli()
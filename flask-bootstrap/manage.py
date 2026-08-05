"""Flask CLI entry point."""

import click

from app import create_app
from app.commands.init_db import init_db

app = create_app()


@app.cli.command("init-db")
@click.confirmation_option(prompt="Drop and rebuild the local database?")
def init_db_command():
    """Explicitly rebuild and seed the local sample database."""
    init_db()
    click.echo("Initialized the sample database.")

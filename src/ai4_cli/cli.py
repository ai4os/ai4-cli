"""CLI entry point for the AI4 CLI tools."""

import typer

import ai4_cli
from ai4_cli import modules

app = typer.Typer(help="AI4 CLI tools, to interact with an AI4OS (AI4EOSC) platform")
app.add_typer(modules.app, name="modules")


def version_callback(value: bool):
    """Return the version for the --version option."""
    if value:
        typer.echo(ai4_cli.extract_version())
        raise typer.Exit()


@app.callback()
def version(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print the version and exit",
    )
):
    """Show version and exit."""
    pass

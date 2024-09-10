"""CLI entry point for the AI4 CLI tools."""

import dataclasses
from typing_extensions import Annotated
from typing import Optional

import typer

import ai4_cli
from ai4_cli.cli import modules
from ai4_cli.client import client

app = typer.Typer(help="AI4 CLI tools, to interact with an AI4OS (AI4EOSC) platform")
app.add_typer(modules.app, name="modules")


def version_callback(value: bool):
    """Return the version for the --version option."""
    if value:
        typer.echo(ai4_cli.extract_version())
        raise typer.Exit()


@dataclasses.dataclass
class CommonOptions:
    """Dataclass containing common options for the CLI."""

    endpoint: Optional[str]
    api_version: client.APIVersion


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print the version and exit",
    ),
    endpoint: Annotated[
        Optional[str],
        typer.Option(
            "--endpoint",
            "-e",
            help="The endpoint to connect to.",
        ),
    ] = "https://api.cloud.ai4eosc.eu",
    api_version: Annotated[
        client.APIVersion,
        typer.Option(
            "--api-version",
            "-a",
            help="The version of the API to use.",
        ),
    ] = client.APIVersion.v1,
):
    """Implement common options for the CLI."""
    ctx.obj = CommonOptions(endpoint, api_version)

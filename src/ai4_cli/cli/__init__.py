"""CLI entry point for the AI4 CLI tools."""

import dataclasses
import os
from typing_extensions import Annotated
from typing import Optional

import dotenv
import typer

import ai4_cli
from ai4_cli.cli import modules
from ai4_cli.cli import tools
from ai4_cli.client import client

app = typer.Typer(
    help="""AI4 CLI tools, to interact with an AI4OS (AI4EOSC) platform.

The AI4 CLI tools allow you to interact with the AI4EOSC platform, to manage
the modules, tools, and other resources available in the platform.

You need to specify a valid endpoint to connect to the platform. You can do
this by setting the AI4_ENDPOINT environment variable, or by using the
--endpoint option in the commands.

The CLI tools will load the configuration from the .env.ai4 file in the
current directory, if it exists. You can also specify a different file using
the DOTENV_FILE environment variable.
"""
)
app.add_typer(modules.app, name="module")
app.add_typer(tools.app, name="tool")


DOTENV_FILE = os.getenv("AI4_DOTENV_FILE", ".env.ai4")

dotenv.load_dotenv(DOTENV_FILE)


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
    debug: bool


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
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        envvar="AI4_DEBUG",
        help="Enable debugging mode.",
    ),
    endpoint: Annotated[
        Optional[str],
        typer.Option(
            "--endpoint",
            "-e",
            envvar="AI4_API_ENDPOINT",
            help="The endpoint to connect to.",
        ),
    ] = "https://api.cloud.ai4eosc.eu",
    api_version: Annotated[
        client.APIVersion,
        typer.Option(
            "--api-version",
            "-a",
            envvar="AI4_API_VERSION",
            help="The version of the API to use.",
        ),
    ] = client.APIVersion.v1,
):
    """Implement common options for the CLI."""
    ctx.obj = CommonOptions(endpoint, api_version, debug)

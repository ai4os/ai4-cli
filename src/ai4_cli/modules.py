"""Handle CLI commands for modules."""

from typing_extensions import Annotated
from typing import Optional

import typer

from ai4_cli.client import client
from ai4_cli import utils

app = typer.Typer(help="List and get details of the defined modules and tools.")


@app.command(name="list")
def list(
    endpoint: Annotated[
        Optional[str],
        typer.Option(
            "--endpoint",
            "-e",
            help="The endpoint to connect to.",
        ),
    ] = "https://api.cloud.ai4eosc.eu",
    version: Annotated[
        client.APIVersion,
        typer.Option(
            "--api-version",
            "-a",
            help="The version of the API to use.",
        ),
    ] = client.APIVersion.v1,
    long: Annotated[
        bool,
        typer.Option(
            "--long",
            "-l",
            help="Show more details.",
        ),
    ] = False,
):
    """List all modules."""
    cli = client.AI4Client(endpoint, version)
    resp, content = cli.modules.list()

    if long:
        rows = [
            [
                k.get("name"),
                k.get("title"),
                k.get("summary"),
                ", ".join(k.get("keywords")),
            ]
            for k in content
        ]

        columns = ["ID", "Module name", "Summary", "Keywords"]
    else:
        rows = [[k.get("name"), k.get("title"), k.get("summary")] for k in content]
        columns = ["ID", "Module name", "Summary"]

    utils.format_list(
        columns=columns,
        items=rows,
    )

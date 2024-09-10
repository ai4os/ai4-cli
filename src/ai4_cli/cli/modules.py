"""Handle CLI commands for modules."""

from typing_extensions import Annotated

import typer

from ai4_cli.client import client
from ai4_cli import utils

app = typer.Typer(help="List and get details of the defined modules and tools.")


@app.command(name="list")
def list(
    ctx: typer.Context,
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
    endpoint = ctx.obj.endpoint
    version = ctx.obj.api_version

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

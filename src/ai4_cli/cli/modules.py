"""Handle CLI commands for modules."""

from typing_extensions import Annotated

import typer

from ai4_cli.client import client
from ai4_cli import exceptions
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
    debug = ctx.obj.debug

    cli = client.AI4Client(endpoint, version, http_debug=debug)
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


@app.command(name="show")
def show(
    ctx: typer.Context,
    module_id: str = typer.Argument(..., help="The ID of the module to show."),
):
    """Show details of a module."""
    endpoint = ctx.obj.endpoint
    version = ctx.obj.api_version
    debug = ctx.obj.debug

    cli = client.AI4Client(endpoint, version, http_debug=debug)
    try:
        resp, content = cli.modules.show(module_id)
    except exceptions.BaseHTTPError as e:
        utils.format_rich_error(e)
        raise typer.Exit()

    utils.format_dict(content, exclude=["tosca", "continuous_integration"])

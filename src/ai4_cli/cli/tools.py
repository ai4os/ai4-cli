"""Handle CLI commands for tools."""

import enum
from typing_extensions import Annotated
from typing import List, Optional

import typer

from ai4_cli.client import client
from ai4_cli import exceptions
from ai4_cli import utils

app = typer.Typer(help="List and get details of the defined tools.")


class ToolColumns(str, enum.Enum):
    """Columns to show in the list command."""

    ID = "ID"
    NAME = "Tool name"
    SUMMARY = "Summary"
    KEYWORDS = "Keywords"


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
    sort: Annotated[
        ToolColumns,
        typer.Option(
            "--sort",
            help="Sort the tools by the given field.",
        ),
    ] = ToolColumns.ID,
    tags: Annotated[
        Optional[List[str]],
        typer.Option(
            "--tags",
            help="Filter tools by tags. The given tags must all be present on a "
            "module to be included in the results. Boolean expression is "
            "t1 AND t2.",
        ),
    ] = None,
    not_tags: Annotated[
        Optional[List[str]],
        typer.Option(
            "--not-tags",
            help="Filter tools by tags. Only the tools that do not have any of the "
            "given tags will be included in the results. Boolean expression is "
            "NOT (t1 AND t2).",
        ),
    ] = None,
    tags_any: Annotated[
        Optional[List[str]],
        typer.Option(
            "--tags-any",
            help="Filter tools by tags. If any of the given tags is present on a "
            "module it will be included in the results. Boolean expression is "
            "t1 OR t2.",
        ),
    ] = None,
    not_tags_any: Annotated[
        Optional[List[str]],
        typer.Option(
            "--not-tags-any",
            help="Filter tools by tags. Only the tools that do not have at least "
            "any of the given tags will be included in the results. "
            "Boolean expression is "
            "NOT (t1 OR t2).",
        ),
    ] = None,
):
    """List all tools."""
    endpoint = ctx.obj.endpoint
    version = ctx.obj.api_version
    debug = ctx.obj.debug

    cli = client.AI4Client(endpoint, version, http_debug=debug)
    filters = {
        "tags": tags,
        "not_tags": not_tags,
        "tags_any": tags_any,
        "not_tags_any": not_tags_any,
    }
    _, content = cli.tools.list(filters=filters)

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

        columns = [
            ToolColumns.ID,
            ToolColumns.NAME,
            ToolColumns.SUMMARY,
            ToolColumns.KEYWORDS,
        ]
    else:
        rows = [[k.get("name"), k.get("title"), k.get("summary")] for k in content]
        columns = [
            ToolColumns.ID,
            ToolColumns.NAME,
            ToolColumns.SUMMARY,
        ]

    try:
        idx = columns.index(sort)
    except ValueError:
        e = exceptions.InvalidUsageError(f"Invalid column to sort by: {sort}")
        utils.format_rich_error(e)
        raise typer.Exit()

    sorted_rows = sorted(rows, key=lambda x: x[idx])
    utils.format_list(
        columns=columns,
        items=sorted_rows,
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
        _, content = cli.tools.show(module_id)
    except exceptions.BaseHTTPError as e:
        utils.format_rich_error(e)
        raise typer.Exit()

    utils.format_dict(content, exclude=["tosca", "continuous_integration"])

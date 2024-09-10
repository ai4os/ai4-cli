"""Utilities for the AI4 CLI."""

import os
from typing import Any, List, Literal, Optional, Union

import rich.panel

from ai4_cli import exceptions

# TODO(aloga): Move all this code to a standalone library

_TERMINAL_WIDTH = os.getenv("TERMINAL_WIDTH")
MAX_WIDTH = int(_TERMINAL_WIDTH) if _TERMINAL_WIDTH else None
ALIGN_ERRORS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_ERRORS_PANEL_BORDER = "bold red"
ALIGN_WARNING_PANEL: Literal["left", "center", "right"] = "left"
STYLE_WARNING_PANEL_BORDER = "bold yellow"
ALIGN_OK_PANEL: Literal["left", "center", "right"] = "left"
STYLE_OK_PANEL_BORDER = "bold green"
STYLE_TABLE_BORDER = "bold blue"


def _get_rich_console(stderr: bool = False) -> rich.console.Console:
    return rich.console.Console(
        width=MAX_WIDTH,
        stderr=stderr,
    )


def format_rich_error(error: exceptions.BaseError) -> None:
    """Format an error using rich."""
    console = _get_rich_console(stderr=True)
    console.print(
        rich.panel.Panel(
            f"{error}",
            title="Error",
            highlight=True,
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title_align=ALIGN_ERRORS_PANEL,
        )
    )


def format_rich_warning(error: Union[str, Exception]) -> None:
    """Format a warning using rich."""
    console = _get_rich_console(stderr=True)
    console.print(
        rich.panel.Panel(
            f"{error}",
            title="Warning",
            highlight=True,
            border_style=STYLE_WARNING_PANEL_BORDER,
            title_align=ALIGN_WARNING_PANEL,
        )
    )


def format_rich_ok(message: str) -> None:
    """Format a message using rich."""
    console = _get_rich_console(stderr=False)
    console.print(
        rich.panel.Panel(
            f"{message}",
            title="Success",
            highlight=True,
            border_style=STYLE_OK_PANEL_BORDER,
            title_align=ALIGN_OK_PANEL,
        )
    )


def format_list(
    columns: List[Any],
    items: Union[List[str], List[List[str]]],
) -> None:
    """Format a list of items using rich."""
    table = rich.table.Table(
        border_style=STYLE_TABLE_BORDER,
        highlight=True,
    )

    for column in columns:
        table.add_column(column)

    if not isinstance(items, list):
        items = [items]
    for row in items:
        table.add_row(*row)

    console = _get_rich_console(stderr=False)
    console.print(table)


def format_dict(
    dictionary: dict,
    exclude: Optional[List[str]] = None,
) -> None:
    """Format a dictionary using rich."""
    table = rich.table.Table(
        border_style=STYLE_TABLE_BORDER,
        highlight=True,
    )

    table.add_column("Key")
    table.add_column("Value")

    for key, value in dictionary.items():
        if exclude and key in exclude:
            continue

        if isinstance(value, list):
            value = ", ".join(value)

        if isinstance(value, dict):
            table.add_section()
            value = "\n".join([f"{k}: {v}" for k, v in value.items()])

        table.add_row(key, value)

    console = _get_rich_console(stderr=False)
    console.print(table)

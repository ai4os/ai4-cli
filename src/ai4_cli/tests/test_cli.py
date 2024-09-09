"""Clients for the CLI and Typer."""

import typer.testing

import ai4_cli
from ai4_cli import cli


def test_version():
    """Test that version is eager."""
    result = typer.testing.CliRunner().invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert ai4_cli.extract_version() in result.output

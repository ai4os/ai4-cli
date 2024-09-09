"""Clients for the CLI and Typer."""

import typer.testing

import ai4_cli
from ai4_cli import cli


def test_version():
    """Test that version is eager."""
    result = typer.testing.CliRunner().invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert ai4_cli.extract_version() in result.output


def test_modules_command():
    """Test that the modules command is available."""
    result = typer.testing.CliRunner().invoke(cli.app, ["modules", "--help"])
    assert result.exit_code == 0
    assert "List and get details of the defined modules and tools." in result.output


def test_modules_list_and_wrong_api_version():
    """Test that the modules list command fails with an invalid API version."""
    result = typer.testing.CliRunner().invoke(
        cli.app, ["modules", "list", "--api-version", "v2"]
    )
    assert result.exit_code == 2
    assert "Invalid value for '--api-version'" in result.output

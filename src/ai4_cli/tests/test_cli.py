"""Clients for the CLI and Typer."""

import typer.testing

import ai4_cli
from ai4_cli import cli


def test_version():
    """Test that version is eager."""
    result = typer.testing.CliRunner().invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert ai4_cli.extract_version() in result.output


def test_module_command():
    """Test that the modules command is available."""
    result = typer.testing.CliRunner().invoke(cli.app, ["module", "--help"])
    assert result.exit_code == 0
    assert "List and get details of the defined modules." in result.output


def test_module_list_and_wrong_api_version():
    """Test that the modules list command fails with an invalid API version."""
    result = typer.testing.CliRunner().invoke(
        cli.app, ["--api-version", "v2", "module", "list"]
    )
    assert result.exit_code == 2
    assert "Invalid value for '--api-version'" in result.output


def test_tool_command():
    """Test that the tools command is available."""
    result = typer.testing.CliRunner().invoke(cli.app, ["tool", "--help"])
    assert result.exit_code == 0
    assert "List and get details of the defined tools." in result.output


def test_tool_list_and_wrong_api_version():
    """Test that the tools list command fails with an invalid API version."""
    result = typer.testing.CliRunner().invoke(
        cli.app, ["--api-version", "v2", "tool", "list"]
    )
    assert result.exit_code == 2
    assert "Invalid value for '--api-version'" in result.output

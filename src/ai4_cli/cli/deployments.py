"""Module for deployments commands."""

import enum
import functools
from typing_extensions import Annotated
from typing import List, Optional

import typer

from ai4_cli.client import client
from ai4_cli import exceptions
from ai4_cli import oidc
from ai4_cli import utils


app = typer.Typer(
    help="""List and get details of your deployments.

This command is authenticated, and requires the OIDC agent to be running.
"""
)


def authenticated(f):
    """Ensure the we have authentication before calling the client.

    This decorator will check if the user has passed the oidc options to the
    CLI, and if not, it will raise an error. If they are present, it will create an
    oidc.OpenIDConnectAgent object and store it in the context object.
    """
    @functools.wraps(f)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        """Check if the user is authenticated."""
        if not (ctx.obj.oidc_sock and ctx.obj.oidc_account):
            utils.format_rich_error(
                "OIDC agent authentication not setup. Please run "
                "`ai4-cli --help` for more information."
            )
            raise typer.Abort()

        agent = oidc.OpenIDConnectAgent(
            ctx.obj.oidc_account, socket_path=ctx.obj.oidc_sock
        )
        ctx.obj.oidc_agent = agent
        return f(ctx, *args, **kwargs)

    return wrapper


class DeploymentColumns(str, enum.Enum):
    """Columns for the deployments list command."""

    ID = "ID"
    TITLE = "Deployment Title"
    STATUS = "Status"
    SUBMISSION = "Submission time"
    RESOURCES = "Resources requested"
    ENDPOINTS = "Endpoints"


@app.command(name="list")
@authenticated
def list_deployments(
    ctx: typer.Context,
    long: bool = typer.Option(
        False,
        "--long",
        "-l",
        help="Show more details.",
    ),
    sort: DeploymentColumns = typer.Option(
        DeploymentColumns.ID,
        "--sort",
        help="Sort the deployments by the given field.",
    ),
    vos: Annotated[
        Optional[List[str]],
        typer.Option(
            "--vo",
            help="Filter deployments by the given VOs.",
        ),
    ] = None,
):
    """List all deployments."""
    endpoint = ctx.obj.endpoint
    version = ctx.obj.api_version
    debug = ctx.obj.debug
    oidc_agent = ctx.obj.oidc_agent

    cli = client.AI4Client(endpoint, version, http_debug=debug, oidc_agent=oidc_agent)

    filters = {}
    if vos:
        filters["vos"] = vos

    try:
        _, content = cli.deployments.list(filters=filters)
    except exceptions.BaseHTTPError as e:
        utils.format_rich_error(e)
        raise typer.Exit()

    if long:
        rows = [
            [
                k["job_ID"],
                k["title"],
                k["status"],
                k["submit_time"],
                "\n".join([f"{i}: {j}" for i, j in k["resources"].items()]),
                "\n".join([f"{i}: {j}" for i, j in k["endpoints"].items()]),
            ]
            for k in content
        ]
        columns = [
            DeploymentColumns.ID,
            DeploymentColumns.TITLE,
            DeploymentColumns.STATUS,
            DeploymentColumns.SUBMISSION,
            DeploymentColumns.RESOURCES,
            DeploymentColumns.ENDPOINTS,
        ]
    else:
        rows = [
            [
                k["job_ID"],
                k["title"],
                k["status"],
                k["submit_time"],
            ]
            for k in content
        ]
        columns = [
            DeploymentColumns.ID,
            DeploymentColumns.TITLE,
            DeploymentColumns.STATUS,
            DeploymentColumns.SUBMISSION,
        ]
    utils.format_list(
        columns=columns,
        items=rows,
    )

import getpass
from types import SimpleNamespace

import click
from click.testing import CliRunner

from chpass.config import (
    DEFAULT_CHROME_PROFILE,
    DEFAULT_EXPORT_DESTINATION_FOLDER,
    DEFAULT_FILE_ADAPTER,
)


@click.group()
@click.option("-u", "--user", default=getpass.getuser(), type=str)
@click.option("-i", "--file-adapter", default=DEFAULT_FILE_ADAPTER, type=str)
@click.option("-p", "--profile", default=DEFAULT_CHROME_PROFILE, type=str)
@click.pass_context
def cli(ctx: click.Context, user: str, file_adapter: str, profile: str) -> None:
    """Gather information from chrome."""
    ctx.ensure_object(dict)
    ctx.obj.update({
        "user": user,
        "file_adapter": file_adapter,
        "profile": profile,
    })


@cli.command(name="import")
@click.option(
    "-f",
    "--from",
    "from_file",
    required=True,
    type=str,
    help="credentials file to import from",
)
@click.pass_context
def import_cmd(ctx: click.Context, from_file: str) -> SimpleNamespace:
    """imports a file with the passwords"""
    ctx.obj.update({"mode": "import", "from_file": from_file})
    return SimpleNamespace(**ctx.obj)


@cli.group(invoke_without_command=True)
@click.option(
    "-d",
    "--destination",
    "destination_folder",
    default=DEFAULT_EXPORT_DESTINATION_FOLDER,
    type=str,
    help="destination folder to export the files",
)
@click.pass_context
def export(ctx: click.Context, destination_folder: str) -> SimpleNamespace | None:
    """exports a chrome data files"""
    ctx.obj.update(
        {
            "mode": "export",
            "destination_folder": destination_folder,
            "export_kind": None,
        }
    )
    if ctx.invoked_subcommand is None:
        return SimpleNamespace(**ctx.obj)
    return None


@export.command("passwords")
@click.pass_context
def export_passwords(ctx: click.Context) -> SimpleNamespace:
    ctx.obj.update({"export_kind": "passwords"})
    return SimpleNamespace(**ctx.obj)


@export.command("history")
@click.pass_context
def export_history(ctx: click.Context) -> SimpleNamespace:
    ctx.obj.update({"export_kind": "history"})
    return SimpleNamespace(**ctx.obj)


@export.command("downloads")
@click.pass_context
def export_downloads(ctx: click.Context) -> SimpleNamespace:
    ctx.obj.update({"export_kind": "downloads"})
    return SimpleNamespace(**ctx.obj)


@export.command("top_sites")
@click.pass_context
def export_top_sites(ctx: click.Context) -> SimpleNamespace:
    ctx.obj.update({"export_kind": "top_sites"})
    return SimpleNamespace(**ctx.obj)


@export.command("profile_pic")
@click.pass_context
def export_profile_pic(ctx: click.Context) -> SimpleNamespace:
    ctx.obj.update({"export_kind": "profile_pic"})
    return SimpleNamespace(**ctx.obj)


@cli.command("list-profiles")
@click.pass_context
def list_profiles(ctx: click.Context) -> SimpleNamespace:
    ctx.obj.update({"mode": "list-profiles"})
    return SimpleNamespace(**ctx.obj)


def parse_args(args: list[str]) -> SimpleNamespace:
    runner = CliRunner()
    result = runner.invoke(cli, args, standalone_mode=False)
    if result.exception:
        raise result.exception
    return result.return_value

from typing import final

import click
from initialise_git import get_all_licences

# https://stackoverflow.com/questions/59733806/python-click-group-how-to-have-h-help-for-all-commands
CONTEXT_SETTINGS: final = dict(help_option_names=["-h", "--help"])

all_licences = get_all_licences()
all_licences = [licence["key"] for licence in all_licences]


@click.group()
@click.help_option("--help", "-h")
def cli():
    """
    Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual environment.
    """
    pass


@cli.command(short_help="Create a new Python project with virtual environment.")
@click.argument("project_name")
@click.option(
    "--venv-name",
    help="What to name the virtual environment. If 'None', disables environment creation.",
    default=".venv",
    show_default=True,
)
@click.option(
    "--spec",
    help="The version specifier to be used in the requirements file.",
    type=click.Choice(["<", "<=", "!=", "==", ">=", ">", "~=", "==="]),
    default="==",
    show_default=True,
)
@click.option(
    "--dependencies",
    "-d",
    help="Packages to install in the virtual environment (if any).",
    multiple=True,
)
def new(*args, **kwargs) -> None:
    click.echo("Hello world!")
    click.echo(args)
    click.echo(kwargs)


@cli.command(
    short_help="Open a project in your editor of choice. Supported: VS Code, PyCharm, IDLE, Notepad, and Notepad++."
)
@click.argument("project_path")
@click.argument("editor")
def start() -> None:
    click.echo("Second command")


@cli.command(
    short_help="Create a Git repository and initialises it with a gitignore and licence. Must have Git installed."
)
@click.argument("project_path")
@click.option(
    "--licence",
    help="The licence to be added to the Git repository.",
    type=click.Choice(all_licences),
    default="gpl-3.0",
    show_default=True,
)
def git() -> None:
    click.echo("Third command")


if __name__ == "__main__":
    cli()

from platform import python_version
from typing import final

import click

from rollout.__init__ import __version__
from rollout.initialise_git import get_all_licences

# https://stackoverflow.com/questions/59733806/python-click-group-how-to-have-h-help-for-all-commands
CONTEXT_SETTINGS: final = dict(help_option_names=["-h", "--help"])

all_licences = get_all_licences()
all_licences = [licence["key"] for licence in all_licences]


@click.group(context_settings=CONTEXT_SETTINGS)
@click.help_option("--help", "-h")
@click.version_option(
    __version__,
    message=f"%(prog)s v%(version)s, running via Python v{python_version()} and click v{click.__version__}",
)
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
def start(*args, **kwargs) -> None:
    click.echo("Second command")
    click.echo(args)
    click.echo(kwargs)


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
@click.option(
    "--desktop",
    help="If specified, opens the project in GitHub Desktop instead of directly using Git. If specified, licence is ignored (because you set that up in the program).",
    is_flag=True,
    default=False,
    show_default=False,
)
def git(*args, **kwargs) -> None:
    click.echo("Third command")
    click.echo(args)
    click.echo(kwargs)


if __name__ == "__main__":
    cli()

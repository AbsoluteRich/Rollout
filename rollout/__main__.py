import os
from pathlib import Path
from platform import python_version
from typing import final

import click
from halo import Halo

from rollout import commands, common, initialise_git, new_project
from rollout.__init__ import __version__

# https://stackoverflow.com/questions/59733806/python-click-group-how-to-have-h-help-for-all-commands
CONTEXT_SETTINGS: final = dict(help_option_names=["-h", "--help"])

all_licences = initialise_git.get_all_licences()
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
    "version_specifier",
    help="The version specifier to be used in the requirements file.",
    type=click.Choice(["<", "<=", "!=", "==", ">=", ">", "~=", "==="]),
    default="==",
    show_default=True,
)
@click.option(
    "--dependencies",
    "-d",
    "packages",
    help="Packages to install in the virtual environment (if any).",
    multiple=True,
)
@click.option(
    "--no-import",
    "do_not_import",
    help="Do not automatically import packages. Useful if the package's name in PyPI differs from the name you use in code.",
    is_flag=True,
    default=False,
    show_default=False,
)
def new(
    project_name: str,
    venv_name: str,
    packages: list[str] | None,
    version_specifier: str,
    do_not_import: bool,
) -> None:
    project_path = Path(project_name)
    venv_name = None if venv_name == "None" else venv_name
    if (not venv_name) and packages:
        click.echo(
            "Packages will be ignored, as there is no virtual environment to install them to."
        )

    with Halo("Creating project folders...", spinner="dots").start() as spin:
        success = new_project.create_project_folders(project_name)
        if success:
            spin.succeed(spin.text + " Done!")
        else:
            spin.fail(
                spin.text + " Folder already exists. Try renaming or deleting it."
            )
            return

    with Halo("Creating entrypoint...", spinner="dots").start() as spin:
        new_project.create_entrypoint(project_name, packages, do_not_import)
        spin.succeed(spin.text + " Done!")

    if venv_name:
        with Halo("Setting up virtual environment...", spinner="dots").start() as spin:
            commands.venv(project_path / venv_name)
            spin.succeed(spin.text + " Done!")

    if packages and venv_name:
        pip_executable = project_path / venv_name / "Scripts" / "pip.exe"

        for package in packages:
            with Halo(
                f"Installing {package} in {venv_name}...", spinner="dots"
            ).start() as spin:
                with open(project_path / "pip-log.txt", "a") as f:
                    commands.pip_install(
                        pip_executable, package, stdout=f, stderr=f, text=True
                    )
                spin.succeed(spin.text + " Done!")

        with Halo("Creating requirements file...", spinner="dots").start() as spin:
            with open(project_path / "requirements.txt", "w") as f:
                commands.pip_freeze(pip_executable, stdout=f, stderr=f, text=True)

            if version_specifier != "==":
                with open(project_path / "requirements.txt", "r") as f:
                    contents = f.read()

                contents = contents.replace("==", version_specifier)

                with open(project_path / "requirements.txt", "w") as f:
                    f.write(contents)

            spin.succeed(spin.text + " Done!")

    click.echo(f"Your new project can be found at {Path.cwd() / project_name}")
    if packages:
        click.echo(
            "If you don't need to see the output for the commands, you can delete 'pip-log.txt'."
        )
    click.echo(
        f"Now that you've created {project_name}, you might like to set it up with Git by using 'rollout git' or "
        f"begin coding using 'rollout start'."
    )


@cli.command(
    short_help="Open a project in your editor of choice. Supported: VS Code, PyCharm, IDLE, Notepad, and Notepad++."
)
@click.argument("project_path")
@click.argument("editor")
def start(project_path: str, editor: str) -> None:
    is_project, file_path = common.check_project(project_path)

    if is_project:
        project_path = os.path.split(file_path)[0]

        match editor:
            case "vsc":
                # Todo
                commands.vsc(project_path)

            case "pycharm":
                # Todo
                commands.pycharm(project_path)

            case "idle":
                commands.idle(file_path)

            case "notepad":
                commands.notepad(file_path)

            case "notepad++":
                # Todo
                commands.notepadplusplus(file_path)
    else:
        click.echo("Invalid project path!")


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
    help="If specified, opens the project in GitHub Desktop instead of directly using Git. If specified, licence is "
    "ignored (because you set that up in the program).",
    is_flag=True,
    default=False,
    show_default=False,
)
def git(project_path: str, licence: str, desktop: bool) -> None:
    is_project, _ = common.check_project(project_path)

    if is_project:
        if desktop:
            commands.github_desktop(project_path)
        else:
            project_path = Path(project_path)
            commands.git_init(project_path)

            with Halo("Creating gitignore...", spinner="dots").start() as spin:
                with open(project_path / ".gitignore", "w") as f:
                    f.write(initialise_git.get_gitignore("Python"))
                spin.succeed(spin.text + " Done!")

            with Halo("Creating licence...", spinner="dots").start() as spin:
                with open(project_path / "LICENSE", "w") as f:
                    f.write(initialise_git.get_licence(licence))
                spin.succeed(spin.text + " Done!")
    else:
        click.echo("Invalid project path!")


if __name__ == "__main__":
    cli()

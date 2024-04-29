import click


@click.group()
@click.help_option("--help", "-h")
def cli():
    """
    Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual environment.
    """
    pass


@cli.command(short_help="Create a new Python project with virtual environment.")
@click.argument("project_name")
@click.option("--venv-name")
@click.option("--spec")
@click.option("--dependencies", "-d")
def new() -> None:
    click.echo("Hello world!")


@cli.command(short_help="Open a project in your editor of choice.")
def start() -> None:
    click.echo("Second command")


@cli.command(
    short_help="Create a Git repository and initialises it with a gitignore and licence. Must have Git installed."
)
def git() -> None:
    click.echo("Third command")


if __name__ == "__main__":
    cli()

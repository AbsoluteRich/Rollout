from pathlib import Path

from invoke import task
from invoke.context import Context

from rollout.__init__ import __version__ as current_version


@task
def reformat(ctx: Context) -> None:
    for command in [
        "python -m black tasks.py",
        "python -m black rollout",
        "python -m isort rollout --profile black",
    ]:
        ctx.run(command)


@task
def update_dependencies(ctx: Context) -> None:
    ctx.run("pipenv update")


@task
def bump(_: Context, label: str | None = None) -> None:
    version_file = Path.cwd() / "rollout" / "__init__.py"

    match label:
        case "major":
            location = 0
        case "minor":
            location = 1
        case "patch":
            location = 2
        case _:
            label = input("Type in a valid semver label (Enter to cancel): ")
            if not label:
                print("Cancelled!")
                return

            bump(_, label)
            return

    new_version: list[str] = current_version.split(".")
    new_version[location] = str(int(new_version[location]) + 1)
    new_version_string = ".".join(new_version)

    print(f"Current version: {current_version}")
    print(f"Bumped version: {new_version_string}")

    with open(version_file, "r") as f:
        content = f.read()

    content = content.replace(current_version, new_version_string)

    with open(version_file, "w") as f:
        f.write(content)

    return


@task(bump, update_dependencies, reformat)
def pre_commit(_: Context) -> None:
    pass

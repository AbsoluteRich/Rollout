from invoke import task
from rollout.__init__ import __version__ as current_version
from pathlib import Path


@task
def reformat(c):
    for command in [
        "python -m black tasks.py",
        "python -m black rollout",
        "python -m isort rollout --profile black",
    ]:
        c.run(command)


@task
def update_dependencies(c):
    for command in [
        "pipenv update",
        "pipenv requirements > requirements.txt",
        "pipenv requirements --dev > requirements-dev.txt",
    ]:
        c.run(command)


@task
def bump(_, label: str = None):
    version_file = Path.cwd() / "rollout" / "__init__.py"
    new_version = current_version.split(".")
    location = None

    while not location:
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

    new_version[location] = str(int(new_version[location]) + 1)
    new_version = ".".join(new_version)

    print(f"Current version: {current_version}")
    print(f"Bumped version: {new_version}")

    with open(version_file, "r") as f:
        content = f.read()

    with open(version_file, "w") as f:
        content = content.replace(current_version, new_version)
        f.write(content)


@task(bump, update_dependencies, reformat)
def pre_commit(_):
    pass

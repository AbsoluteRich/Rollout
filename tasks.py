from invoke import task
from rollout.__init__ import __version__ as current_version
from pathlib import Path

heavy_commands = [
    "pipenv update",
    "pipenv requirements > requirements.txt",
    "pipenv requirements --dev > requirements-dev.txt",
]
commands = [
    "python -m black tasks.py",
    "python -m black rollout",
    "python -m isort rollout --profile black",
]


@task
def pc(c, lite: bool = False):
    if not lite:
        for command in heavy_commands:
            c.run(command)

    for command in commands:
        c.run(command)


@task
def bump(_, label: str = "minor"):
    version_file = Path.cwd() / "rollout" / "__init__.py"
    new_version = current_version.split(".")

    match label:
        case "major":
            location = 0
        case "minor":
            location = 1
        case "patch":
            location = 2
        case _:
            print("Invalid semver label!")
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

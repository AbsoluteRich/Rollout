from pathlib import Path

from halo import Halo
from jinja2 import Environment

from . import commands

# This can't be a separate file, because where would that be stored?
TEMPLATE = """# Welcome to your new Python project!
{% if dependencies is defined %}{% for dependency in dependencies %}import {{ dependency }}
{% endfor %}{% endif %}
if __name__ == "__main__":
    pass

"""


def create_project_folders(project_name: str) -> bool:
    project_path = Path(project_name)
    if project_path.exists():
        return False

    project_path.mkdir()
    (project_path / "src").mkdir()
    return True


def create_entrypoint(project_name: str, packages: list) -> None:
    jinja = Environment()
    template = jinja.from_string(TEMPLATE)
    if packages:
        template = template.render(dependencies=packages)
    else:
        template = template.render()

    with open(Path(project_name) / "src" / "main.py", "w") as f:
        f.write(template)


def run(  # None of these parameters should have default value, that's what the CLI is for
    project_name: str,
    venv_name: str,
    packages: list[str] | None,
    version_specifier: str,
) -> tuple[True, Path] | tuple[False, str]:
    project_path = Path(project_name)

    with Halo("Creating project folders...", spinner="dots").start() as spin:
        success = create_project_folders(project_name)
        if not success:
            spin.fail(spin.text)
            return False, "Folder already exists. Try renaming or deleting it."
        spin.succeed(spin.text + " Done!")

    with Halo("Creating entrypoint...").start() as spin:
        create_entrypoint(project_name, packages)
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

        print(project_path / "requirements.txt")
        with Halo("Creating requirements file...", spinner="dots").start() as spin:
            with open(project_path / "requirements.txt", "w") as f:
                commands.pip_freeze(pip_executable, stdout=f, stderr=f, text=True)

            if version_specifier != "==":
                with open(project_path / "requirements.txt", "r") as f:
                    contents = f.read()
                print(contents)
                contents = contents.replace("==", version_specifier)
                print(contents)
                with open(project_path / "requirements.txt", "w") as f:
                    f.write(contents)

            spin.succeed(spin.text + " Done!")

    return True, Path.cwd() / project_name

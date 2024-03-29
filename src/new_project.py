from jinja2 import Environment, FileSystemLoader
from halo import Halo
from commands import venv, pip_install, pip_freeze
from pathlib import Path


def create_project_folders(project_name: str) -> bool:
    project_path = Path(project_name)
    if project_path.exists():
        return False

    project_path.mkdir()
    (project_path / "src").mkdir()
    return True


def create_entrypoint(project_name: str, packages: list) -> None:
    jinja = Environment(loader=FileSystemLoader(Path.cwd()))
    template = jinja.get_template("template.jinja2")
    if packages:
        template = template.render(dependencies=packages)
    else:
        template = template.render()

    with open(Path(project_name) / "src" / "main.py", "w") as f:
        f.write(template)


# https://github.com/manrajgrover/halo/issues/5
def run(
    project_name: str, venv_name: str, packages: list[str] | None = None
) -> tuple[bool, Path]:
    project_path = Path(project_name)

    spinner = Halo("Creating project folders...").start()
    success = create_project_folders(project_name)
    if not success:
        spinner.fail(spinner.text)
        return False, "Folder already exists. Try renaming or deleting it."
    spinner.succeed(spinner.text + " Done!")

    spinner = Halo("Creating entrypoint...").start()
    create_entrypoint(project_name, packages)
    spinner.succeed(spinner.text + " Done!")

    if venv_name:
        spinner = Halo("Setting up virtual environment...").start()
        venv(project_path / venv_name)
        spinner.succeed(spinner.text + " Done!")

    if packages and venv_name:
        pip_executable = project_path / venv_name / "Scripts" / "pip.exe"

        for package in packages:
            spinner = Halo(f"Installing {package} in {venv_name}...").start()
            with open(project_path / "pip-log.txt", "a") as f:
                pip_install(pip_executable, package, stdout=f, stderr=f, text=True)
            spinner.succeed(spinner.text + " Done!")

        spinner = Halo("Creating requirements file...").start()
        with open(project_path / "requirements.txt", "w") as f:
            pip_freeze(pip_executable, stdout=f, stderr=f, text=True)
        spinner.succeed(spinner.text + " Done!")

    return True, Path.cwd() / project_name

import argparse
import os
from jinja2 import Environment, FileSystemLoader
from halo import Halo
from commands import venv, pip_install, pip_freeze
from sys import exit


def create_project_folders(project_name: str) -> bool:
    if os.path.exists(project_name):
        return False
    os.makedirs(f"{project_name}/src")
    return True


def create_entrypoint(project_name: str, packages: list) -> None:
    jinja = Environment(loader=FileSystemLoader(os.getcwd()))
    template = jinja.get_template("template.jinja2")
    if packages:
        template = template.render(dependencies=packages)
    else:
        template = template.render()

    with open(f"{project_name}/src/main.py", "w") as f:
        f.write(template)


# https://github.com/manrajgrover/halo/issues/5
def main(project_name: str, venv_name: str, packages: list[str] | None = None) -> tuple[bool, str]:
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
        venv(os.path.join(project_name, venv_name))
        spinner.succeed(spinner.text + " Done!")

    if packages and venv_name:
        pip_path = os.path.join(project_name, venv_name, "Scripts")
        pip_executable = os.path.join(pip_path, "pip.exe")

        for package in packages:
            spinner = Halo(f"Installing {package} in {venv_name}...").start()
            with open(os.path.join(project_name, "pip-log.txt"), "a") as f:
                pip_install(pip_executable, package, stdout=f, stderr=f, text=True)
            spinner.succeed(spinner.text + " Done!")

        spinner = Halo("Creating requirements file...").start()
        with open(os.path.join(project_name, "requirements.txt"), "w") as f:
            pip_freeze(pip_executable, stdout=f, stderr=f, text=True)
        spinner.succeed(spinner.text + " Done!")

    return True, os.path.join(os.getcwd(), project_name)


def setup_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rollout",
        description="Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual "
                    "environment.",
    )

    parser.add_argument(
        "project_name", help="Name of the project.",
    )
    parser.add_argument(
        "--venv-name", help="What to name the virtual environment (.venv by default).\nIf called 'None', disables virtual environment creation.",
        default=".venv"
    )
    parser.add_argument(
        "--dependencies", "-d", help="Packages to install in the virtual environment (if any).",
        nargs="+",
    )

    return parser


if __name__ == "__main__":
    args = setup_cli().parse_args()

    if args.venv_name == "None":
        if args.dependencies:
            print("Packages will be ignored, as there is no virtual environment to install them to")
        result = main(
            args.project_name,
            packages=args.dependencies,
            venv_name=None
        )
    else:
        result = main(
            args.project_name,
            packages=args.dependencies,
            venv_name=args.venv_name
        )
    
    if result[0]:
        print(f"Your new project can be found at {result[1]}")
        if args.dependencies:
            print("If you don't need to see the output for the commands, you can delete 'pip-log.txt'.")
    else:
        print(f"[error] {result[1]}")
        if args.dependencies:
            print("Reading 'pip-log.txt' might help you solve your problem.")

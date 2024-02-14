import argparse
import os
from subprocess import run
from jinja2 import Environment, FileSystemLoader


# Todo: Split this one big function up into parts
def create_project(project_name: str, venv_name: str = "venv", packages: list[str] | None = None) -> tuple[bool, str]:
    print("Creating project folders...", end=" ", flush=True)
    if os.path.exists(project_name):
        return False, "Folder already exists. Try renaming or deleting it."
    os.makedirs(f"{project_name}/src")
    print("done.", flush=True)

    print("Setting up project...", end=" ", flush=True)
    jinja = Environment(loader=FileSystemLoader(os.getcwd()))
    template = jinja.get_template("template.jinja2")
    if packages:
        template = template.render(dependencies=packages)
    else:
        template = template.render()

    with open(f"{project_name}/src/main.py", "w") as f:
        f.write(template)
    print("done.", flush=True)

    print("Setting up virtual environment...", end=" ", flush=True)
    os.chdir(project_name)
    run(["python", "-m", "venv", venv_name], check=True)
    os.chdir(os.path.split(os.getcwd())[0])
    print("done.", flush=True)

    if packages:
        print("Installing packages via the virtual environment's pip", flush=True)
        os.chdir(os.path.join(project_name, venv_name, "Scripts"))
        arguments = ["pip.exe", "install"]
        arguments.extend(packages)
        run(arguments, check=True)

        requirements = run(["pip.exe", "freeze"], check=True, capture_output=True, text=True).stdout

        for _ in range(2):  # Gets from project\venv\Scripts to project
            os.chdir(os.path.split(os.getcwd())[0])
        
        print("Creating requirements file...", end=" ", flush=True)
        with open("requirements.txt", "w") as f:
            f.write(requirements)
        print("done.")

        return True, os.getcwd()

    return True, os.path.join(os.getcwd(), project_name)


cli = argparse.ArgumentParser(
    prog="rollout",
    description="Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual "
                "environment.",
)

cli.add_argument(
    "project_name", help="Name of the project",
)
cli.add_argument(
    "--dependencies", "-d", help="Packages to install in the virtual environment",
    nargs="+",
)

if __name__ == "__main__":
    args = cli.parse_args()
    result = create_project(args.project_name, packages=args.dependencies)
    if result[0]:
        print(f"Your new project can be found at {result[1]}")
    else:
        raise Exception(result[1])

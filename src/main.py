import argparse
import os
import subprocess


# Todo: Split this one big function up into parts
def create_project(project_name: str, venv_name: str = "venv", packages: list[str] | None = None) -> tuple[bool, str]:
    print("Creating project folders...", end="", flush=True)
    if os.path.exists(project_name):
        return False, "Folder already exists. Try renaming or deleting it."
    os.makedirs(f"{project_name}/src")
    print(" done.", flush=True)

    print("Setting up project...", end="", flush=True)
    with open("template.py") as template:
        with open(f"{project_name}/src/main.py", "w") as f:
            f.write(template.read())
    print(" done.", flush=True)

    print("Setting up virtual environment...", end="", flush=True)
    os.chdir(project_name)
    subprocess.run(["python", "-m", "venv", venv_name], shell=True, check=True)
    os.chdir(os.path.split(os.getcwd())[0])
    print(" done.", flush=True)

    if packages:
        print("Installing packages via the virtual environment's pip", flush=True)
        os.chdir(os.path.join(project_name, venv_name, "Scripts"))
        arguments = ["pip.exe", "install"]
        arguments.extend(packages)
        subprocess.run(arguments, shell=True, check=True)

        for _ in range(3):  # Gets from project\venv\Scripts to project
            os.chdir(os.path.split(os.getcwd())[0])

    return True, os.getcwd()


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
    if not result[0]:
        raise Exception(result[1])
    else:
        print(f"Your new project can be found at {result[1]}")
